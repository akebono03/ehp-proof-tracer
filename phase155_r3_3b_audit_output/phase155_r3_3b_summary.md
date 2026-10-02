# Phase 155-R3-3B — deletion-candidate file/dependency safety audit

## Input

- Git HEAD: `41d7811065a52eff216c333031cc1c02c3a35457`
- Deletion candidate functions: 161
- Candidate files: 71

## Function safety

- Safe function deletions: 161
- Blocked/unresolved function deletions: 0

| function status | count |
| --- | ---: |
| `safe_function_deletion` | 161 |
| `blocked_external_function_reference` | 0 |
| `missing_candidate_function` | 0 |
| `candidate_file_parse_error` | 0 |

## File safety

- Whole-file deletion eligible: 5
- Function-only files: 66
- Unresolved files: 0

| file status | count |
| --- | ---: |
| `safe_whole_file_deletion` | 5 |
| `function_only_retained_tests_or_symbols` | 65 |
| `blocked_external_module_import` | 1 |
| `unresolved_file_safety` | 0 |

## Safety interpretation

A candidate function is not approved when another Python module imports/references that test function directly.

A whole file is approved only when every top-level test function is a deletion candidate and no other Python module imports the module or any symbol from it.

Files containing retained tests or externally imported helpers/constants remain function-only deletion targets.

R3-3B performs no deletion. R3-3C may modify only the rows marked safe by this audit.

Repository-wide pytest remains deferred until Phase 155 closure.
