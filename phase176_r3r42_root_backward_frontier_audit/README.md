# Phase 176 R3R42 — Root Backward Frontier Audit

Read-only audit of the actual Web proof query `(n, k) = (3, 5)` at the reviewed develop baseline `7cbf3edfa0de21a24eb249637e1e99127a176297` (or a clean descendant).

Run `run.ps1 -DryRun` to check the source baseline and `run.ps1` to execute the canonical Web narrative query and the focused audit tests. The script requires a clean tracked worktree on `develop`. Untracked audit files are allowed. It performs no Git write operations, no source rewrites, and no proof registration.

The audit observes the actual provider calls, exact candidate order and subgoals, root gate inputs and outputs, accepted steps, unresolved goals, and Web view. It then checks selected independent goal candidates in the same screened context, using fresh shared providers. Independent probes are not evidence that the public root traversal visited or proved those goals. Neither observation nor probe introduces a mathematical rule, source or GIVEN step.

The report is saved under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r42_root_backward_frontier_audit/report.json` (temporary-directory fallback if LOCALAPPDATA is unavailable). A PASS means the frontier was recorded, not that the group was proved.
