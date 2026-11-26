# Phase 178 R5 — Delta surjectivity public connection

Connect the unchanged R4 rule in `shared_expansion_provider` using the existing `extra_providers` registry. No new mathematical rule, GIVEN, renderer, or root-specific production path. R4 rule and tests must already be present, unchanged (committed or untracked).

Run `run.ps1 -DryRun` then `run.ps1` from the repository root. The complete revised shared function with imports and complete source are exported to the reported attempt directory. DryRun does not edit tracked files. Execution allows only the expected shared file modification; on failure it retains that modification and reports the error. Do not commit a failed attempt.

The audit captures one actual n=3,k=6 root search and checks ordinary public provider proposals, including multiple valid dimensions and invalid types. This does not assert that Delta surjectivity has been proved if it is not reached by the root search. R4 isolated tests and installer tests run without the pytest cache provider. No full pytest. The next stage addresses finite group cardinality and injectivity.
