# EHP Proof Tracer — Phase 169 R4D

Read-only audit of the **pi_6^4** completed proof's public Web narrative, reference citations, and typed proof-tree trust boundary.

## Scope

- Checks Git `develop`, existing R4B and R4C expansion bindings, and the 18-step proof.
- Validates the same proof-tree trust boundary as the public Web route.
- Calls the real public `build_standard_web_group_proof_view` with `citation_source="model"`.
- Captures rendered Markdown, model citation mappings, and Web line segments.
- Reports uncited, mismatched, or duplicated references as *visual findings*, without modifying proof validity.
- Runs only scoped pytest. Does **not** modify production modules, tests, or the tracked R4C audit output.

## Run (PowerShell from repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4d_pi64_narrative_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4d_pi64_narrative_audit\run.ps1"
```

## Output

- `output/audit.md` — human-readable audit summary.
- `output/audit.json` — structured findings, citation associations, full narrative and Web rendering segments.
- `output/web_narrative.md` — full proof text and reference display for manual review.

The full test suite is intentionally deferred until the end of Phase 169. The audit reports reference-display issues but never invents proof steps or silently repairs them.
