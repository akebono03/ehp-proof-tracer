# Phase 169 R10E7 — Chapter VI Family Source Audit

This package performs a read-only inspection of adopted Toda Chapter VI source text, stable-family identity metadata, and the currently available publication-order manifest. It does not register any new assertion, create a proof step, alter production code, or execute the complete test suite.

From the repository root, extract the ZIP, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e7_ch6_family_source_audit\run.ps1"
```

The script checks reviewed Git blobs at known `develop` heads, runs focused tests, verifies literal source definitions and family metadata, records the current Chapter VI citation-manifest gap, and checks that tracked files remain unchanged. It writes `output/audit.json` and `output/audit.md`; previous outputs are restored on failure.

A passing audit is **not** a verified proof or an authenticating check of the original printed edition. The next change requires reviewed Chapter VI publication-position anchors and a fail-closed source registration step before any `GeneratorImage` inference is accepted.
