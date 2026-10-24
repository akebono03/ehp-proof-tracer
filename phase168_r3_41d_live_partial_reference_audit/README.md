# Phase 168 R3-41D: Live Partial Proof and Reference Audit

This is a **read-only audit** of the current EHP Proof Tracer development tree. It does not patch or delete any implementation, reference registry, mathematical rule, test, or historical baseline.

## Scope

- Capture each selected public Web search exactly once, recording its actual `PartialProofResult`, screened `RegistryBridgeResult`, `ProofNarrativeModel`, common Renderer Markdown, and Web view.
- Inspect the Reference section for the **full content** of each registered statement as well as headings and citation numbers.
- Check step-to-citation relationships and the origin of cited assertion IDs against the screened bridge, without generating any new citations.
- Inspect preserved open goals, diagnostics, and completion flags for genuinely incomplete results.
- Record the status and source evidence for five real, potentially incomplete group searches, plus a known complete control case. If an expected partial case does not occur, report that coverage gap rather than claiming it passed.

## Changed files

**None in the existing repository.** Only this new audit package is added.

New functions and their locations:

- `audit_core.py`: `normalize_visible`, `web_line_text`, `web_text`, `web_reference_text`, `markdown_reference_text`, `section_bullets`, `audit_citation_projection`.
- `audit.py`: `capture_live_case`, `one_case`, `main`.
- `tests/test_phase168_r3_41d_live_partial_reference_audit.py`: six focused, full test functions.

## Running

From the extracted repository root, use PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41d_live_partial_reference_audit\run.ps1"
```

The script runs only targeted pytest modules and then saves output in `output/`. **The full pytest suite is not run.**

## Outputs and interpretation

- `output/audit.json` — structured per-case data, source hashes, explicitly identified gaps.
- `output/audit.md` — Japanese status summary.
- `output/<case>_reference.md` — actual Reference section including citation bodies.
- `output/<case>_narrative.md` — actual common narrative text.
- `output/<case>_web.txt` — what survives Web view conversion.
- `output/review_bundle.zip` — compact bundle for sharing results.

A missing registered assertion body and an inference-only citation are tracked separately. A search with no citations does **not** prove that citation rendering is correct for real partial proofs. Exceptions are reported as audit findings; this tool never promotes a goal or a diagnostic into a proven mathematical fact.

## Phase boundary

R3-41D collects evidence only. R3-41E may address an observed issue, after reviewing the actual output. No legacy route is removed in this package.
