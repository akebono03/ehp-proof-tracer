# Phase 155-R1 — Test inventory / classification audit

## Boundary

This audit performs static inventory only. It does not execute pytest, delete tests, change production code, or decide removals.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `8301520a7434f3836b1dbc7e8fa08a60c024225a`
- Test files: 843
- Test functions: 10292
- Exact normalized-AST duplicate groups: 93
- Non-current candidates requiring later review: 1618

## Primary classification

| category | test functions |
| --- | ---: |
| `current_contract` | 8674 |
| `historical_compatibility` | 319 |
| `audit_only` | 920 |
| `superseded_snapshot` | 1 |
| `duplicate_coverage` | 268 |
| `performance_heavy_integration` | 110 |

## Phase distribution

| phase | test functions |
| --- | ---: |
| `27` | 15 |
| `30` | 25 |
| `32` | 39 |
| `33` | 73 |
| `34` | 35 |
| `35` | 53 |
| `36` | 14 |
| `37` | 11 |
| `38` | 13 |
| `39` | 24 |
| `40` | 24 |
| `41` | 36 |
| `42` | 36 |
| `43` | 32 |
| `44` | 94 |
| `45` | 103 |
| `46` | 83 |
| `47` | 134 |
| `48` | 134 |
| `49` | 146 |
| `50` | 150 |
| `52` | 24 |
| `53` | 38 |
| `54` | 35 |
| `55` | 40 |
| `56` | 66 |
| `57` | 87 |
| `58` | 62 |
| `59` | 118 |
| `60` | 157 |
| `61` | 102 |
| `62` | 114 |
| `63` | 107 |
| `65` | 184 |
| `66` | 129 |
| `67` | 132 |
| `68` | 241 |
| `69` | 79 |
| `70` | 330 |
| `71` | 134 |
| `72` | 238 |
| `73` | 262 |
| `74` | 223 |
| `75` | 404 |
| `76` | 123 |
| `77` | 141 |
| `78` | 183 |
| `79` | 27 |
| `80` | 53 |
| `81` | 43 |
| `82` | 84 |
| `83` | 62 |
| `84` | 74 |
| `85` | 74 |
| `86` | 55 |
| `87` | 37 |
| `88` | 47 |
| `90` | 32 |
| `91` | 19 |
| `92` | 49 |
| `93` | 66 |
| `94` | 44 |
| `95` | 106 |
| `96` | 158 |
| `97` | 32 |
| `98` | 34 |
| `99` | 173 |
| `100` | 145 |
| `101` | 32 |
| `102` | 75 |
| `103` | 397 |
| `104` | 84 |
| `105` | 65 |
| `106` | 3 |
| `107` | 62 |
| `108` | 66 |
| `109` | 127 |
| `110` | 52 |
| `111` | 18 |
| `113` | 5 |
| `114` | 16 |
| `115` | 14 |
| `117` | 14 |
| `118` | 40 |
| `120` | 13 |
| `121` | 13 |
| `122` | 15 |
| `123` | 17 |
| `124` | 5 |
| `125` | 9 |
| `126` | 3 |
| `128` | 10 |
| `129` | 12 |
| `130` | 40 |
| `131` | 23 |
| `132` | 54 |
| `133` | 10 |
| `134` | 75 |
| `135` | 12 |
| `136` | 4 |
| `137` | 3 |
| `141` | 39 |
| `142` | 11 |
| `143` | 351 |
| `144` | 342 |
| `145` | 5 |
| `146` | 3 |
| `147` | 5 |
| `148` | 53 |
| `149` | 5 |
| `150` | 53 |
| `153` | 70 |
| `154` | 44 |
| `core` | 1482 |

## Classification policy

- A Phase number alone never makes a test historical.
- `superseded_snapshot` requires an explicit snapshot/fixed-count signal plus a numeric equality assertion.
- `duplicate_coverage` requires an exact normalized AST duplicate across test functions.
- `performance_heavy_integration` requires a heavy-suite name signal plus loop/integration evidence.
- `audit_only` and `historical_compatibility` are selected only from explicit naming signals.
- Everything else remains conservatively in `current_contract` until R2/R3 review.

## R1 conclusion

R1 identifies candidates; it does not authorize deletion or expectation changes. R2 should inspect stale expectations, and R3 should review exact duplicates/superseded snapshots against the current contract.
