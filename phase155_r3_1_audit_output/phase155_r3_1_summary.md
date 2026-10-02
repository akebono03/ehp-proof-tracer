# Phase 155-R3-1 — duplicate / superseded candidate audit

## Boundary

This is a conservative static candidate audit. It does not delete, rename, move, or rewrite any existing test.
A candidate pair is not proof that the older test should be removed.
Phase number alone is never used as evidence of redundancy.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `9f88c9fa72dc50820d487acfef2e9f28af0f72df`
- Source-level test functions scanned: 10292
- Candidate pairs: 332
- Files touched by candidate pairs: 198

## Test-level primary categories

| category | tests |
| --- | ---: |
| `exact_duplicate_candidate` | 245 |
| `semantic_duplicate_candidate` | 0 |
| `historical_compatibility` | 269 |
| `independently_valuable` | 9778 |

## Candidate-pair categories

| category | pairs |
| --- | ---: |
| `exact_duplicate_candidate` | 175 |
| `semantic_duplicate_candidate` | 0 |
| `superseded_candidate` | 157 |

## Decision rule

- `exact_duplicate_candidate`: normalized function AST is identical after ignoring test function name/decorators.
- `semantic_duplicate_candidate`: normalized AST becomes identical after Japanese/ASCII punctuation normalization.
- `superseded_candidate`: a later-phase test uses the same nontrivial call surface and contains every semantic assertion atom of the older test.
- `independently_valuable`: no conservative duplicate proof was found.
- `historical_compatibility`: the test explicitly identifies legacy/historical/compatibility intent in its name.

## Important limitation

Helper functions, fixtures, parametrization semantics, negative assertions, fixture scope, setup cost, and human-readable intent can make two similar tests independently valuable.
Therefore every candidate has `deletion_authorized=false`.
R3-2 must read candidate source and execute the candidate pair before any removal decision.

## R3-1 completion gate

R3-1 is complete when the inventory and pair CSVs are generated and all candidate pairs remain non-destructive.
No repository-wide pytest is run in R3-1.
