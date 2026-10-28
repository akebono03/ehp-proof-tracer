# Phase 169 R10ET-R1 — Definition/Reference Dependency Audit

This is an **AUDIT_ONLY** bundle. It reads the current repository's search results, replays the Trust Boundary verifier, records the reachable Proof Tree, resolves every Reference to its linked ProofSteps, and checks whether cited `GeneratorImage` steps are eligible for the universal stable-element Definition. It never replaces an inference, prunes a source, or rewrites the renderer.

## Run from a PowerShell terminal

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r1_definition_reference_dependency_audit.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r1_definition_reference_dependency_audit\run.ps1"
git status -sb
```

The script refuses branches other than `develop`. It also refuses a HEAD different from `36e4dc41427ec4437009c96b01cacb07dc165bf6` until source changes have been reviewed. For a reviewed newer HEAD, run with `-AllowHeadChange`. Use `-Cases core` for six higher-stem cases, or the default `-Cases all` for those plus six 1-/2-stem cases. Use `-SkipTests` only to omit the five focused existing-test files.

Reports are written to `output/<timestamp>/audit.json`, `audit.md`, and individual `pi*_*/proof_steps.json` and `narrative.md` files. A failure in an individual case is retained in `audit.json` rather than concealed. No full-suite pytest is run.

`image_cited_but_common_eligible` reports possible *replacement candidates*, not a mathematical license to delete existing citations. Existing source-group results and Toda (4.5) must remain in the verified proof. The bundle has not been executed against the user's local working tree.
