# Phase 169 R10ET-R4 — Certified cyclic Definition projection

This package installs only a proof-preserving, typed cyclic display fix. It does **not** change the backward search priority, the stored source registry, the direct-sum projection, or any existing tests or documentation.

## Changed code

- `phase169_r10a_verified_stable_chain_projection/projection.py`: replace the complete `project_verified_stable_image_chain()` function in place. Preserve its public signature and all original typed checks. Replace only the final cited-image support call with the R4 verified cited-or-Definition policy.
- `phase168_r3_5_model_renderer.py`: replace the complete `render_model_backed_narrative_markdown()` function in place. Retain all other branches; print `Definition より,` for a verified R4 cyclic chain with no image citations, and never print an orphan `より,` prefix.
- Add `phase169_r10et_r4_cyclic_definition_projection/policy.py` with the full, self-contained `canonical_definition_image`, `_verified_index`, `_ancestor_given_numbers`, and `verified_cyclic_generator_image_citation_numbers` functions.
- Add full new test functions in `tests/test_r10et_r4_live.py` and `tests/test_r10et_r4_patch.py`.

No top-level imports in existing production files are changed. The changed local import in each complete function is included in the exported function source. Both **complete replacement files** and **complete changed functions** are exported to the run's output directory before production files are updated. No `...` code omission is used.

## Run (Windows PowerShell)

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r4_cyclic_definition_projection.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r4_cyclic_definition_projection\run.ps1"
git status -sb
```

Run must start from `develop` with no preexisting tracked changes; exact file hashes are verified against the reviewed GitHub versions. It applies two complete-function edits and runs focused pytest plus real, trusted, common-Definition shadow searches for 10 target groups. On any failed test or audit it restores both production files from the backup.

Expected after success: **exactly two modified tracked files** and an untracked phase directory. Review full replacement sources under `output/<timestamp>/`. This phase deliberately does not run the entire pytest suite.

## Boundary

R4 prepares the cyclic projection and renderer to support universal stable-element Definition without removing legacy citation paths. R5 may change the shared expansion priority only after R4's real-case comparisons pass. Existing DB prior and Toda (4.5) remain independent, verified proof evidence.
