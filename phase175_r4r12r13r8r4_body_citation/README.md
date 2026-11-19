# Phase 175 R4R12R13R8R4 — Verified Body Citation Prefixes

This package changes only `render_model_backed_narrative_markdown` in the shared model-backed renderer. It preserves the complete proof search, original sources, registered citation numbers, EHP reasoning, and existing APIs.

For a directly cited inference whose actual GIVEN parent owns exactly the same citation numbers, the body uses “より” instead of “を用いて”. For a directly unwrapped typed source, the renderer uses the citation owned by that source's verified GIVEN ProofStep, provided the embedded statement has exactly the same type and value as the inference conclusion. Neither behavior infers a citation from a locator or a text rendering.

Execute `run.ps1 -DryRun` first, then `run.ps1`. Only focused pytest tests run. The installer pins the unmodified shared renderer blob and rejects pre-existing tracked changes to that file. It preserves LF/CRLF, and writes the **entire updated function** to `output/render_model_backed_narrative_markdown_FULL.py`. It does not edit the five top-level project documents or execute the full pytest suite.
