# Phase 165 R6 — Rule Collision Review

Read-only review of the five signature-collision pairs found in R5, using the active R8 rule discovery only. It does not import or execute the retired production applicability catalog.

Extract into your repository root and run `run.ps1`. Inspect `audit_result.json` for each rule's description, premises, conclusion, and presence of its guard/builder. Classification is conservative; no rule is deleted, and equivalence is not certified.

Two targeted tests are run; full pytest is not run.
