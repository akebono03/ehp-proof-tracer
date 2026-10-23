# Phase 168 Frozen Narrative Baselines

This package preserves the actual historical text of three proofs produced by the earlier shared renderer, as observed in `akebono03/ehp-proof-tracer` commit `c250a3fe7be0e569af58faecfdb6556d6c090555`, `phase167_r4_4_order_audit_results/`.

Use these texts as an immutable quality baseline for the **new** Proof Narrative Model renderer. Preserve their mathematical reasoning and sequence, not their old citation numbering or known textual defects. All definitive References must be generated from the new model and matched to in-body citations. Do not fall back to the old renderer or hardcode proof text per group.

See `BASELINE_POLICY.md` for the binding implementation policy. Running `run.ps1` copies the snapshot under the project root; it refuses to overwrite changed files and does not run tests or alter production code.
