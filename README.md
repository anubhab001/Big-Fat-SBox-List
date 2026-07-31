# Big-Fat-SBox-List

Public collection of Substitution Boxes (SBoxes for short) used in cryptography

Last update: 31 July 2026 <!-- TODO: This is to be updated in UTC with each (major) commit/push -->

## Organisation

- YAML files containing details about multiple SBoxes, properties, cryptographic properties, historical notes etc.

- Files are written by input size (each input size in bits gets a new file) and bijectivity (non-bijective SBoxes are moved to other files). Additionally, due to large number of 4-bit bijective SBoxes, those are split into 2 files based on whether or not those are used in a cipher ([`4bit_cipher.yaml`](4bit_cipher.yaml)) or just exemplary / representative ([`4bit_nocipher.yaml`](4bit_nocipher.yaml)).

- Entries within each YAML file are in alphabetical order by key.

## Naming Convention

- Entry keys use an all-uppercase Latin with/without dot convention (e.g., `PRESENT` as without dot; `MIDORI.SB0`, `JH.S0` as with dot), with no hyphen and no space. Note that the cipher name preceeds the dot and the SBox name is after dot, or if there is no specific name to its SBox then only the cipher's name or some identifier (like `DILLON`) is used.

- `canonical_name` field records the exact name as it appears in the original paper to preserve information (related to casing, non-Latin characters, subscript, hyphen, space). 

- Lowercase `v` indicates a version number and is not part of the cipher name (e.g., `PRINCEv2`).

- The underscore `_` is a permitted special character. Its principal use is the `_Inv` suffix, which indicates that the entry is the inverse of another SBox already included (e.g., `ARIA.S2_Inv`).

- The all-uppercase rule may be relaxed where a version or variant designator would otherwise be lost. For example, the trailing letter in `SNOW V` or `ROCCA S` marks a specific version, so it is retained as a designator rather than being folded into an indistinct run of capitals. The exact form is always preserved in `canonical_name` (e.g., `["SNOW-V"]`, `["ROCCA-S"]`).


## Data Files

### Bijective SBoxes

| File | # Entry | Bit Mapping | 
|:------|:-------:|-------------:|
| [`3bit.yaml`](3bit.yaml) | 7 | 3 → 3 |
| [`4bit_cipher.yaml`](4bit_cipher.yaml) | 147 | 4 → 4 |
| [`4bit_nocipher.yaml`](4bit_nocipher.yaml) | 354 | 4 → 4 |
| [`5bit.yaml`](5bit.yaml) | 16 | 5 → 5 |
| [`6bit.yaml`](6bit.yaml) | 5 | 6 → 6 |
| [`7bit.yaml`](7bit.yaml) | 2 | 7 → 7 |
| [`8bit.yaml`](8bit.yaml) | 66 | 8 → 8 |
| [`9bit.yaml`](9bit.yaml) | 1 | 9 → 9 |

### Non-Bijective SBoxes

| File | # Entry | Bit Mapping |
|:------|:-------:|-------------:|
| [`nonbijective4bit.yaml`](nonbijective4bit.yaml) | 1 | 4 → 2 |
| [`nonbijective6bit.yaml`](nonbijective6bit.yaml) | 8 | 6 → 4 |
| [`nonbijective8bit.yaml`](nonbijective8bit.yaml) | 3 | 8 → 8 |

## Entry Format

Each YAML entry has the following fields in order (mandatory fields marked with *, conditionally mandatory fields marked with †):

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name` | list | Name as written in the original paper (preserving case, non-Latin character, subscript, hyphen, space) |
| `output_bits`<sup>†</sup> | int | Output bit size; compulsory for non-bijective SBoxes; skipped for bijective SBoxes |
| `lookup_table`<sup>*</sup> | list | Look-up table (substitution values) |
| `algebraic_degree`<sup>*</sup> | list | Algebraic degree of each coordinate function in order from the least-significant output bit (bit 0) to the most-significant (bit $n−1$). For an $n$-bit SBox there are $n$ integers in the list. The overall degree of the SBox is the maximum of these values. |
| `nonlinearity`<sup>*</sup> | int | Non-linearity: Minimum Hamming distance from the set of all affine Boolean functions, taken over all non-zero linear combinations of output bits |
| `differential_uniformity`<sup>*</sup> | int | Differential uniformity (DU): Maximum number of input pairs $(x, x')$ with $x \oplus x' = \Delta_{in}$ such that $S(x) \oplus S(x') = \Delta_{out}$, maximised over all non-zero $\Delta_{in}$ and all $\Delta_{out}$ |
| `absolute_linear_uniformity`<sup>*</sup> | int | Absolute linear uniformity (ALU): Maximum absolute value of any entry in the linear approximation table (LAT), excluding row 0 (input mask = 0) and column 0 (output mask = 0) |
| `boomerang_uniformity`<sup>†</sup> | int | Boomerang Uniformity: Maximum entry of the boomerang connectivity table (BCT). The BCT entry for $\Delta_{in}, \Delta_{out}$ counts the number of $x$ such that $S^{-1}(S(x) \oplus \Delta_{out}) \oplus S^{-1}(S(x \oplus \Delta_{in}) \oplus \Delta_{out}) = \Delta_{in}$, maximised over all non-zero $\Delta_{in}, \Delta_{out}$; compulsory for bijective SBoxes; skipped for non-bijective SBoxes |
| `absolute_autocorrelation_uniformity`<sup>*</sup> | int | Absolute autocorrelation uniformity (AAU): Maximum absolute value in the autocorrelation table (ACT); $\mathrm{ACT}[a,b] = \sum_x (-1)^{\langle b,\, S(x \oplus a) \oplus S(x)\rangle}$ for non-zero input difference $a$ and non-zero output mask $b$; also called absolute indicator |
| `differential_branch_number`<sup>*</sup> | int | Differential branch number: Minimum weight $\mathrm{wt}(\Delta_{in}) + \mathrm{wt}(\Delta_{out})$ over all non-trivial DDT entries |
| `linear_branch_number`<sup>*</sup> | int | Linear branch number: Minimum weight $\mathrm{wt}(a) + \mathrm{wt}(b)$ over all non-trivial LAT entries |
| `involution`<sup>*</sup> | bool | Involutory SBox: True iff $S(S(x)) = x$  $\forall x$ |
| `order`<sup>†</sup> | int | Least $k$ with $S$ applied $k$ times equal to the identity, that is, the least common multiple of the cycle lengths; compulsory for bijective SBoxes, skipped for non-bijective SBoxes. An involution has order $2$ |
| `fixed_point`<sup>*</sup> | list | Fixed point:  Values where $S(x) = x$ (`[]` for no fixed point) |
| `year`<sup>*</sup> | list | Collection of significant publication years (competition submission, journal publication, standard approval) etc. |
| `cipher`<sup>*</sup> | bool | True iff used in a cipher |
| `source` | str | One or more URL(s) of code or related resources (mainly [PEIGEN SBox collection](https://github.com/peigen-sboxes/PEIGEN/tree/master/EvaluationResults/Sect5.1_CryptographicProperties), [Sage reference manual](https://github.com/sagemath/sage/blob/develop/src/sage/crypto/sboxes.py)) whence some information is mined |
| `origin`<sup>*</sup> | str | Citation of the original publication |
| `aliases` | list | Ciphers that have rebranded this SBox under a new name |
| `alias` | str | The cipher whose SBox this entry is an alias for; placed immediately below `canonical_name` |
| `reuse` | list | Ciphers that reuse this SBox under its original name |
| `note` | str | Remarks such as government-body origin, competition/standardization status, related cryptographic properties or information |
| `trivium` | str | Lesser-known trivium about the cipher at hand (e.g., etymology, but not related to cryptographic importance) |


### Reuse and Rebranding (Alias)

Three fields handle inter-cipher SBox relationships:

- **`reuse`** (list in main entry): Ciphers that explicitly use this SBox under its original name (i.e., without giving a new name). No separate entry is created for the reusing cipher. For example, `CRAFT` reuses the `MIDORI Sb0` SBox (`CRAFT` appears in `MIDORI.SB0`'s `reuse` list) without renaming it as the `CRAFT` SBox.

- **`alias`** (field in a secondary entry, replacing `lut`): A cipher that takes another cipher's SBox and renames it as its own gets a standalone entry with `alias: SOURCE_CIPHER`. This entry can carry `year`, `canonical_name` and `note` (if available), but cannot carry `lut` (as `lut` is to be read from its `alias`).

- **`aliases`** (list in main entry): The inverse of `alias`. Lists all ciphers whose own entries have `alias:` pointing to this main entry. In other words, ciphers that have rebranded this SBox under a new name.


### Notes

1. Our convention — uppercase Latin characters with the dot and the underscore allowed — enforces uniformity and ASCII searchability, but it destroys the original typographic formatting used by the designers, such as mixed case (e.g., "Midori"), non-Latin characters (like Cyrillic "π"; Greek "σ"), subscript notation (e.g., "Sb₀"), hyphen (like "SHA-3") and space (like "SNOW 3G"). 

2. `canonical_name` — which is applicable only when `cipher` is true, and used to preserve the original formatting as intended by the cipher's designer(s) — is a list. For a cipher with a single SBox, it is a one-element list (e.g., `["GIFT"]`). When a cipher has multiple SBoxes distinguished by a subscript or letter (e.g., `S₀`, `π₁`), it is a two-element list `["CipherName", "SBoxName"]` where the first element is the cipher's canonical name and the second is the specific SBox sub-name (e.g., `["CLEFIA", "S₁"]`).

3. `alias` (a secondary entry's field pointing to one source) and `aliases` (the main entry's list of ciphers that rebranded it) are not the singular and plural of the same concept. `reuse` is not linked with `alias` or `aliases` (both `alias` and `aliases` deal with cases where an SBox ) 

4. `year` field is a list of significant publication years (e.g., competition submission, journal publication, standard approval). Single-year entries still use list format: `year: [2019]`. Multi-year entries carry inline comments explaining each year (e.g., `year: [2014, 2023]  # CAESAR submission (2014); NIST LWC winner (2023)`). 

5. The dot notation is not restricted to ciphers; non-cipher research entries may also use it (e.g., `APN.1` where APN is a class and 1 is an index).

6. In a secondary (alias) entry, the `alias` field is placed immediately below `canonical_name`, ahead of any `year`, `origin` or `note`.

7. Each URL is prefixed with `URL: `. Multiple URLs are separated by `; `.

## Python / Sage Loader

### Installing / Importing
[`bigfatsbox.py`](bigfatsbox.py) is a loader that exposes every YAML entry as a Python object. It requires Python 3.11+ or SageMath 9.3+, on top of [PyYAML](https://pypi.org/project/PyYAML/).

With all files (including YAML data files) available in the working directory (or on `sys.path`), the following should work inside a Python or Sage REPL:

```python
import bigfatsbox
print(bigfatsbox.last_update)    # Prints '24 April 2026 23:54 UTC'
```


### Python

The following data types (case-insensitive) are accessible:
- `SBoxEntry` is the Python class wrapping a single YAML entry.
- `SBoxGroup` groups related entries under a common cipher prefix (e.g. all `ARIA.*` entries together).

The `repr` of an `SBoxEntry` shows the key name and (truncated) origin for quick identification in a REPL (though access is always by name alone):

```python
sb = bigfatsbox.present          # SBoxEntry('PRESENT', origin='Bogdanov et al.; PRESENT: An Ultra-Lightweight Block Ciph...')
print(sb.lookup_table)           # Prints (12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2)
print(sb.nonlinearity)           # Prints 4
print(sb.differential_uniformity)  # Prints 4
print(sb.absolute_linear_uniformity)  # Prints 4
print(sb.boomerang_uniformity)   # Prints 16
print(sb.absolute_autocorrelation_uniformity)  # Prints 16
print(sb.differential_branch_number)  # Prints 3
print(sb.linear_branch_number)   # Prints 2
print(sb.involution)             # Prints False
print(sb.fixed_point)            # Prints ()
print(sb.year)                   # Prints (2007,)
print(sb.cipher)                 # Prints True
print(sb.canonical_name)         # Prints ('PRESENT',)
print(sb.lut)                    # Alias for lookup_table
print(sb.input_size)             # Prints 4  (log₂ of LUT length)
print(sb.output_size)            # Prints 4  (equals input_size for bijective; from output_bits for non-bijective)
print(sb.keys())                 # Returns dict_keys view of available fields
print(sb.fields)                 # List of available field names
print(sb.fields[0])              # Prints 'lookup_table'
print(sb.to_dict())              # Raw dict copy of all YAML fields

# Case-insensitive access
assert bigfatsbox.PRESENT == bigfatsbox.present

# Bracket access (exact name, case-insensitive)
sb = bigfatsbox['PRESENT']       # same as bigfatsbox.present

# Import by name
from bigfatsbox import present, aes

# Import everything (loads all YAML files)
from bigfatsbox import *
```

Ciphers with multiple SBoxes are accessible as `SBoxGroup` objects:

```python
aria = bigfatsbox.aria            # SBoxGroup('ARIA', members=['inv', 's2', 's2_inv', 'sq', 'sq_inv'])
print(aria.s2)                   # SBoxEntry('ARIA.S2', origin='Kwon et al.; New Block Cipher: ARIA; ICISC 2003; URL: h...')
print(aria.s2.lookup_table)      # Prints [...]
for sb in aria:                   # Iterate all ARIA entries
    print(sb.name, sb.nonlinearity)

clefia = bigfatsbox.clefia        # SBoxGroup for CLEFIA.S0, CLEFIA.S1
print(clefia.s0.canonical_name)  # Prints ('CLEFIA', 'S₀')
```


### Lazy Loading and Access through Size

The loader is lazy, meaning importing `bigfatsbox` does not load any YAML file immediately. To load all SBoxes of a given input bit size, use `load_bits(n)` or the `bN` namespace:

```python
# Load all 4-bit SBoxes (reads only 4bit_cipher.yaml, 4bit_nocipher.yaml,
# and nonbijective4bit.yaml)
all_4bit = bigfatsbox.load_bits(4)   # Dict: uppercase key → SBoxEntry
print(len(all_4bit))                 # Prints approx. 500 (all bijective + non-bijective 4-bit)

# Bit-size namespace (b3, b4, b5, b6, b7, b8, b9 are pre-wired)
b4 = bigfatsbox.b4                   # Namespace for all 4-bit SBoxes
print(b4.present)                    # SBoxEntry('PRESENT')

# Access from a namespace
from bigfatsbox import b8
print(b8.aes)                        # SBoxEntry('AES')
```

Accessing `sb.input_size` and `sb.output_size` works on any loaded entry:

```python
print(bigfatsbox.aes.input_size)    # Prints 8
print(bigfatsbox.aes.output_size)   # Prints 8
print(bigfatsbox.cmea.output_size)  # Prints 8  (non-bijective; from output_bits field)
```

### Wildcard Search

`bigfatsbox.find(pattern)` returns a dict of all entries matching a wildcard pattern. Bracket notation `bigfatsbox['pattern']` is equivalent for wildcards:

```python
# find() — returns dict: uppercase key → SBoxEntry
matches = bigfatsbox.find('pre*')      # PRESENT, PRIDE, PRIDE_Inv, PRINCE, PRINCEv2, …
matches = bigfatsbox.find('ARIA.*')    # ARIA.INV, ARIA.S2, ARIA.S2_Inv, ARIA.SQ, ARIA.SQ_Inv
matches = bigfatsbox.find('*_S0')      # All entries ending in _S0
matches = bigfatsbox.find('AE.*')      # All non-cipher AE research SBoxes

# Bracket notation (equivalent to find for wildcards)
matches = bigfatsbox['pre*']           # Same as bigfatsbox.find('pre*')

# Iterate results
for name, sb in bigfatsbox.find('pre*').items():
    print(name, sb.nonlinearity, sb.differential_uniformity)

# Exact bracket access (non-wildcard)
sb = bigfatsbox['PRESENT']            # same as bigfatsbox.present
```



### Sage (Automatic)

When `import bigfatsbox` is evaluated inside a SageMath session, attribute access automatically returns a [`sage.crypto.sbox.SBox`](https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/sbox.html#sage.crypto.sbox.SBox) object directly. Additional metadata fields (`note`, `trivium`, `year`, `origin`, etc.) are not exposed via the SBox object itself but remain accessible via `bigfatsbox.yaml`:

```python
# Inside a Sage session:
aes = bigfatsbox.aes               # sage.crypto.sbox.SBox object
print(aes.differential_uniformity())    # Prints 4  (Sage method, not attribute)
print(aes.nonlinearity())               # Prints 112
print(aes.boomerang_uniformity())       # Prints 4
print(aes.is_bijective())               # Prints True

# Wildcard search and bit-size access work identically in Sage:
for name, sb in bigfatsbox.find('pre*').items():
    print(name, sb.nonlinearity())      # sb is an SBox object in Sage

all_8bit = bigfatsbox.load_bits(8)     # dict: key → SBox object
from bigfatsbox import b4
print(b4.present)                      # SBox([12, 5, 6, ...])

# Access YAML metadata in Sage (always returns plain Python dict)
data = bigfatsbox.yaml.aes
print(data['year'])                    # (2001,)
print(data['canonical_name'])          # ('Rijndael',)
print(data['note'])                    # additional remarks
```

### Raw YAML

Raw dictionary access is available via the `yaml` proxy. This is identical in Python and Sage and exposes all YAML fields including `canonical_name`, `year`, `note`, `trivium`, `origin`, `source`, `alias`/`aliases`/`reuse`, and `absolute_linear_uniformity`:

```python
data = bigfatsbox.yaml.aes         # Plain Python dictionary with all YAML fields
print(data['nonlinearity'])        # Prints 112
print(data['year'])                # Prints (2001,)
print(data['canonical_name'])      # Prints ('Rijndael',)
print(data['source'])              # Source URL string
data = bigfatsbox.yaml['AES']      # same, case-insensitive bracket access


all_names = bigfatsbox.yaml.all_names()    # sorted list of all entry keys (uppercase)
all_dicts = bigfatsbox.yaml.all_entries()  # full dict: key → raw dict
```

### Notes
1. Entries with an `alias` field are transparently resolved to the source entry in both Python and Sage:

    ```python
    print(bigfatsbox.rijndael)       # SBoxEntry('AES', ...) — resolves through alias
    print(bigfatsbox.kuznechik)      # SBoxEntry('KUZNYECHIK', ...) — alternate transliteration
    ```

2. The `yaml` proxy always returns raw dicts regardless of Sage mode, giving access to all YAML fields. List-valued fields are returned as tuples (e.g., `year`, `canonical_name`, `lookup_table`).

3. Python identifiers cannot start with a digit, so use `bigfatsbox.b3.sea` instead of `bigfatsbox.3bit.sea`. The `b` prefix is used throughout: `b3`, `b4`, `b5`, `b6`, `b7`, `b8`, `b9`.

4. `find('pattern')` and `bigfatsbox['pattern']` support `*` and `?` wildcards (case-insensitive) and always return a `dict`. For an exact lookup, `bigfatsbox['KEY']` behaves identically to `bigfatsbox.key`.

5. Wildcards are case-insensitive. `*` matches any sequence of characters; `?` matches a single character.