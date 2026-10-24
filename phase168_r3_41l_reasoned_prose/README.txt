Phase 168 R3-41L: Typed explanation of cited specialization and diagonal suspension

This package modifies only phase168_r3_5_model_renderer.py and only the existing
render_model_backed_narrative_markdown() function. All existing module-level
imports stay unchanged. The function-internal imports appear in the complete
replacement function. No search, model, registry, publication-order or baseline
changes are made.

The installer verifies the exact verified R3-41J2 renderer source SHA-256 before
patching; fails closed if the workspace has changed; preserves a byte-for-byte
backup; and rolls back if any focused test or audit fails.

The tests require a working GitHub develop checkout with all Phase 168 changes
through R3-41J2 already installed. No repository-wide pytest is run.

Execute from the Windows repository root:

powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41l_reasoned_prose\run.ps1"

After success, upload: phase168_r3_41l_reasoned_prose\output\review_bundle.zip
