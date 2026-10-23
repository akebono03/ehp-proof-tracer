# Phase 168 R3-32 — Renderer Integrity Audit

This package inspects the post-R3-29 renderer and its three projections without editing project code. It scans for proof-step construction/search calls, records renderer type checks, and renders π₃², π₄³ and π₅⁴ using the common model-backed renderer.

The runtime checks ensure that model steps match proof steps, rendering does not mutate inputs, numbered reference headings correspond to the Proof Narrative Model, and all displayed reference numbers belong to the model.

Run from an extracted folder in the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_32_renderer_integrity_audit\run.ps1
```

Outputs: `output/renderer_integrity_audit.json` and `output/renderer_integrity_audit.md`. The exit status is nonzero for mismatches. This is a focused audit only, not the full pytest suite. It does not establish mathematical proof soundness or HTTP routing.
