# Phase 168 R2-13 — Proof-tree-grounded final references

Run `run.ps1` from the repository root after extracting this folder there.

Target file: `toda_group_proof_narrative_contribution_renderer.py`.
Target function: `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`.

This is a **small transition patch**, not the final cleanup of the reference pipeline. The final Reference section is derived from reference-bearing proof steps reachable through the root's premises. Earlier markdown-driven operations remain intact for this phase; therefore a test failure or incomplete output means further diagnosis is necessary.

The script rejects repeated patching, takes a full backup in `output/`, and writes the full replacement function to `output/modified_function_full.py`.

The included focused patch tests run first, then the patch is applied and two existing reference test files are run. The full suite is intentionally not executed. To restore, copy `output/toda_group_proof_narrative_contribution_renderer.py.before` to the repository root using `Copy-Item -Force`.
