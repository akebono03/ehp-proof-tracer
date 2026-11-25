# Phase 177 R7 — Left Composition Reuse Audit

Read-only audit of the existing equality-preservation rule after R6. Reviewed develop HEAD: `59d7a79aa632dbc5d1999b8478361cebd77df540` (177-6). No existing source file is edited. The script requires that commit locally and in `origin/develop`, with clean tracked files; untracked audit files are permitted.

The exact (5.11) composition identity and five additional typed targets are checked. Each premise is reconstructed independently by the normal source-first DFS. The existing left-composition rule is replayed with that actual proof. A separate public-search attempt uses no extra provider. The report distinguishes these results, including an independent probe using the provider captured from the real root search. Independent probes are not evidence accepted by the actual root proof. Arbitrary typed left factors in the additional cases are formal elements; no assertion about their order or nonzero status is made.

`PUBLIC_COMPOSITION_PROVED` means public DFS produced an inferred exact target. `PUBLIC_BACKWARD_CONNECTION_FRONTIER` means the existing rule was replayed but an exact public candidate was absent and the public target was unresolved. `PUBLIC_CANDIDATE_REPLAY_FRONTIER` means an exact candidate was present but the public target remained unresolved. An R6 premise regression or failure to replay the existing typed rule fails the audit. The PASS gate certifies a completed observation, not completion of every target.

Run `run.ps1 -DryRun` and then `run.ps1`. Reports are written to `%LOCALAPPDATA%/EHPProofTracerAudit/phase177_r7_left_composition_reuse_audit`. Focused tests only. No new mathematical rules, GIVENs, registry updates, Delta provider connection, or renderer changes.
