# Phase 162 R4-B Common Renderer Link Repair 1

This focused repair prevents the common transport paragraph from being injected for its own source/base group, even when a symbolic transport witness is reachable in the base group's proof ancestry.

The only production file replaced is `toda_group_proof_narrative_transport_link.py`. The updated test file `tests/test_phase162_r4_b_common_renderer_link.py` is also replaced. No changes are made to the public renderer, its baseline function, or the existing proof rules.

Run `run_phase162_r4_b_common_renderer_link_repair1.ps1` after extracting this folder into the repository root. The script copies both full files and runs only the Phase 162 R4-B focused tests. Full-suite tests are intentionally deferred to the end of Phase 162.

The repair does not certify symbolic-to-concrete specialization and does not resolve earlier baseline duplication or reference attribution.
