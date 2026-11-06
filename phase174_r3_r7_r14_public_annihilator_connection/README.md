# Phase 174 R3-R7-R14 — Public Cited Annihilator Connection

This package adds the **general, cited Toda (5.9) annihilator** to the standard shared source bridge and connects the existing type-checked general specialization rule to the common backward expansion provider. It does not insert a concrete zero relation as a GIVEN, modify narrative rendering, or assert that the group proof is complete.

## Scope

The only existing tracked target is `phase165_r52_r9_shared_math.py`, within `build_shared_typed_bridge()` and `shared_expansion_provider()`. The patch makes two guarded insertions. Other files in this directory are new audit scripts, tests and documentation.

The prerequisite is a successful R13 full audit recorded at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r13\cited_annihilator_bridge.json`. The reviewed `develop` commit is `9a8a3e953fe7d3bc7d8d989188aef15525b3a414`; a single intervening commit containing only the R13 package is also accepted, provided all pinned sources match. No other commits or preexisting tracked edits are accepted.

## Run (PowerShell)

From the project root, expand `R14.zip` into the current directory, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r14_public_annihilator_connection\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R14 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r14_public_annihilator_connection\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R14 audit failed" }
git status -sb
git diff --stat
```

DryRun performs source verification and grouped focused pytest, without modifying tracked sources. It also generates `MODIFIED_FUNCTIONS_FULL_JA.md` containing complete replacement function bodies. The normal run repeats preflight and focused tests, applies the guarded patch, runs a focused public integration test and records the audit JSON. A backup of the original tracked source is saved outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r14\`. A failed post-patch test/audit triggers rollback.

## Completion criteria

The focused regression suites, source guard, cited general source admission, n=6 inference ancestry and public provider expansion must all pass. The audited result must preserve the target's unproved status. The complete repository pytest suite is reserved for the end of Phase 174.
