Phase 161: Type-depth priority & per-conclusion-type beam probe

Purpose: Diagnose bounded goal-directed type-closure search without prelisting
seven intermediate goals or naming seven inference-rule families.

Changes compared with phase161_backward_type_closure_budget_fix:
- Prioritize candidate rules by the backward type-closure depth of their conclusion.
- Limit retained (including initial) conclusions of any one concrete Statement class to four.
- Check the exact goal immediately when a rule produces it.
- Record cumulative type-cap rejections in per-round diagnostics.

Limitations:
- This is an experimental heuristic, not a complete proof search.
- The six-premise seed profile is still specified, and Relation provenance still
  uses an inference-rule name. The output must not be described as fully goal-only.
- Valid paths can be pruned by the per-type cap.
- Existing Production rules, repository and pytest tests are not modified.
- Full pytest suite is not run.

From the repository root:
  powershell -ExecutionPolicy Bypass -File .\phase161_backward_type_priority_probe\run_phase161_backward_type_closure.ps1

Output: phase161_backward_type_priority_probe.json
