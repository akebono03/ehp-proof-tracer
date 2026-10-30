# Phase 171 R18: Cardinality Premise Audit

This read-only package examines why the public search cannot reconstruct the cardinality-four statement for $\pi_6(S^3)$ even though R17 independently established the EHP short exact sequence.

It checks the three exact subgoals proposed by the existing `finite middle-group cardinality from short exact sequence` rule: the previous $\pi_5(S^2)$ order-two presentation, the EHP short exact sequence, and the $\pi_6(S^5)$ order-two presentation. It reconstructs each subgoal separately with the canonical resolver in both the independent screened context and the real public context. Where all three subgoals are proved, it validates their combination with the original inference matcher. Independently derived steps are **never** passed back into production search; no source or proof is registered.

## Prerequisites

- The `develop` branch, with the exact reviewed R11 provider blob.
- R17 audit package and its successful `output/audit.json`.
- R16 package and its original prerequisites.
- Python and pytest installed in the existing repository environment.

## Execution

Unpack `EHP_Phase171_R2J_R4_R9_R18_CARDINALITY_PREMISES_AUDIT_ONLY.zip` into the repository root. From Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r18_cardinality_premise_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r18_cardinality_premise_audit\run.ps1"
```

Seven focused tests are run with the pytest cache provider disabled; the full suite is not run. The report is written to `output/audit.json`. The output includes the three premise statuses, inference matcher count, cardinality standalone status and an evidence-based classification.

No production implementation, mathematical rule, citation policy, proof trust boundary, or `GIVEN` leaf is changed. This phase does not claim the target group is complete.
