# Phase 159-R1-2 closure repair5

## Purpose

Restore the existing eta-family canonical display contract after Phase 158
public Narrative reconstruction.

The existing `_phase136_compact_eta_powers()` function already defines the
canonical display replacements. This repair applies that existing function to
the final Phase 158 public Narrative string, including the Reference section.

No new canonicalization rules are introduced.

## Production change

- `toda_group_proof_narrative_renderer.py`
  - replace the complete
    `_phase158_normalize_public_narrative_contract()` function

No import changes.
No test-file changes.

## Run

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_2_closure_repair5_eta_canonicalization" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_2_closure_repair5_eta_canonicalization.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_2_closure_repair5_eta_canonicalization\run_phase159_r1_2_closure_repair5.ps1"
```

The full pytest suite is intentionally not run.
