# Phase 172 R1: Read-only Proof Display Audit

This package audits the **actual** completed proof of `pi_6^3` using the current model-backed public presentation route. It does not modify any production source, existing test, registered mathematical fact, ProofStep, or citation. It does not run the full test suite.

## Prerequisites

- Run on Windows, in the `develop` branch of `akebono03/ehp-proof-tracer`.
- Git and the project's usual Python environment must be available.
- The reviewed source files must match the GitHub `develop` content recorded in `audit.py`. Newer unrelated commits are accepted if those content hashes remain the same.
- A reachable `origin/develop` must match the local `HEAD`; if the remote is unreachable, the audit reports this and continues with the strict content checks. It will never fetch, pull, reset, or switch branches.

## Run

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R1_AUDIT_ONLY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r1_renderer_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r1_renderer_audit\run.ps1"
```

To run three existing focused test files in isolated pytest processes:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r1_renderer_audit\run.ps1" -RunFocusedTests
```

To run only the four package-level diagnosis tests, execute:

```powershell
python -B -m pytest -q -p no:cacheprovider .\phase172_r1_renderer_audit\tests\test_audit.py
```

The run writes `audit.json`, `web_narrative.md`, `proof_steps.json`, `references.json`, `line_alignment.json`, `web_rendered_lines.json`, and `AUDIT_FINDINGS_JA.md` into a timestamped directory under `%LOCALAPPDATA%\EHPProofTracerRecovery\`. No output is written into the source repository except the extracted package itself.

The line-to-ProofStep alignment is explicitly a **candidate** matching diagnostic. Compound narrative sentences, verified summaries, or equal TeX statements may depend on more than one ProofStep. No mathematical or display change is proposed by this audit.
