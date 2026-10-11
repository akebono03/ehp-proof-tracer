# Phase 163 R4-R42: Read-only TeX extraction

Run `run.ps1` from the project root after extracting the archive into that root.
The package includes the exact five input TeX files uploaded for chapters 1–5.
It extracts labelled theorem-like environments and equation environments in source order,
retaining unmodified TeX content in `phase163_r4_r42_output/extraction.json`.

It optionally compares inferred reference locators with the current registry bridge.
No source documents, Statement IDs, registry entries, or proof-search behavior are modified.
Environment labels are candidates only, not verified publication numbers. Some translated
or parallel-column text is outside the extracted environments. Unlabelled statements,
unnumbered equations, standalone definitions, and implicit references require later review.
Do not treat this output as a complete bulk registration.

Run focused tests: `python -m pytest -q phase163_r4_r42_tex_extract/tests/test_phase163_r4_r42_tex_extract.py`.
The full test suite is intentionally deferred to the end of Phase 163.
