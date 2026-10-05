# Phase 159-R1-2 closure repair4

## Scope

Test-only packaging repair.

Repair3 failed before writing any repository file because the generated
apply script encoded the test source incorrectly. Repair2 production code
remains unchanged.

This package stores the complete test source as Base64 in the apply script,
decodes it, syntax-checks it, backs up the existing test file, and then
replaces that test file.

## Run

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_2_closure_repair4_test_payload_fix" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_2_closure_repair4_test_payload_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_2_closure_repair4_test_payload_fix\run_phase159_r1_2_closure_repair4.ps1"
```

The full pytest suite is intentionally not run.
