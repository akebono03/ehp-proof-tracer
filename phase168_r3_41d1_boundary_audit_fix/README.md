# Phase 168 R3-41D1: Partial Proof Boundary Audit Fix

Read-only fix for audit-side section parsing. The common Narrative renderer uses `## 使用する結果` and `## 証明` for incomplete proof results, and unprefixed headings for complete results. This audit accepts both, isolates references from the preceding target and subsequent proof, and checks proof citation tags only within the proof section.

No project implementation files or mathematical proof rules are changed. A capture failure produces an audit report and a failing process exit code, rather than a misleading all-clear. Limited pytest only; the project-wide suite is reserved for the end of Phase 168.

Run `run.ps1` after extracting this directory into the repository root. Outputs are placed in `output/`, including `audit.json`, `audit.md`, and `review_bundle.zip`.
