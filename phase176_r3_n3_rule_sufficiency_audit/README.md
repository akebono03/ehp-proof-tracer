# EHP Proof Tracer — Phase 176 R3

This package performs a **read-only rule-sufficiency audit** for the registered group target `(n,k)=(3,5)`. It records the exact outstanding typed goals, accepted proof steps, relevant positioned-source registrations, and the number and shape of unverified proposals returned by the existing shared provider.

It **does not** certify a candidate expansion as a proof, register a source, add a mathematical inference, modify shared code, or complete the group proof. The four known Phase 174 historical Source Guard failures remain unresolved. The complete pytest suite is not run.

From the repository root, extract the ZIP, run `phase176_r3_n3_rule_sufficiency_audit\run.ps1 -DryRun`, then run the same script without `-DryRun`. Inspect `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3_n3_rule_sufficiency_audit\report.json`. Only the local audit folder under `%LOCALAPPDATA%` is written at runtime.

If the current checkout has diverged from the reviewed Phase 176 R2 commit, the audit stops for review. This is a provenance check, not a request to reset, pull, or overwrite local changes.
