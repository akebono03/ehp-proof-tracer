# Phase 163 R4-R51: Priority Semantic Review

This package performs a read-only, source-anchored review of chapter 3 stable homotopy group and stable Toda bracket passages, and chapter 5 generator notation. It carries forward all 316 audit candidates and does not register new production statements.

Run `run.ps1` from the repository root after extracting the ZIP into that root. Prerequisites are `phase163_r4_r50_output/review.json`, `phase163_r4_r47_output/catalog.json`, and `phase163_r4_r42_tex_extract/inputs/`. The runner executes only its focused nine tests, then writes `phase163_r4_r51_output/review.json`, `review_queue.csv`, and `report.md`.

Classification expresses the role of a passage in this TeX transcription; it does not verify the original edition or assert formal mathematical correctness. No source files, existing IDs, production registry, or proof search are changed.
