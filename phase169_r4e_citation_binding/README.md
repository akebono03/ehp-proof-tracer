# Phase 169 R4E — Proof-linked Narrative Citations

This package fixes two citation display gaps in the public narrative for `pi_6^4` without changing the proof rules, proof search, goal resolution, trust boundary, or web API.

The change is confined to the complete `project_reference_bodies` function in `phase168_r3_37c_reference_projection.py` and the complete `render_model_backed_narrative_markdown` function in `phase168_r3_5_model_renderer.py`.

## Run on Windows PowerShell

Unzip the archive at the root of the `develop` checkout, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase169_r4e_citation_binding\run.ps1
```

The patch verifies the reviewed Git blob identities of both source files, checks that neither has unrelated working-tree edits, writes byte-exact backups and complete replacement functions, applies the narrow change, runs focused tests, and audits the proof-backed Web narrative. Any failed validation restores both source files. No full test suite is run.

## Artifacts

- `output/phase168_r3_37c_reference_projection.py.before` — byte-exact original
- `output/phase168_r3_37c_reference_projection.py.FULL` — complete revised file
- `output/project_reference_bodies_FULL.py` — complete revised function
- `output/phase168_r3_5_model_renderer.py.before` — byte-exact original
- `output/phase168_r3_5_model_renderer.py.FULL` — complete revised file
- `output/render_model_backed_narrative_markdown_FULL.py` — complete revised function
- `output/web_narrative.md`, `output/audit.json`, `output/audit.md` — verified result

The Proposition 4.4 sentence states the necessary Hopf-invariant-one hypothesis. The displayed proof tags reference actual cited ancestors, never a guessed proposition label. The previously verified `pi_6^4` complete proof is preserved.
