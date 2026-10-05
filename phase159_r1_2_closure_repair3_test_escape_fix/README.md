# Phase 159-R1-2 closure repair3

## Scope

This is a test-only correction.

The previous focused test accidentally searched for two literal backslashes
before `pi` and `to`. The renderer correctly emits one LaTeX backslash.

Production code from repair2 is left unchanged.

## Run

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_2_closure_repair3_test_escape_fix" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_2_closure_repair3_test_escape_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_2_closure_repair3_test_escape_fix\run_phase159_r1_2_closure_repair3.ps1"
```

The full pytest suite is intentionally not run.
