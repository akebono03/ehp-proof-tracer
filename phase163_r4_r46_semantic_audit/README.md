# Phase 163 R4-R46 — Conservative TeX Semantic Anchor Audit

This package audits the 23 existing assertion IDs belonging to Proposition 5.1, Proposition 5.3, Proposition 5.6, equation (5.1), and equation (5.3).

It requires the previous `phase163_r4_r45_output/review.json` and the unchanged `phase163_r4_r42_tex_extract/inputs/Toda_05_2(6).tex` under the repository root.

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r46_semantic_audit\run.ps1"
```

Outputs in `phase163_r4_r46_output`: `audit.json`, `assertion_anchors.csv`, and `report.md`.

The four principal classifications are `EXPLICIT`, `SPECIALIZATION`, `SURROUNDING_TEXT`, and `NOT_LOCATED`. `ANCHOR_NOT_FOUND` means the editorially selected TeX pattern could not be found. All findings are conservative review annotations. `EXPLICIT` means a mathematical notation witness is present, **not** that the complete formal statement or the original published text was independently verified. Source verification remains false. No registry mutation, ID allocation, inference rule, or proof-search integration occurs.

Only the eight focused tests run. The project-wide pytest suite remains deferred until the end of Phase 163.
