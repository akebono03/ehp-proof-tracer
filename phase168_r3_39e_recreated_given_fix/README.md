# Phase 168 R3-39E: Restore general-source ancestry

The earlier R3-39D patch removed legacy direct `GIVEN` links from the shared bridge, but the publication-order citation screen reconstructs all eligible fixed assertions as `GIVEN` links. This patch corrects the shared screen to reuse the existing typed specialization matcher and suppress a concrete leaf only when an eligible general assertion from the same printed source can derive it. Registered assertions are preserved.

Only `screen_shared_proof_context()` in `phase165_r52_r16_web_citation_gate.py` changes. The complete resulting function is emitted as `full_function.py`; the complete module (including all imports) is emitted under `full_files/`. There are two focused tests. Failure restores the original file. The full suite is not run.

Extract in the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase168_r3_39e_recreated_given_fix\run.ps1`.
