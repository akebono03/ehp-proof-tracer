# Phase 165 R57-R1: One registered Web proof entry

This patch consolidates the remaining standard Web group-proof entry onto the registered `n,k`-only search already used by the Group query. A completed proof continues through the restored public `render_toda_group_proof_narrative_markdown()` renderer. No group-specific prose, proof rules, or mathematical facts are introduced.

Only `web_group_proof.py` is modified, with an idempotent installer and a backup. Its entire `build_standard_web_group_proof_view` function is replaced; top-level imports stay unchanged. `audit_routes.py` writes a read-only inventory of direct Python call sites in root production modules to `phase165_r57_r1_renderer_inventory.json`. It intentionally does not delete shared helpers or the partial renderer: existing public code depends on them, and incomplete proofs still require an explicit public-presentation design. Removal before a full dependency and regression audit could break existing APIs or tests.

Run `run.ps1` from the extracted directory. The script installs, inventories, and runs four focused test modules. The full test suite is not run.
