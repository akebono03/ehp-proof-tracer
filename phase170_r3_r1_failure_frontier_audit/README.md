# Phase 170 R3-R1 — Failure Frontier Audit

This is an **AUDIT_ONLY** diagnostic package. It combines the recorded R1
backward-search outcomes with the recorded R2 database conversion results. For
the five failed target groups it independently inspects the current typed goal
selector, citing assertion resolution and source eligibility screening.

It **does not rerun backward search**, fabricate a proof, change any project
source or test, execute the full test suite, or modify the Git index. Only new
JSON/Markdown reports are written under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

The five targets are pi_6^3, pi_7^4, pi_8^5, pi_8^4 and pi_9^5. The
`SOURCE_ORDER_OR_CITATION_DIAGNOSTIC` label is a preliminary R2 classification
based on text diagnostics; it does not establish a violation of publication
precedence or the absence of a mathematical theorem.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r1_failure_frontier_audit\run.ps1"
```

`run.ps1` automatically discovers the most recent
`phase170_r2_head_sync_r1_*/audit.json`. Supply `-R2Report` to select a report
explicitly. The complete report is saved as `audit.json` and `audit.md` in a
new timestamped recovery folder. The script refuses an unreviewed branch, a
production-file change, an uncommitted database edit, an inconsistent report,
or an output overwrite. Later commits containing only newly added R2 audit
artifacts can be inspected without weakening the code-content checks.

The exit code certifies the audit execution, not the existence of missing
inference rules or the mathematical validity of a proposed derivation.
