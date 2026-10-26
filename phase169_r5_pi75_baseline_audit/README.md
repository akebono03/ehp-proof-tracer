# Phase 169 R5 — Pi7^5 Baseline Audit

This read-only package inspects the existing typed backward search for `pi_7^5` (`n=5, k=2`). It does not modify production code, established tests, proof sources, or project documentation.

Run from the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r5_pi75_baseline_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r5_pi75_baseline_audit\run.ps1"
```

The runner executes 17 focused pytest cases (4 new, 7 existing R3O and 6 existing R4C), then inspects the registered `pi_7^5` goal, citation-screened `(4.5)` premise availability, Toda stable-range guard, current real backward search, optional narrative and Web view. A partial proof remains partial.

Outputs are generated in `output/audit.md`, `output/audit.json`, and `output/web_narrative.md`. The tracked Git status is compared before and after the audit; no full-suite pytest runs.
