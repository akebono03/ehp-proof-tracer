# Phase 165 R57-R23: Typed Conclusion Unification

This package adds a shared, read-only conclusion unifier for explicit `InferenceRule.conclusion_pattern` declarations. It does not infer subgoals, discover candidate rules, or modify existing backward-search behavior.

## Install and test (Windows PowerShell)

Extract this ZIP in the root of the EHP Proof Tracer repository and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r57_r23_conclusion_unification\run.ps1
```

The script copies one new Python module into the repository root and runs seven focused pytest tests. No full test suite is run.

## Completion boundary

R23 checks typed goal-to-conclusion matching with nested dataclasses, tuples, repeated variables, and exact equality. R24 will address rule/candidate discovery, R25 will construct premises, and R26 will connect these to the shared backward-search engine. Builder-only rules are not invertible by this phase alone.
