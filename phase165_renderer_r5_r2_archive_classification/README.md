# Phase 165 Renderer R5-R2: active vs. archived imports

Read-only targeted final audit after R4. This update distinguishes active root modules and official `tests/` imports from explicitly suffixed historical root snapshots (`*.phaseNNN_name.py`). Archived hits are *reported* separately, not deleted or silently forgotten. An active residual import still fails the audit and is printed with its exact path in `audit_output/review.md`.

Extraction: unzip into the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase165_renderer_r5_r2_archive_classification\run.ps1`.

No production sources are changed. Targeted tests only; no full pytest. A static PASS still requires review of independent helper Renderer candidates, dynamic runtime paths, and mathematical presentation semantics.
