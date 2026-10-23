# Phase 168 R3-33 — Frozen Narrative Baseline Comparison

This is a **read-only audit**. It compares the current model-backed narrative for π₃², π₄³ and π₅⁴ with the three preserved historical baseline texts. It checks named mathematical milestones and their relative order, not historical Reference numbering. The frozen originals are bundled unchanged.

The comparison uses deliberately conservative string matching. `MISSING_OR_DIFFERENT_EXPRESSION` includes harmless notation differences as well as genuinely absent sentences, so the report requires human review. `OUT_OF_ORDER_OR_DUPLICATE` can include repeated generic words such as “is an isomorphism.” The tests verify the audit algorithm, **not** proof correctness.

Extract this folder at the repository root, then in PowerShell run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_33_baseline_comparison\run.ps1
```

Output files: `output/baseline_comparison.json`, `output/baseline_comparison.md`, and the three current narrative `.txt` files. The original frozen texts stay in `baselines/`. No production files are changed. Full pytest is deferred until the end of Phase 168.
