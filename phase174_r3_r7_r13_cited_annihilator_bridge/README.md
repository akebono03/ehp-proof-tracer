# Phase 174 R3-R7-R13 — Isolated Cited Toda (5.9) Bridge

This read-only audit registers the **general** Toda (5.9) ν–η annihilator in a fresh, in-memory, source-qualified `RegistryBridgeResult`. It screens the fixed general law through the project's existing Source-first path and derives the concrete instance with the existing R12 typed inference rule. The production source registry, default proof provider, rendered narrative, and target-group proof are **not modified**.

## Requirements

- Git branch `develop` and the reviewed GitHub HEAD. The script rejects unreviewed source changes.
- Previously completed R12 full audit JSON in `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r12\toda59_annihilator.json`.
- Python, pytest, PowerShell, and the repository's normal dependencies.
- Extract `R13.zip` directly into the repository root.

## Execute

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\R13.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r13_cited_annihilator_bridge\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R13 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r13_cited_annihilator_bridge\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R13 audit failed" }
git status -sb
```

Focused tests run in separate pytest processes to avoid identical test-module name collisions. There is no full test suite run within this step.

The full audit report is stored under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r13\cited_annihilator_bridge.json`.

## Proof boundary

The adopted Toda transcription is checked against the `(5.9)` manifest record and the source text. The manifest's publication position is **only adopted-source order**, not independently verified printed-edition order. The only new fixed assertion is the **general** relation `nu_n o eta_(n+3) = 0` for `n >= 6`, in an isolated bridge. The `n = 6` instance is an inference from this citation-qualified general statement; it is never directly registered as a GIVEN. No public proof completion is claimed.
