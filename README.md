# Big-Fat-SBox-List

Public collection of Substituition Boxes (SBoxes for short) used in cryptography

## Organization

- YAML files containing details about multiple SBoxes, properties, cryptographic properties, historical notes etc.

- Files are written by input size (each input size in bits gets a new file) and bijectivity (non-bijective SBoxes are moved to other files). Additionally, due to large number of 4-bit SBoxes, those are split into 2 files based on whether or not those are used in a cipher ([4bit_cipher.yaml](4bit_cipher.yaml)) or just exemplary/representative ([4bit_nocipher.yaml](4bit_nocipher.yaml)).

- Entries within each YAML file are in alphabetical order by key.

## Naming Convention

- Entry keys use an all-uppercase Latin with/without dot convention (e.g., `PRESENT` as without dot; `MIDORI.SB0`, `JH.0` as with dot). Note that the cipher name preceeds the dot and the SBox name is after dot, or if there is no specific name to its SBox then only the cipher's name or some identifier (like `DILLON`) is used.

- `canonical_name` field records the exact name as it appears in the original paper to preserve information (related to casing, non-Latin characters, subscript). 

- Lowercase `v` indicates a version number and is not part of the cipher name (e.g., `PRINCEv2`).

- `_Inv` at the end indicates that it is the inverse of another SBox which is already included (e.g., `ARIA.S2_Inv`).


## Files

### Bijective SBoxes

| File | # Entry | Bit Mapping | 
|:------|:-------:|-------------:|
| [3bit.yaml](3bit.yaml) | 6 | 3 → 3 |
| [4bit_cipher.yaml](4bit_cipher.yaml) | 146 | 4 → 4 | 
| [4bit_nocipher.yaml](4bit_nocipher.yaml) | 354 | 4 → 4 |
| [5bit.yaml](5bit.yaml) | 16 | 5 → 5 |
| [6bit.yaml](6bit.yaml) | 5 | 6 → 6 |
| [7bit.yaml](7bit.yaml) | 2 | 7 → 7 |
| [8bit.yaml](8bit.yaml) | 68 | 8 → 8 |

### Non-Bijective SBoxes

| File | # Entry | Bit Mapping |
|:------|:-------:|-------------:|
| [nonbijective4bit.yaml](nonbijective4bit.yaml) | 1 | 4 → 2 |
| [nonbijective6bit.yaml](nonbijective6bit.yaml) | 8 | 6 → 4 |

## Entry Format

Each YAML entry has the following fields in order (mandatory fields are marked with `*`):

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name` | list | Name as written in the original paper (preserving case, non-Latin characters, subscripts, hyphens). Always a list. |
| `output_bits`* | int | Output bit size for non-bijective SBoxes |
| `lut`* | list | Look-up table (substitution values) |
| `algebraic_degree`* | int | Maximum algebraic degree |
| `nonlinearity`* | int | Non-linearity |
| `differential_uniformity`* | int | Differential uniformity |
| `absolute_linear_uniformity`* | int | Maximum absolute value in the linear approximation table (excluding row 0 and column 0) |
| `involution`* | bool | True iff S(S(x)) = x for all x |
| `fixed_point`* | list | Values where S(x) = x (`[]` for no fixed point) |
| `year` | list | Collection of significant publication years (competition submission, journal publication, standard approval) etc. |
| `cipher`* | bool | True if used in a cipher, false otherwise (e.g., for research or exemplary SBoxes) |
| `source` | str | URL of code or other resources (mainly [PEIGEN SBox collection](https://github.com/peigen-sboxes/PEIGEN/tree/master/EvaluationResults/Sect5.1_CryptographicProperties), [Sage reference manual](https://github.com/sagemath/sage/blob/develop/src/sage/crypto/sboxes.py)) whence some information is mined |
| `origin` | str | Citation of the original publication |
| `aliases` | list | Ciphers that have rebranded this SBox under a new name |
| `alias` | list | That cipher whose SBox is rebranded by current cipher |
| `reuse` | list | Ciphers that reuse this SBox under its original name |
| `note` | str | Remarks such as government-body origin, competition/standardization status, related cryptographic properties or information |
| `fun_fact` | str | Relevant lesser-known trivia (not directly related to the cipher) |


### Reuse and Rebranding (Alias)

Three fields handle inter-cipher SBox relationships:

- **`reuse`** (list in main entry): Ciphers that explicitly use this SBox under its original name (i.e., without giving a new name). No separate entry is created for the reusing cipher. For example, ZORRO explicitly uses the AES SBox and credits it as such; ZORRO appears in AES's `reuse` list.

- **`alias`** (field in a secondary entry, replacing `lut`): A cipher that takes another cipher's SBox and renames it as its own gets a standalone entry with `alias: SOURCE_CIPHER`. This entry can carry `year`, `canonical_name` and `note` (if available), but cannot carry `lut` (as `lut` is to be read from its `alias`).

- **`aliases`** (list in main entry): The inverse of `alias`. Lists all ciphers whose own entries have `alias:` pointing to this main entry. In other words, ciphers that have rebranded this SBox under a new name.


### Notes

1. Our convention — uppercase Latin characters with only dot allowed — enforces uniformity and ASCII searchability, but it destroys the original typographic formatting used by the designers, such as mixed case (e.g., "Midori"), non-Latin characters (like Cyrillic π; Greek σ, ν), subscript notation (e.g., Sb₀). 

2. `canonical_name` — which is applicable only when `cipher` is true, and used to preserve the original formatting as intended by the cipher's designer(s) — is a list. For a cipher with a single SBox, it is a one-element list (e.g., `["GIFT"]`). When a cipher has multiple SBoxes distinguished by a subscript or letter (e.g., `S₀`, `π₁`), it is a two-element list `["CipherName", "SBoxName"]` where the first element is the cipher's canonical name and the second is the specific SBox sub-name (e.g., `["CLEFIA", "S₁"]`).

2. For non-bijective SBoxes, `output_bits` is mandatory, but it is omitted for bijective SBoxes. 

3. `alias` (a secondary entry's field pointing to one source) and `aliases` (the main entry's list of ciphers that rebranded it) are not the singular and plural of the same concept. `reuse` is not linked with `alias` or `aliases` (both `alias` and `aliases` deal with cases where an SBox ) 

4. `year` field is a list of significant publication years (e.g., competition submission, journal publication, standard approval). Single-year entries still use list format: `year: [2019]`. Multi-year entries carry inline comments explaining each year (e.g., `year: [2014, 2023]  # CAESAR submission (2014); NIST LWC winner (2023)`). When an ePrint preprint differs from the published venue year, the venue year is used.

5. The dot notation is not restricted to ciphers; non-cipher research entries may also use it (e.g., `APN.1` where APN is a class and 1 is an index, not a cipher–SBox pair).


