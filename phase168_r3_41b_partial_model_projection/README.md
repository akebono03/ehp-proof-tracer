# Phase 168 R3-41B — Model-Backed Partial Narratives

This package extends the existing proof narrative model with search-state metadata and renders incomplete proof states through the existing shared renderer.

The changes are limited to `ProofNarrativeModel`, `build_proof_narrative_model()`, and `render_model_backed_narrative_markdown()`. They do not change any mathematical inference, search rule, source registry, standard Web route, legacy API, or complete-proof wording.

Incomplete states display the original search status, open goals, diagnostics, and actual observed proof steps without inventing references or marking an unfinished proof complete. Completed narratives are captured and compared byte-for-byte before and after the patch.

Run `run.ps1` after extracting this directory into the repository root. It checks source hashes, backs up modified files, applies the patch, runs only focused tests, captures four complete examples, audits the three incomplete statuses, and creates `output/review_bundle.zip`. On failure, it restores the original implementation files. Do not run the full pytest suite during this subphase.

The model-free fallback and explicit legacy route remain available. Moving public routes to the new partial model is outside this package.
