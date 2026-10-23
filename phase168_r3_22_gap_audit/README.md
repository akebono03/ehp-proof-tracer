# Phase 168 R3-22 — Narrative Gap Audit

This package audits the existing Backward Search → Proof Narrative Model → model-backed Renderer pipeline. It compares each of three preserved Phase 167 narratives (plus π₄² without a frozen baseline) to actual typed proof steps and the current renderer output. Reference numbering is **not** frozen.

Extract at the repository root and execute `run.ps1` in Windows PowerShell. Results appear in the package's `output/` folder. No production code, tests or documents are changed, and no full pytest is run.

Historical markers are heuristic signals, not a substitute for mathematical proof verification. The JSON records all steps, citations, missing generic mappings and generated prose for precise follow-up.
