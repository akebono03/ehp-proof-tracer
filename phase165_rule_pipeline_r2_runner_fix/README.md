# Phase 165 Rule Pipeline R2 Runner Fix

This replaces only the execution wrapper and test import of the previous read-only audit.

The audit is run with `python -m phase165_rule_pipeline_r2_runner_fix.audit` from the repository root so `expression` and other project modules can be imported. No production files are changed. Targeted tests only; full pytest is not run.
