# Phase 144-6 Final Completion Audit and Full pytest

## Production changes

None.

This package is the final Phase 144-6 completion gate.

## Audit order

1. Compile the four Phase 144-6 production-delta files.
2. Run `git diff --check`.
3. Print raw `git diff --numstat`.
4. Print a diff stat ignoring end-of-line whitespace.
5. Verify `toda_upstream_bootstrap.py` still matches local `HEAD`.
6. Recheck the R25-9A/R25-9B observable completion contract.
7. Discover and run every local `tests/test_phase144_6*.py`.
8. Run available cross-phase boundary controls.
9. Only if every previous gate passes, run the complete `pytest -q` suite.

## Explicit completion contract

For pi_6^3 with source replay depth 2:

- the source replay remains depth 2;
- the ordinary presentation remains depth 2;
- Narrative semantic closure adds exactly one missing endpoint;
- that endpoint is a `TodaBracketMembershipStatement`;
- the resulting argument roles are group structure, order, definition;
- the Narrative contains the nu-prime definition introduction;
- the Narrative retains the order relation and final group conclusion;
- the internal pi_5^3 supporting fact remains suppressed.

## Full-suite rule

The full suite is run only after the completion audit passes.

If the full suite fails, Phase 144-6 is not declared complete. The failing
regressions become the only repair target before another final gate.
