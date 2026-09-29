Phase 145-1 Stage 2 - Phase Artifact Classification

Purpose
-------
Classify tracked Phase work artifacts conservatively into:

A_SAFE_DELETE
  Mechanically proven low-risk candidates under the current rules.

B_REVIEW
  Artifacts that contain unique payload/test/apply material, are referenced
  by other Phase artifacts, or otherwise are not mechanically proven safe.

C_SAVE
  Artifacts whose names are directly referenced by canonical production code,
  tests, or formal documentation.

Safety
------
This package DOES NOT DELETE OR MODIFY repository files.
It only writes classification reports under:
  phase145_1_stage2_artifact_classification/output/

The first-stage backup files are excluded from this classification.

GitHub baseline
---------------
develop tree SHA used when preparing this audit:
3bcb84fe687ace64f15859df1f9dcb5da7113266

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase145_1_stage2_artifact_classification\run_phase145_1_stage2.ps1"

Outputs
-------
phase145_1_stage2_classification.csv
phase145_1_stage2_summary.txt

R1 performance repair
---------------------
Reference scanning now caches each text/code file once and builds reference indexes.
Classification rules and deletion behavior are unchanged. This remains audit-only.
