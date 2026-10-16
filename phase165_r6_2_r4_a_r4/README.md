# Phase 165 R6-2 R4-A-R4

Read-only typed-goal applicability audit. Run `run.ps1` from the repository root in PowerShell. Python 3.10 or newer is supported.

The audit collects registered assertion contents from `build_shared_typed_bridge()` and tries R8's symbolic inverse provider and the R57-R26 generic backward provider for each factory that has a conclusion pattern and premises. The tool does not invent goals, add references, certify proofs, or change production files. By default, the first 250 distinct registered assertions are tested; truncation is clearly recorded. Outputs are in `reports/goal_applicability.json` and `.md`.

An emitted `GoalExpansion` is a proposal, not a proof. This is not an exhaustive audit of all providers or all possible goals. Any registry build failure is reported as INCOMPLETE and the script exits nonzero. Full pytest is not run.
