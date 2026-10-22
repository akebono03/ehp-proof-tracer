# Phase 168 R3-6: standard Web entry boundary

The standard Web entry accepts `citation_source="model"`, projecting the same screened typed bridge used for its proof search into the existing R3-3/R3-5 model-based rendering path. This is opt-in: the default long-form proof path remains unchanged, avoiding loss of detailed mathematical reasoning in existing group proofs. No renderer citation heuristics are added.

From the repository root, extract the ZIP, then run `powershell -ExecutionPolicy Bypass -File .\phase168_r3_6_standard_web_entry\run.ps1`.

The script saves the original `web_group_proof.py` under the package's `backup` directory and runs only targeted tests and four-group diagnostics, not the full test suite.
