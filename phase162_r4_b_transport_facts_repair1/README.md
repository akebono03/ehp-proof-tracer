# Phase 162 R4-B Repair 1

Replaces the proof-tree transport facts extractor and its focused tests. It follows the symbolic family relation to the generic transport and generator bridge, without requiring the symbolic generator `eta_n` to equal the concrete root generator `eta_4`.

No production renderer or inference rules are changed. The extractor reports a structurally connected symbolic witness, **not** a verified symbolic-to-concrete substitution.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase162_r4_b_transport_facts_repair1.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r4_b_transport_facts_repair1\run_phase162_r4_b_repair1.ps1"
```

Focused tests are run. Full suite is not run.
