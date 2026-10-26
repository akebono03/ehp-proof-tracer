# Phase 169 R3K — Model renderer Japanese prose projection

This package applies a narrowly-scoped, guarded full-function replacement of `render_model_backed_narrative_markdown`, and adds `phase169_r3k_narrative_projection.py`. It preserves Backward Search, proof assertions, rules, citation registry, and partial-state behavior.

The `run.ps1` script validates exact committed source, installs with backup, executes focused tests and a read-only audit, and restores automatically on failures. After installation, `output/render_model_backed_narrative_markdown.full.py` contains the complete replacement function and `output/phase168_r3_5_model_renderer.py.full.py` contains the whole resulting file.

This step is intentionally limited to cited map property prose and suppression of repeated displayed finite-cyclic group presentations while preserving each distinct cited result. It does not remove the Chapter V eta notation reference or assert a new eta-squared suspension identity.

Use `Expand-Archive` in the repository root, then `powershell -ExecutionPolicy Bypass -File .\phase169_r3k_narrative_localization\run.ps1`. Only focused pytest is run.
