# Phase 155-R2B — stale candidate verification

## Boundary

R2B executes only the unique test functions referenced by the R2 `stale_candidate_high` findings.
It does not execute the repository-wide test suite, rewrite production code, rewrite existing tests, or delete tests.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `0a3e5f5ffb1cd04469f5ee131b2b2fd202fcc886`
- R2 high findings: 83
- Unique focused tests executed: 61
- Focused pytest exit code: 1
- Collection errors: 0

## Verification classes

| class | findings |
| --- | ---: |
| `confirmed_stale` | 65 |
| `current_contract` | 13 |
| `historical_compatibility` | 0 |
| `false_positive` | 5 |
| `verification_inconclusive` | 0 |

## Focused pytest outcomes

| outcome | tests |
| --- | ---: |
| `failed` | 45 |
| `passed` | 16 |

## Contract-by-class matrix

| contract | confirmed stale | current contract | historical compatibility | false positive | inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ascii_prose_punctuation` | 65 | 5 | 0 | 0 | 0 |
| `no_internal_fallback_leakage` | 0 | 8 | 0 | 5 | 0 |

## R1 / R2 file coverage difference

- `tests/test_phase50_pi4_3_dependency_compatibility.py` — R1=False, R2=False, on_disk=True: Present on disk but absent from the R1 inventory; inspect R1 collection logic.

## Interpretation

- `confirmed_stale`: current code causes the selected test to fail with an assertion. This is evidence for an R2 repair candidate, not an instruction to delete the test.
- `current_contract`: the high static rule was over-broad; the test passes and is on the current Phase 153-154 contract boundary.
- `historical_compatibility`: the test passes and R1 intentionally classified it as compatibility coverage.
- `false_positive`: the static rule fired, but current behavior satisfies the test and it is not otherwise identified as a current-contract or compatibility test.
- `verification_inconclusive`: collection/setup/non-assertion failure or skip prevented proof of staleness.

## R2B completion gate

R2B is complete when every R2 high finding is mapped to a focused test outcome and only assertion-backed failures are carried forward as `confirmed_stale` repair candidates.
No existing test is deleted or rewritten in R2B.
