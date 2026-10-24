# EHP Proof Tracer — Phase 168 R3-41P7 residual math-validation audit

Audit-only inspection of the remaining mathematics-aware checks inside Typed Projection. **No repository application source files or existing tests are changed.**

## Run from the EHP Proof Tracer repository root (Windows PowerShell)

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p7_shape_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p7_shape_boundary_audit\run.ps1"
```

The runner records `output/audit.json` and `output/audit.md`, checks the complete proof/reference texts of three groups against the R3-41P6 captures, and executes a **focused set of tests only**. Logs and observed texts are bundled into `output/review_bundle.zip` even if the audit fails. The full pytest suite is not run.

## Scope

The audit compares these existing functions:

- `_stable_eta_renaming_shape` in the inference rule and in `project_stable_eta_notation_transition`.
- `prop42_exactness_indices` in proof-side exactness inference and in `typed_sentence`.

It also runs isolated **synthetic shape probes** for valid and malformed typed inputs, to identify which fail-closed checks would be lost by removing the validation calls. Synthetic probes are diagnostics, **not registered mathematical facts**.

## Outputs

- `output/audit.json`, `output/audit.md`: call evidence, source hashes, and findings
- `output/pi*_current.md`: public three-group outputs
- `output/pi*_fulltext.diff`: exact comparison to R3-41P6 captures
- `output/audit_stdout.log`, `output/audit_stderr.log`: audit logs
- `output/pytest_focused_stdout.log`, `output/pytest_focused_stderr.log`: focused tests
- `output/review_bundle.zip`: compact review package

A nonzero exit code means an audit check or focused test needs review. Source hashes before and after are compared to detect accidental application changes.
