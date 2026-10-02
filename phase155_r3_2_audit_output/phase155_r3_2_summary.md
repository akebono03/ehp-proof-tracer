# Phase 155-R3-2 — candidate coverage verification

## Boundary

R3-2 verifies the R3-1 candidate pairs by focused pytest execution and source/dependency comparison.
It does not delete, move, rename, or rewrite existing tests.
It does not modify production code.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `9e985588f66f8f5ec80eb49aecd8177e61afd66a`
- Candidate pairs: 332
- Unique candidate tests executed: 440
- Focused pytest exit code: 1
- Collection errors: 0

## Decisions

| decision | pairs |
| --- | ---: |
| `removable_duplicate` | 159 |
| `retain_independent` | 123 |
| `historical_keep` | 43 |
| `needs_review` | 7 |

## Candidate category × decision

| candidate category | removable | retain | historical | review |
| --- | ---: | ---: | ---: | ---: |
| `exact_duplicate_candidate` | 69 | 80 | 22 | 4 |
| `semantic_duplicate_candidate` | 0 | 0 | 0 | 0 |
| `superseded_candidate` | 90 | 43 | 21 | 3 |

## Focused pytest outcomes

| outcome | tests |
| --- | ---: |
| `failed` | 2 |
| `missing` | 11 |
| `passed` | 427 |

## Verification rule

- `removable_duplicate`: both tests pass current behavior and source-backed dependency context proves full duplication/replacement.
- `retain_independent`: candidate similarity exists, but helper/import/constant dependency context or coverage does not prove replacement.
- `historical_keep`: the test explicitly identifies legacy/historical/compatibility intent.
- `needs_review`: execution or source evidence is incomplete.

For exact duplicates, normalized test bodies and direct module-level dependency fingerprints must match.
For superseded candidates, the newer semantic assertion contract must contain the older contract and direct dependency fingerprints must also match.

## Important boundary

A `removable_duplicate` decision authorizes the pair as a removal candidate for R3-3 only.
R3-2 itself deletes zero tests.
Repository-wide pytest remains deferred until the end of Phase 155.
