# Big-Fat-SBox-List

Public collection of SBoxes used in cryptography, organized in YAML files by input size and bijectivity.

## Naming Conventions

Entry keys use an all-uppercase Latin-with-underscore scheme (e.g., `PRESENT`, `MIDORI_SB0`, `JH_0`). This convention enforces uniformity and ASCII searchability, but it destroys the original typographic formatting used by the designers, such as mixed case (Midori), non-Latin characters (Cyrillic π, Greek σ, ν), subscript notation (Sb₀), or hyphens. The `canonical_name` field records the exact name as it appears in the original paper to preserve this information.

Additional conventions:

- Lowercase `v` indicates a version number and is not part of the cipher name (e.g., `PRINCEv2`, `QARMAv2_SIGMA`).
- The `year` field records the first peer-reviewed publication year. When an ePrint preprint differs from the published venue year, the venue year is used, with a clarifying comment in the YAML.

## Files

**Bijective SBoxes**:

| File | Entries |
|------|:-------:|
| `3bit.yaml` | 6 |
| `4bit.yaml` | 192 |
| `5bit.yaml` | 14 |
| `6bit.yaml` | 5 |
| `7bit.yaml` | 2 |
| `8bit.yaml` | 61 |

**Non-bijective SBoxes**:

| File | Entries | Bit Mapping |
|------|:-------:|-------------|
| `nonbijective4bit.yaml` | 1 | 4→2 |
| `nonbijective6bit.yaml` | 8 | 6→4 |

## Entry Format

Each YAML entry has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name` | str or list | Name as written in the original paper (preserving case, non-Latin characters, subscripts, hyphens). When a cipher contains multiple SBoxes distinguished by a subscript or letter (e.g., `S₀`, `π₁`), this is a two-element list `["CipherName", "SBoxName"]` where the first element is the cipher's canonical name and the second is the specific SBox sub-name. When the cipher name itself is the canonical SBox name, this is a plain string (e.g., `"GIFT"`). |
| `lut` | list | Lookup table (substitution values) |
| `algebraic_degree` | int | Maximum algebraic degree of Boolean component functions |
| `nonlinearity` | int | Nonlinearity; minimum Hamming distance to affine functions |
| `differential_uniformity` | int | Differential uniformity |
| `involution` | bool | Whether S(S(x)) = x for all x |
| `fixed_point` | list/null | Values where S(x) = x, or null if none |
| `absolute_linear_uniformity` | int | Maximum absolute value in the linear approximation table (excluding row 0 and column 0) |
| `year` | int | Year of first peer-reviewed publication |
| `cipher` | bool | `true` if used in a cipher; `false` for research or exemplary SBoxes |
| `source` | str | URL to PEIGEN or other dataset reference |
| `origin` | str | Full citation of the original publication |
| `aliases` | list | Ciphers that have rebranded this SBox under a new name (see below) |
| `reuse` | list | Ciphers that explicitly reuse this SBox under its original name (see below) |
| `note` | str | Remarks (e.g., government-body origin, competition status, cryptographic properties) |

For **alias entries**, the entry has `alias: SOURCE_CIPHER` instead of `lut:`, indicating that the cipher rebranded another cipher's SBox as its own. For example, if a cipher takes the PRESENT SBox and calls it by a new name in their paper, that cipher gets its own entry with `alias: PRESENT`.

For **non-bijective SBoxes**, `input_bits` and `output_bits` are mandatory. The file name encodes only the input width, so `output_bits` must always be read from the entry.

## SBox Reuse and Rebranding

Three fields handle inter-cipher SBox relationships:

- **`reuse`** (list in main entry): Ciphers that explicitly use this SBox under its original name, without renaming it. No separate entry is created for the reusing cipher. For example, ZORRO explicitly uses the AES SBox and credits it as such; ZORRO appears in AES's `reuse` list.

- **`alias`** (field in a secondary entry, replacing `lut`): A cipher that takes another cipher's SBox and renames it as its own gets a standalone entry with `alias: SOURCE_CIPHER`. This entry also carries `year`, `canonical_name`, and `note`, but no `lut`.

- **`aliases`** (list in main entry): The inverse of `alias`. Lists all ciphers whose own entries have `alias:` pointing to this main entry. In other words, ciphers that have rebranded this SBox under a new name.

Note: `alias` (a secondary entry's field pointing to one source) and `aliases` (the main entry's list of ciphers that rebranded it) are not the singular and plural of the same concept.

