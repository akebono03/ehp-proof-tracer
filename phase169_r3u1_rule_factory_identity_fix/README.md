# Phase 169 R3U1 — Rule-factory identity regression repair

This package supersedes `phase169_r3u_delta_diagonal_dependency.zip` after its focused tests reported a rule-function identity failure.

The mathematical change is the same as R3U: a derived Toda (5.1) diagonal group structure is a mandatory proof premise for Delta injectivity, alongside the cited Proposition 5.1 statement. No new source fact or special-case narrative route is introduced.

The R3U1-only correction is in `test_r3i_historical_inference_only_rules_remain_intact()` in the three existing R3I test copies. The historical Hopf rule factory creates fresh Python function objects for each call; the regression checks the retained function *code object* rather than object identity. Its behavioral tests are retained.

The installer writes full before/after files to `output/`, verifies the `develop` branch, and restores altered files if any focused test or proof audit fails. See `INSTRUCTIONS_JA.md` and `CHANGED_CODE.md`. The full pytest suite is not run.
