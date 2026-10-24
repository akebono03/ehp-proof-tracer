# Phase 168 R3-41P3: Provenance-only specialization display

## Scope

Replace one nested Renderer helper and one Toda (4.5) evidence-projection function. No search rules, mathematical source registrations, Web routing, or public API names are changed. The existing Proof Tree and Narrative Model supply the necessary citation ancestry. No new adapter layer is introduced.

## Install and run (PowerShell)

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41p3_provenance_only.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41p3_provenance_only\run.ps1"
```

## Changes

- `phase168_r3_5_model_renderer.py`: nested `validated_specialization_citation_numbers()` is replaced by `direct_given_premise_citation_numbers()`, and its sole call site changes. The full `render_model_backed_narrative_markdown()` function, as written to the user's environment, is preserved in `output/full_files/phase168_r3_5_model_renderer.py`.
- `phase168_r3_27_typed_statement_projection.py`: replace the complete `toda45_specialization_evidence()` function. No imports are changed.
- Add focused tests checking the entire three-group rendered proof and Reference texts against R3-41P2 captures, rule-replay absence, and consistent citations.

The exact complete replacement functions are in `replacements.py`. The complete resulting source files are saved automatically under `output/full_files/`.

## Rollback

```powershell
python -B -m phase168_r3_41p3_provenance_only.restore
```

The run script automatically restores both source files when its focused pytest fails. The R3-29 test modification from the previous task is left untouched.

## Deferred scope

The typed exactness / stable eta rendering checks and inference-rule-name-dependent word choice are unchanged by this patch; they will be audited independently. The full pytest suite is reserved for the end of Phase 168.
