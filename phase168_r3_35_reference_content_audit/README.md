# Phase 168 R3-35 — Reference Content Connection Audit

Read-only diagnostic for the actual Proof Narrative Model citation-to-assertion connection. Inspect the cited assertion IDs, their registered `content` objects, and the renderability of corresponding proof conclusions for π₃², π₄³ and π₅⁴.

The audit deliberately does not invent generic theorem text from specific example statements or locator strings. It distinguishes verified source statements from proof-step conclusions. The next implementation should use these concrete findings to render only evidence-backed content, without changing the common Renderer architecture.

Unzip into the repository root. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_35_reference_content_audit\run.ps1
```

Outputs: `output/reference_content_audit.md` and `.json`. Only two limited tests are run; full pytest is reserved for the end of Phase 168.
