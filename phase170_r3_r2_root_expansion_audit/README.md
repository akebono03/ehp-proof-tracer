# Phase 170 R3-R2 — Root Expansion Audit

This read-only package examines the five `SEARCH_FAILED` groups from Phase 170 R1.
It requires the completed R1, R2 and R3-R1 reports, and reuses the reviewed R3-R1
preflight checks. No checked-in source, test, database, Git index or prior report is
changed. New output is written only under `%LOCALAPPDATA%/EHPProofTracerRecovery`.

It does **not** rerun recursive proof search. For each failed group's root typed
Goal, it invokes the existing production backward-expansion provider after the
same source-screening and context normalization used by production search. It
reports proposed inference rules, subgoal types, and whether subgoals are
already present as exact screened GIVEN statements.

A proposal is not a verified proof. An unproved direct subgoal might be proved
recursively; an empty proposal list does not prove that a mathematical theorem
is absent. The audit does not claim to certify the correctness of Toda's source.

## Run in Windows PowerShell

From the repository root, extract the ZIP into `.` and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r2_root_expansion_audit\run.ps1"
```

Optional: `-R3Report 'C:\path\to\phase170_r3_r1_...\audit.json'`.

Only the package's small focused test set is run. The full pytest suite is
reserved for the end of Phase 170.
