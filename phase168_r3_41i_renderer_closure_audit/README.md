# Phase 168 R3-41I — Renderer Closure and Frozen Benchmark Audit

This read-only audit evaluates the current Proof Narrative Model Web renderer against the immutable Phase 168 baselines for pi3^2, pi4^3, and pi5^4. It reuses the repository's R3-38 full-text comparison and R3-39F explanation checks; it never edits mathematical statements, source files, or frozen originals.

Extract the ZIP to the repository root. Run `phase168_r3_41i_renderer_closure_audit/run.ps1` in Windows PowerShell. Its limited pytest checks run before the real capture. The outputs are written to `output/audit.json`, `output/audit.md`, original/current comparison text, unified differences, and `output/review_bundle.zip`.

The benchmark policy freezes the mathematical reasoning, order, and level of detail, **not** the numeric Reference labels or Reference list order. Diff counts are advisory: they do not establish mathematical errors or equivalence. Explanation checks are narrow heuristics and cannot replace a complete content review. The audit returns a successful exit code when the capture finishes, even when outstanding content gaps remain; read the `status` and `issues` fields.

The unresolved finite-cyclic search premises found in R3-41H belong to later proof-search work. This package only assesses renderer closure and does not run the full pytest suite.
