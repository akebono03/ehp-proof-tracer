# Phase 163 R4-R44 Assertion crosswalk

- TeX environments: 108
- Existing references: 23
- Existing assertions: 67
- New reference candidates: 66
- Unresolved locators: 19
- Existing component positions present: 36
- Existing component positions unknown: 31
- Existing assertion ↔ TeX span semantic equivalence is NOT verified.
- All TeX registration/structured/source-verified flags remain false.
- No registration, ID issuance, proof-search connection, or project source edits.

## Assertion count by reference

| Reference ID | Assertion count |
|---|---:|
| `toda:(4.5)` | 1 |
| `toda:(5.1)` | 6 |
| `toda:(5.13)` | 3 |
| `toda:(5.2)` | 1 |
| `toda:(5.3)` | 4 |
| `toda:(5.5)` | 1 |
| `toda:(5.7)` | 1 |
| `toda:(5.8)` | 1 |
| `toda:Lemma 5.13` | 1 |
| `toda:Lemma 5.14` | 3 |
| `toda:Lemma 5.4` | 1 |
| `toda:Lemma 5.7` | 2 |
| `toda:Proposition 2.2` | 1 |
| `toda:Proposition 2.5` | 1 |
| `toda:Proposition 3.1` | 1 |
| `toda:Proposition 4.4` | 1 |
| `toda:Proposition 5.1` | 4 |
| `toda:Proposition 5.11` | 4 |
| `toda:Proposition 5.15` | 8 |
| `toda:Proposition 5.3` | 4 |
| `toda:Proposition 5.6` | 5 |
| `toda:Proposition 5.8` | 6 |
| `toda:Proposition 5.9` | 7 |

## Pending decisions

1. Verify each existing component against the exact TeX span; do not infer correspondence from its name.
2. Treat a whole TeX environment as a reference unit, separate from any component assertions.
3. Preserve unnumbered and symbolic-label environments with chapter/source order; do not invent bibliographic numbering.
4. Review definitions outside standard TeX environments before claiming complete chapter registration.
