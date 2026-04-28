#!/usr/bin/env python3
"""
bigfatsbox.py — Big Fat SBox List loader (generated using artificial intelligence)

Two access modes:

  Python mode
  -----------
  import bigfatsbox
  sb  = bigfatsbox.present          # SBoxEntry (or Sage SBox if in Sage)
  sb  = bigfatsbox.PRESENT          # case-insensitive
  sb.lookup_table                   # the LUT list
  sb.nonlinearity                   # any YAML field as attribute
  sb.to_dict()                      # raw dict

  from bigfatsbox import present    # same as bigfatsbox.present
  from bigfatsbox import *          # imports all entries as SBoxEntry objects

  aria = bigfatsbox.aria            # SBoxGroup (entries keyed ARIA.*)
  aria.s2                           # ARIA.S2 entry (case-insensitive sub-key)
  for sb in bigfatsbox.aria: ...    # iterate over all ARIA entries

  Sage mode (auto-detected when running inside SageMath)
  -------------------------------------------------------
  from bigfatsbox import present    # returns sage.crypto.sbox.SBox(lut)
  bigfatsbox.present                # same

  YAML/raw-dict mode (works in both Python and Sage)
  ---------------------------------------------------
  bigfatsbox.yaml.present           # raw dict from YAML
  bigfatsbox.yaml['PRESENT']        # same (case-insensitive)

For `import bigfatsbox` to work, `bigfatsbox.py` and all YAML data files must be
in the same directory, and that directory must either be the working directory
or be present on `sys.path`.
"""

from __future__ import annotations

import math as _math
import os
import re
import sys
import types as _types
from pathlib import Path
from typing import Any, Iterator

# ---------------------------------------------------------------------------
# Path setup — YAML files live alongside this script
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent
_PUBLIC = _HERE   # bigfatsbox.py and the YAML files share the same directory

# ---------------------------------------------------------------------------
# Last-update stamp — read from README.md in the same directory
# ---------------------------------------------------------------------------

def _read_last_update() -> str | None:
    readme = _HERE / 'README.md'
    if not readme.exists():
        return None
    with open(readme, encoding='utf-8') as _f:
        for _line in _f:
            _m = re.match(r'^Last update:\s*(.+?)\s*<!--', _line)
            if _m:
                return _m.group(1).strip()
    return None

last_update: str | None = _read_last_update()

# ---------------------------------------------------------------------------
# Raw data store
# ---------------------------------------------------------------------------

_raw: dict[str, dict]  = {}   # UPPERCASE key → raw YAML dict
_aliases: dict[str, str] = {}  # alias UPPERCASE → canonical UPPERCASE
_loaded: bool = False


def _ensure_loaded() -> None:
    global _loaded
    if _loaded:
        return
    _loaded = True
    _do_load()


def _do_load() -> None:
    try:
        import yaml as _yaml
        _safe_load = _yaml.safe_load
    except ImportError:
        raise ImportError(
            "PyYAML is required to use bigfatsbox.\n"
            "Install it with:  pip install pyyaml"
        )

    for fpath in sorted(_PUBLIC.glob('*.yaml')):
        with open(fpath, encoding='utf-8') as f:
            data = _safe_load(f)
        if not isinstance(data, dict):
            continue
        for key, val in data.items():
            if not isinstance(val, dict):
                continue
            ukey = key.upper()
            _raw[ukey] = val
            # Register canonical aliases list (e.g. AES has ARIA_S1, RIJNDAEL…)
            for alias in (val.get('aliases') or []):
                _aliases[str(alias).upper()] = ukey
        # Register alias-entry keys (e.g. RIJNDAEL: {alias: AES})
    for key, val in list(_raw.items()):
        if isinstance(val, dict) and 'alias' in val:
            target = str(val['alias']).upper()
            _aliases[key] = target


def _resolve(name: str) -> str | None:
    """Resolve name (possibly alias) to canonical UPPERCASE key, or None."""
    _ensure_loaded()
    uname = name.upper()
    visited: set[str] = set()
    while uname in _aliases and uname not in visited:
        visited.add(uname)
        uname = _aliases[uname]
    if uname in _raw:
        return uname
    return None


# ---------------------------------------------------------------------------
# Sage detection
# ---------------------------------------------------------------------------

def _in_sage() -> bool:
    """Return True when running inside a SageMath session."""
    return 'sage.all' in sys.modules or 'sage' in sys.modules


def _sage_sbox(lut: list) -> Any | None:
    """Return a sage.crypto.sbox.SBox object, or None if Sage unavailable."""
    try:
        from sage.crypto.sbox import SBox   # type: ignore
        return SBox(lut)
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# SBoxEntry — wrapper around a single YAML entry dict
# ---------------------------------------------------------------------------

class SBoxEntry:
    """
    Thin wrapper providing attribute access to a single S-box YAML entry.

    Field access:
        sb.lookup_table        → list of ints
        sb.nonlinearity        → int
        sb.algebraic_degree    → list of ints
        sb.univariate_polynomial → str or None
        sb.note                → str or None
        ...  (any YAML field)

    Convenience:
        sb.lut                 → alias for sb.lookup_table
        sb.to_dict()           → copy of the raw dict
        sb.to_sage()           → sage.crypto.sbox.SBox(lut)  (if Sage available)
        sb.keys()              → dict_keys view of available fields
        sb.fields              → list of available field names (indexable: sb.fields[0])
    """

    __slots__ = ('_name', '_data')

    def __init__(self, name: str, data: dict) -> None:
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_data', data)

    # ── attribute access ────────────────────────────────────────────────────

    def __getattr__(self, attr: str) -> Any:
        data = object.__getattribute__(self, '_data')
        if attr in data:
            return data[attr]
        alt = attr.replace('_', '-')
        if alt in data:
            return data[alt]
        raise AttributeError(
            f"SBoxEntry '{object.__getattribute__(self, '_name')}' "
            f"has no field '{attr}'"
        )

    # ── convenience properties ──────────────────────────────────────────────

    @property
    def lut(self) -> list | None:
        data = object.__getattribute__(self, '_data')
        return data.get('lookup_table', data.get('lut'))

    @property
    def name(self) -> str:
        return object.__getattribute__(self, '_name')

    @property
    def input_size(self) -> int:
        """Number of input bits: log₂ of the LUT length."""
        lut = self.lut
        if lut is None:
            raise ValueError(f"SBoxEntry '{self.name}' has no lookup table")
        return int(_math.log2(len(lut)))

    @property
    def output_size(self) -> int:
        """Number of output bits: from output_bits field, or equals input_size for bijective."""
        data = object.__getattribute__(self, '_data')
        ob = data.get('output_bits', data.get('output-bits'))
        if ob is not None:
            return int(ob)
        return self.input_size

    # ── utility methods ─────────────────────────────────────────────────────

    def keys(self):
        return object.__getattribute__(self, '_data').keys()

    @property
    def fields(self) -> list:
        """List of available field names for this entry. Supports indexing: sb.fields[0]."""
        return list(object.__getattribute__(self, '_data').keys())

    def to_dict(self) -> dict:
        return dict(object.__getattribute__(self, '_data'))

    def to_sage(self):
        """Return a sage.crypto.sbox.SBox object for this entry (requires Sage)."""
        lut = self.lut
        if lut is None:
            raise ValueError(f"SBoxEntry '{self.name}' has no lookup table")
        obj = _sage_sbox(lut)
        if obj is None:
            raise ImportError("SageMath is not available")
        return obj

    # ── dunder ──────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        name   = object.__getattribute__(self, '_name')
        data   = object.__getattribute__(self, '_data')
        origin = data.get('origin', '')
        short  = (origin[:57] + '...') if len(origin) > 60 else origin
        return f"SBoxEntry({name!r}, origin={short!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SBoxEntry):
            return (object.__getattribute__(self, '_name')
                    == object.__getattribute__(other, '_name'))
        return NotImplemented

    def __hash__(self) -> int:
        return hash(object.__getattribute__(self, '_name'))


# ---------------------------------------------------------------------------
# SBoxGroup — multiple related S-boxes (e.g. all ARIA.* entries)
# ---------------------------------------------------------------------------

class SBoxGroup:
    """
    A namespace grouping related S-box entries.

    Example:
        bigfatsbox.aria          # all entries whose key starts with ARIA
        bigfatsbox.aria.s2       # ARIA.S2 (case-insensitive sub-key)
        list(bigfatsbox.aria)    # iterate over all ARIA entries
    """

    def __init__(self, group_name: str) -> None:
        object.__setattr__(self, '_gname', group_name)
        object.__setattr__(self, '_members', {})   # lower-case sub-key → entry

    def _add(self, sub_key: str, entry: 'SBoxEntry') -> None:
        object.__getattribute__(self, '_members')[sub_key.lower()] = entry

    def __getattr__(self, name: str) -> 'SBoxEntry':
        members = object.__getattribute__(self, '_members')
        key = name.lower()
        if key in members:
            return members[key]
        # Fallback: try a full lookup e.g. ARIA.S1
        gname = object.__getattribute__(self, '_gname')
        entry = _get_entry(f'{gname}.{name.upper()}')
        if entry is not None:
            return entry
        raise AttributeError(
            f"SBoxGroup '{gname}' has no member '{name}'"
        )

    def __iter__(self) -> Iterator['SBoxEntry']:
        return iter(object.__getattribute__(self, '_members').values())

    def __len__(self) -> int:
        return len(object.__getattribute__(self, '_members'))

    def __repr__(self) -> str:
        gname   = object.__getattribute__(self, '_gname')
        members = object.__getattribute__(self, '_members')
        return f"SBoxGroup({gname!r}, members={sorted(members.keys())})"


# ---------------------------------------------------------------------------
# Core lookup helpers
# ---------------------------------------------------------------------------

def _wrap(name: str, data: dict) -> 'SBoxEntry | Any':
    """Wrap data as SBoxEntry (or Sage SBox when inside a Sage session)."""
    if _in_sage():
        lut = data.get('lookup_table', data.get('lut'))
        if lut and isinstance(lut, list):
            obj = _sage_sbox(lut)
            if obj is not None:
                return obj
    return SBoxEntry(name, data)


def _get_entry(name: str) -> 'SBoxEntry | Any | None':
    """Resolve name and return wrapped entry, or None if not found."""
    _ensure_loaded()
    canonical = _resolve(name)
    if canonical is None:
        return None
    data = _raw[canonical]
    if 'alias' in data:
        return _get_entry(str(data['alias']))
    return _wrap(canonical, data)


def _get_raw(name: str) -> dict | None:
    """Return the raw dict for an entry by name, or None."""
    _ensure_loaded()
    canonical = _resolve(name)
    if canonical is None:
        return None
    data = _raw[canonical]
    if 'alias' in data:
        return _get_raw(str(data['alias']))
    return data


# ---------------------------------------------------------------------------
# Group builder
# ---------------------------------------------------------------------------

_groups_cache: dict[str, SBoxGroup] | None = None


def _build_groups() -> dict[str, SBoxGroup]:
    _ensure_loaded()
    groups: dict[str, SBoxGroup] = {}

    for ukey in _raw:
        # Entries with dotted names like ARIA.S2 → group ARIA
        if '.' in ukey:
            prefix = ukey.split('.')[0]
            sub    = '.'.join(ukey.split('.')[1:])  # everything after first dot
            if prefix not in groups:
                groups[prefix] = SBoxGroup(prefix)
            entry = _get_entry(ukey)
            if entry is not None:
                groups[prefix]._add(sub, entry)

        # Entries with underscore + digit suffix like LBLOCK_S0 → group LBLOCK
        # (heuristic: last segment is S<digit> or <digit>)
        parts = ukey.rsplit('_', 1)
        if len(parts) == 2:
            suffix = parts[1]
            if (suffix.isdigit()
                    or (suffix.upper().startswith('S') and suffix[1:].isdigit())):
                prefix = parts[0]
                if prefix not in groups:
                    groups[prefix] = SBoxGroup(prefix)
                entry = _get_entry(ukey)
                if entry is not None:
                    groups[prefix]._add(suffix.lower(), entry)

    return groups


def _get_group(name: str) -> SBoxGroup | None:
    global _groups_cache
    if _groups_cache is None:
        _groups_cache = _build_groups()
    uname = name.upper()
    return _groups_cache.get(uname)


# ---------------------------------------------------------------------------
# YAML proxy — always returns raw dicts regardless of Sage mode
# ---------------------------------------------------------------------------

class _YAMLProxy:
    """
    bigfatsbox.yaml.present  →  raw dict (not SBox object)
    bigfatsbox.yaml['PRESENT']  →  same (case-insensitive)

    Useful when you want to inspect all YAML fields rather than getting a
    opaque Sage SBox object.
    """

    def __getattr__(self, name: str) -> dict:
        if name.startswith('_'):
            raise AttributeError(name)
        data = _get_raw(name)
        if data is not None:
            return data
        raise AttributeError(f"bigfatsbox.yaml: no entry '{name}'")

    def __getitem__(self, name: str) -> dict:
        return self.__getattr__(name)

    def __repr__(self) -> str:
        return 'bigfatsbox.yaml  (raw YAML dict access)'

    def all_entries(self) -> dict[str, dict]:
        """Return all entries as a dict of uppercase-key → raw-dict."""
        _ensure_loaded()
        return dict(_raw)

    def all_names(self) -> list[str]:
        """Return all entry keys (uppercase)."""
        _ensure_loaded()
        return sorted(_raw.keys())


yaml = _YAMLProxy()

# ---------------------------------------------------------------------------
# Wildcard search  (bigfatsbox.find('pre*')  or  bigfatsbox['pre*'])
# ---------------------------------------------------------------------------

def find(pattern: str) -> 'dict[str, SBoxEntry | Any]':
    """
    Return a dict of all entries whose name matches *pattern*.

    Supports ``*`` (any characters) and ``?`` (single character) wildcards.
    Matching is case-insensitive.

    Examples::

        bigfatsbox.find('pre*')       # PRESENT, PRIDE, PRINCE, …
        bigfatsbox.find('aria.*')     # all ARIA sub-entries
        bigfatsbox.find('*_s0')       # every entry ending in _S0
        bigfatsbox['pre*']            # same via bracket notation
    """
    import fnmatch as _fnmatch
    _ensure_loaded()
    upat = pattern.upper()
    result: dict[str, Any] = {}
    for ukey in sorted(_raw):
        if _fnmatch.fnmatchcase(ukey, upat):
            entry = _get_entry(ukey)
            if entry is not None:
                result[ukey] = entry
    return result


# ---------------------------------------------------------------------------
# Bit-size access  (bigfatsbox.b4.present,  bigfatsbox.load_bits(4))
# ---------------------------------------------------------------------------

def load_bits(n: int) -> 'dict[str, SBoxEntry | Any]':
    """
    Load and return all SBoxes with input bit size *n*.

    Returns a dict mapping uppercase key → SBoxEntry (or Sage SBox if in Sage).
    """
    _ensure_loaded()
    result: dict[str, Any] = {}
    for ukey, data in _raw.items():
        if 'alias' in data:
            continue
        lut = data.get('lookup_table', data.get('lut'))
        if lut and isinstance(lut, list) and len(lut) > 0:
            try:
                bits = int(_math.log2(len(lut)))
                if bits == n:
                    entry = _get_entry(ukey)
                    if entry is not None:
                        result[ukey] = entry
            except (ValueError, ZeroDivisionError):
                pass
    return result


def _entry_is_bijective(entry: 'SBoxEntry') -> bool:
    """Return True if the entry is a bijective SBox (no output_bits field)."""
    data = object.__getattribute__(entry, '_data')
    return 'output_bits' not in data


class _BitSizeNamespace:
    """
    Lazy namespace exposing all SBoxes of a given input bit size.

        bigfatsbox.b4.present   →  SBoxEntry('PRESENT')
        bigfatsbox.b8.bijective  →  dict of bijective 8-bit SBoxes
        bigfatsbox.b8.nonbijective  →  dict of non-bijective 8-bit SBoxes
        for sb in bigfatsbox.b4: ...
    """

    __slots__ = ('_bits', '_cache')

    def __init__(self, bits: int) -> None:
        object.__setattr__(self, '_bits', bits)
        object.__setattr__(self, '_cache', None)

    def _get_all(self) -> 'dict[str, SBoxEntry | Any]':
        cache = object.__getattribute__(self, '_cache')
        if cache is not None:
            return cache
        bits = object.__getattribute__(self, '_bits')
        cache = load_bits(bits)
        object.__setattr__(self, '_cache', cache)
        return cache

    def __getattr__(self, name: str) -> 'SBoxEntry | Any':
        if name == 'bijective':
            return {k: v for k, v in self._get_all().items() if _entry_is_bijective(v)}
        if name == 'nonbijective':
            return {k: v for k, v in self._get_all().items() if not _entry_is_bijective(v)}
        all_e = self._get_all()
        uname = name.upper()
        if uname in all_e:
            return all_e[uname]
        for key in all_e:
            if key.endswith('.' + uname) or key.endswith('_' + uname):
                return all_e[key]
        bits = object.__getattribute__(self, '_bits')
        raise AttributeError(f"bigfatsbox.b{bits}: no S-box '{name}'")

    def __iter__(self) -> 'Iterator[SBoxEntry | Any]':
        return iter(self._get_all().values())

    def __len__(self) -> int:
        return len(self._get_all())

    def __repr__(self) -> str:
        bits = object.__getattribute__(self, '_bits')
        all_e = self._get_all()
        n_bij = sum(1 for v in all_e.values() if _entry_is_bijective(v))
        n_non = len(all_e) - n_bij
        if n_non:
            return f"bigfatsbox.b{bits}  ({bits}-bit S-box namespace: {n_bij} bijective, {n_non} non-bijective)"
        return f"bigfatsbox.b{bits}  ({bits}-bit S-box namespace, {n_bij} entries)"


_bN_cache: dict[int, _BitSizeNamespace] = {}


def _get_bN(n: int) -> _BitSizeNamespace:
    if n not in _bN_cache:
        _bN_cache[n] = _BitSizeNamespace(n)
    return _bN_cache[n]


# ---------------------------------------------------------------------------
# Module-level attribute access  (enables  from bigfatsbox import present)
# ---------------------------------------------------------------------------

def __getattr__(name: str) -> Any:
    """Called by Python when an attribute is not found on the module."""
    if name.startswith('_') or name in ('yaml', 'last_update', 'find',
                                         'load_bits',
                                         '__file__', '__spec__',
                                         '__loader__', '__path__',
                                         '__package__', '__builtins__'):
        raise AttributeError(name)

    # bN namespace  (b4, b8, b3, etc.)
    m = re.match(r'^b(\d+)$', name.lower())
    if m:
        return _get_bN(int(m.group(1)))

    _ensure_loaded()

    # Direct entry lookup (case-insensitive)
    entry = _get_entry(name)
    if entry is not None:
        return entry

    # Group lookup (e.g.  bigfatsbox.aria  →  SBoxGroup)
    group = _get_group(name)
    if group is not None:
        return group

    raise AttributeError(
        f"bigfatsbox has no S-box or group named '{name}'.\n"
        f"Use bigfatsbox.yaml.all_names() to see all available entries."
    )


# ---------------------------------------------------------------------------
# __dir__ and __all__  (for  from bigfatsbox import *)
# ---------------------------------------------------------------------------

def __dir__() -> list[str]:
    _ensure_loaded()
    return sorted(
        set(list(_raw.keys()) + list(_aliases.keys()))
        | {'yaml', 'last_update', 'find', 'load_bits', 'SBoxEntry', 'SBoxGroup'}
        | {f'b{n}' for n in range(3, 17)}
    )


# __all__ computed at import time so that  from bigfatsbox import *  works.
def _make_all() -> list[str]:
    _ensure_loaded()
    return [k for k in _raw if not k.startswith('_')]


__all__ = _make_all()


# ---------------------------------------------------------------------------
# Module-level __getitem__ — enables  bigfatsbox['pre*']  bracket syntax
# ---------------------------------------------------------------------------

class _BigFatModule(_types.ModuleType):
    """Module subclass that adds subscription syntax for wildcard lookup."""

    def __getitem__(self, name: str) -> 'dict | SBoxEntry | Any':
        """
        bigfatsbox['AES']   →  same as bigfatsbox.aes
        bigfatsbox['pre*']  →  dict of all matching entries (same as find)
        """
        if '*' in name or '?' in name:
            return find(name)
        entry = _get_entry(name)
        if entry is not None:
            return entry
        raise KeyError(f"bigfatsbox: no S-box '{name}'")


sys.modules[__name__].__class__ = _BigFatModule


# ---------------------------------------------------------------------------
# CLI helper  (python bigfatsbox.py present)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import json

    names = sys.argv[1:]
    if not names:
        print("Usage: python bigfatsbox.py <sbox_name> [<sbox_name> ...]")
        print(f"Available entries: {len(_make_all())}")
        sys.exit(0)

    _ensure_loaded()
    for name in names:
        raw = _get_raw(name)
        if raw is None:
            print(f"Not found: {name}", file=sys.stderr)
        else:
            print(f"# {name.upper()}")
            # Pretty-print non-LUT fields first, then LUT
            lut = raw.get('lookup_table', raw.get('lut'))
            for k, v in raw.items():
                if k not in ('lookup_table', 'lut'):
                    print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
            if lut is not None:
                print(f"  lookup_table: [{', '.join(map(str, lut))}]")
