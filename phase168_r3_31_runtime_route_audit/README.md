# Phase 168 R3-31 — Standard Web Runtime Route Audit

This is an audit-only package. It does not patch any repository source code.

It instruments the existing `build_standard_web_group_proof_view` path for three queries: π₃², π₄³ and π₅⁴. It records whether the same result steps reach `build_linked_proof_narrative_model` and the single `render_model_backed_narrative_markdown`, and whether the partial-markdown fallback is used. Instrumentation uses `unittest.mock.patch` within the process and is undone after each query.

The static audit also explicitly reports the legacy citation path and trace-mode compatibility path. Their existence does not indicate that standard model-backed narrative calls use them.

This does **not** confirm browser/HTTP routing, citation correctness beyond the observed model, or full-suite success. The script does not infer proof facts or mutate the working tree.

## Run

Extract this directory in the repository root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_31_runtime_route_audit\run.ps1
```

Reports: `output/runtime_route_audit.json` and `output/runtime_route_audit.md`. Only two focused tests plus three runtime queries execute; no full pytest.
