# Phase 168 R3-41P — Renderer Responsibility Boundary Audit

This package audits the boundary between proof validation and narrative rendering in EHP Proof Tracer.

It is **audit-only**: it does not patch the project's Python source files, change tests, register rules, or run the full pytest suite.

## Run on Windows PowerShell

From your EHP Proof Tracer repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p_boundary_audit\run.ps1"
```

`run.ps1` runs the audit and five existing focused test files plus one new audit-runner regression test.

To run an audit without pytest:

```powershell
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p_boundary_audit\run.ps1" `
  -SkipTests
```

## Outputs

Files under `phase168_r3_41p_boundary_audit/output/` (the review bundle is generated even when the Python audit reports a failure):

- `audit.md`, `audit.json`: static and dynamic findings, Git state, runtime validator calls, citation provenance
- `pi3_2_current.md`, `pi4_3_current.md`, `pi5_4_current.md`: complete renderer output (reference and proof)
- `pi*_reference.diff`, `pi*_proof.diff`: text diffs against available frozen baselines
- `audit_console.log`, `pytest_focused.log`: combined audit and focused pytest logs
- `audit_console_stdout.log`, `audit_console_stderr.log`: unmodified stdout/stderr files, including full tracebacks
- `pi*_audit_error.txt`: per-group complete traceback if any group fails
- `git_status_before.txt`, `git_status_after.txt`: source tree changes for manual inspection

If baseline files are absent, the audit marks comparisons unavailable instead of inventing results. Any failure is reported in `audit.json`.

## Scope

The audit checks common renderer/model/projection code and the cited tests, including dynamic call sites of the mathematical specialization validators. It distinguishes source-provenance consistency from proof correctness.

No program source files are added or replaced. The package creates only its own output files. The project's Python behavior may produce temporary non-source artifacts through existing utilities.

The full pytest suite is deliberately deferred until Phase 168 closes.

## R3-41P1 runner repair

`run.ps1` previously combined stderr into a PowerShell pipeline with `2>&1` while `$ErrorActionPreference = "Stop"`. On Windows PowerShell, the first Python error could stop the runner before it saved a full traceback or produced `review_bundle.zip`. The revised runner uses `Start-Process` with separate stdout/stderr redirection, reports exit codes, and packages diagnostic logs even if Python exits unsuccessfully.

The Python audit also catches failures **per group** and processes the other groups, retaining their findings rather than losing them to a top-level exception. It preserves the previous exit status semantics: audit failures return a nonzero code. It never claims an audit passed when it failed.

This patch replaces only the package's `audit.py` and `run.ps1`, adds a regression test under `tests/`, and updates this package README. No EHP proof generation or application modules are modified.
