# Phase 155-R3-2F-r1 — verification repair and closure

## Changes

- Production code changes: none
- Existing test files changed: 2
- Existing test functions changed: 2
- `ast` import added to those two test files
- Hardcoding guard now inspects control-flow conditions instead of banning legitimate statement-field names across the whole module
- Parameterized pytest node IDs are aggregated by normalized base node ID
- Source fingerprints are recomputed from the current post-repair test files

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `f90d582242286a3067b5b8c52425770c0b4f2bed`
- Fresh focused pytest exit code: 0
- Unique candidate base tests: 440
- Candidate pairs: 332

## Runtime status

| status | base tests |
| --- | ---: |
| `passed` | 440 |

## Final pair decisions

| decision | pairs |
| --- | ---: |
| `removable_duplicate` | 164 |
| `retain_independent` | 125 |
| `historical_keep` | 43 |
| `needs_review` | 0 |

## Closure

- R3-2 closure condition satisfied: `true`
- Duplicate tests deleted in R3-2F-r1: 0
- Repository-wide pytest remains deferred until Phase 155 closure.
