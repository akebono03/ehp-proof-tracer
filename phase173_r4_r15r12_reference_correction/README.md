# EHP Proof Tracer — Phase 173 R4-R15R12R2

## Purpose

Finish the R15R12 focused-test contract corrections after R15R12R1 left one obsolete prior-proof count check, while retaining the source-verified Reference presentation changes. The R15R12R1 DryRun passed six static tests, but focused execution yielded 31 passed and one failed. The sole failure was `assert len(previous.proven_steps) == 28` in the R4G regression: the current n=3, k=2 search instead returns 27 proven steps, still COMPLETE. The installer reported `RESTORED=PASS`; the production source was rolled back.

This package includes the complete R15R12 patch and R15R12R1 corrections, plus the final R15R12R2 prior-proof assertion correction. It does **not** alter proof search, register axioms, manufacture an eighteenth ProofStep, or add specialized narratives.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed HEAD: `e2996ec2ff496203f94daa9bc22550c5e69a6b11`.
- The canonical n=4, k=2 result is COMPLETE with **17** proven ProofSteps, while older suites hard-code **18**. The n=3, k=2 prior result is likewise COMPLETE with **27** steps, while one remaining R4G assertion hard-codes **28**. Proof-step counts are not theorem invariants under First Successful Proof Search.
- The Reference text correctly uses `\pi_i^{n}`; a new test expected the semantically identical `\pi_i^n` spelling. The assertion was corrected to test the actual TeX string without changing the rendered mathematics.
- All original source-verification, citation, completion, and other Web assertions remain in the historical tests.

## Files touched in the repository

Three production modules are patched, without changing their mathematical evidence:

1. `phase168_r3_37c_reference_projection.py` — `project_reference_bodies`, newly added `_verified_source_sentence`, `project_cited_proof_step_reference_bodies`.
2. `phase168_r3_3_proof_narrative_model.py` — `build_proof_narrative_model`.
3. `web_group_proof_common.py` — `_build_group_proof_inline_segments`.

Two directly relevant, historical test modules are patched:

4. `phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py` — `pi64`, `test_r4g_fibration_is_in_same_source_bound_reference`, `test_r4g_web_and_pi53_existing_route_unchanged` (including its completed n=3,k=2 prior proof).
5. `phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py` — `pi64`, `test_r4e_standard_web_path_remains_verified_and_complete`.

Changes to the current phase package itself: `patch.py` (including new `patch_r4e_test`), `install.py` (fifth source blob guard), `tests/test_static.py` (additional proof-step contract tests), and `tests/test_integration.py` (corrected TeX spelling), plus documentation. No repository-wide primary document is changed.

## Run (PowerShell, from the repository root)

Extract the ZIP into the repository root, overwriting the earlier `phase173_r4_r15r12_reference_correction/` package, and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r12_reference_correction\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r12_reference_correction\run.ps1"
```

Both modes require the exact reviewed HEAD and every reviewed Git blob, rejecting unreviewed content. The installer writes full modified functions/imports to `FULL_CHANGED_UNITS.md`. If a focused test or audit fails, the script restores all five originally reviewed files (unless another user changed them since installation). The full repository test suite is deferred until Phase 173 closes.

## Acceptance and next boundary

- Proposition 4.4: complete source-verified conditional isomorphism, without its preceding historical paragraph, appears in Reference.
- Lemma 5.4: verified typed source statement is rendered in Reference.
- Verified `sphere.csv` citations: their TeX is parsed as inline mathematics even inside a bold heading.
- Completed proofs stay completed; k=8 and k=31 keep unresolved named-generator goals.
- Existing source proofs are preserved; no artificial proof-step count is imposed for either the current or prior proof.

Only the Reference and shared Markdown presentation are in scope. The separate UI `Proof` heading duplication and generalizing abstract-root citations are not implemented by R15R12R1.
