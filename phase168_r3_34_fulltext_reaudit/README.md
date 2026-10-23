# Phase 168 R3-34 — Full-text baseline re-audit

This is a read-only baseline comparison for three proofs using the frozen original files and the current R3-33 captured output bundled in this package. Both reference and proof sections are compared line by line. Each case produces separate unified diffs and a reviewed discrepancy inventory. Reference-number changes alone are not treated as correctness failures.

The inventory is based on manual review of the supplied frozen and current texts, and the diff is computed mechanically. The package does not infer mathematical soundness from phrase matching. It does not edit repository code, and it does not perform the full pytest suite.

Extract in the repository root and execute `powershell -ExecutionPolicy Bypass -File .\phase168_r3_34_fulltext_reaudit\run.ps1`.

Generated reports are in `output/`: `fulltext_reaudit.md`, `fulltext_reaudit.json`, and separate `*_reference.diff` and `*_proof.diff` files. The input current captures are the files from R3-33, not a fresh runtime capture; regenerate and independently review if the code has changed.
