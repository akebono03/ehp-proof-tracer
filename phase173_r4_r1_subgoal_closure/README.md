# Phase 173 R4-R1 — Subgoal Closure Audit

A read-only package to test all four typed premises of the proposed Toda (5.6) decomposition under the same citation-screened publication context. It does not change any production code or Git history. A source archive entry is explicitly **not** a proof.

Run `run.ps1 -DryRun` and then `run.ps1` from the extracted package. The runner executes only its focused test module with pytest caching disabled. It writes audit results to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_subgoal_closure\audit.json`.

Expected repository: `akebono03/ehp-proof-tracer`, branch `develop`, descendant of reviewed commit `84f7c3f8`. Every relevant production source blob must match the reviewed content. A new HEAD containing changes to the reviewed sources fails closed.

A PASS means the audit ran, not that a group presentation was proved. The `COMPLETE_ROOT_CERTIFIED` field must be evaluated separately. No full test suite is executed.
