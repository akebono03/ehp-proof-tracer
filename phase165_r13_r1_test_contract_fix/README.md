# Phase 165 R13-R1 — fail-closed test-contract correction

## Reason

Phase 165 rejects a `pi_5^3` proof when a typed goal/rule catalog is not configured. The Phase 164 test `test_pi53_common_narrative_is_renderable` wrongly requires a successful legacy narrative and thus fails. Do not turn the legacy path back on to satisfy this test.

## Changed items

- `tests/test_phase164_r5_r2_unified_web_display.py`
  - Adds the complete import `from phase165_goal_only_search import GoalSearchIncompleteError`.
  - Replaces `test_pi53_common_narrative_is_renderable` with `test_pi53_common_narrative_requires_registered_goal_catalog`.

No production source changes. The `(2,1)` legacy guard from R13 remains intact. No other legacy routes are switched in this step.

## Targeted test

Run `run.ps1` from the extracted package. It executes only the new R13-R1 regression test and the existing Phase 164 R5-R2 test file; whole-suite pytest is intentionally deferred.

## Completion / boundary

Completion means the UI rejects unsupported pi_5^3 proof instead of claiming Phase 164 R5 success, and targeted tests pass. This is NOT end-to-end typed proof generation. Later work must connect a validated registry and common rule catalog; a successful result can then replace the failure expectation.
