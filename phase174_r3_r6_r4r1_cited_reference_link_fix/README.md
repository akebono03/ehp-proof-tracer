# EHP Proof Tracer — Phase 174 R3-R6-R4R1 Source-Cited Reference Body Recovery

This package fixes a **Reference citation-body binding gap**, observed after the Phase 174 R3-R6-R4 patch was successfully applied. The previous focused gate collected 46 tests; 45 passed and one public `pi_8^5` narrative test failed because the cited headings `(4.8)` and `(5.5)` had no text.

## Scope

- Retain the existing source-assertion-ID projection path without changing its mathematical statements.
- Extend the existing common `project_cited_proof_step_reference_bodies()` fallback so that the two canonical, actually cited universal Toda GIVEN steps can display their authentic general formulas.
- Require the exact typed source statement, a source-bearing GIVEN ProofStep, a consistent source locator and known inference-rule provenance, plus re-verification of the adopted Toda text and manifest order.
- Reuse **one shared formula formatter** for registry-bound and source-cited fallback presentation. No group-specific or generator-specific Narrative is introduced.
- Preserve the existing Lemma 5.4 fallback and all other reference projection behavior.
- Do not modify proof search, the inference rule registry, source adoption, group facts, or the verified proof tree.

## Guarded target files

1. `phase168_r3_37c_reference_projection.py`: replace the entire existing `project_cited_proof_step_reference_bodies()` function only; leave other functions and imports unchanged.
2. `phase174_r3_r6_r4_common_reference/projection.py`: introduce `_universal_toda_formula()` and `project_verified_cited_toda_given_reference_body()`; replace the existing `project_cited_universal_toda_reference_body()` function with a source-equivalent implementation using the shared formatter. The entire replacement module and imports are provided.

The guard pins the reviewed `develop` HEAD `f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9`, checks the remote Git blob, and accepts only the exact previously applied R4 local files (or these exact R4R1 replacements), modulo preserved UTF-8 BOM and uniform LF/CRLF conventions. It never resets or cleans the working tree. Other uncommitted paths are left untouched.

## Verification

Run `run.ps1 -DryRun`, then `run.ps1` from the repository root. DryRun checks both target files and collects only the listed focused tests using `--import-mode=importlib`. The normal run applies the reviewed replacements and runs the original 46 focused tests, eight new R4R1 tests, and the existing public Reference audit. The full pytest suite must wait until Phase 174 closeout.

The live focused tests were **not executed** in the artifact-creation environment, which does not contain the full repository. Passing the local packaging and guard tests does **not** certify the public release.
