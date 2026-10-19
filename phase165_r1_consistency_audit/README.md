# Phase 165 R1 — Read-only consistency audit

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r1_consistency_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r1_consistency_audit\run.ps1"
```

The audit performs the existing n,k-only typed search for (2,1) and (3,1), collects actual `ProofStep` ancestry, uses existing replay and presentation APIs, captures the current public Markdown, and examines the shared `WebGroupProofView`. Results are written under `phase165_r1_audit_results/`.

No repository source code is edited. No full pytest suite is run. This audit does not claim to inspect Jinja2 HTML, browser DOM, or KaTeX/MathJax rendering; those require the live app/browser. A missing stage or exception is reported, not patched or hidden.
