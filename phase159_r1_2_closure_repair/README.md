# Phase 159-R1-2 closure repair

## Scope

This package makes only the two agreed closure fixes:

1. suppress `## 使用する結果` when its body is empty;
2. preserve the visible `suspension isomorphism => suspension injectivity`
   dependency when that direct dependency exists in the proof graph.

It does not change reference selection policy, proof rules, group data, or
Phase 159-R1-3 behavior.

## Run

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_2_closure_repair" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_2_closure_repair.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_2_closure_repair\run_phase159_r1_2_closure_repair.ps1"
```

The runner uses focused and related regression tests only. It does not run
the full pytest suite.
