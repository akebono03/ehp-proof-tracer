# Phase 167 R4-1: Typed internal-rule label suppression

This package modifies only `toda_group_proof_narrative_renderer.py`, specifically the full existing `render_toda_group_proof_narrative_markdown()` function. It does not add another renderer or change the public entry.

The suppression is **selected from typed ProofStep ancestry**: `CyclicStructureStatement` with a `QuotientIsomorphismStatement` premise and a finite order. No literal English rule name is encoded in the production patch. After the existing mathematical narrative and quotient anchors have been processed, the formatter removes only standalone labels belonging to those identified proof steps. The final line equality is presentation bookkeeping, not the predicate deciding which inference to hide.

The patch does not change proof trees, citations, group results, theorem terminology, equation deduplication or LaTeX. The runtime comparison requires the complete Web narrative to remain byte-for-byte unchanged for pi3^2 and pi5^4 through pi7^6; for pi4^3, it permits only removal of the one known label line. All five searches must stay complete. On any comparison or pytest failure, the changed module is restored.

Run in repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase167_r4_typed_rule_suppression.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase167_r4_typed_rule_suppression\run.ps1"
```

The installer refuses unexpected source structure and writes the full replacement function to `modified_function_full.py.txt`. Only focused pytest is run. 2-stem and later R4 items are excluded.
