Phase157-R20 repair31

Purpose
-------
1. Ensure reference-prefixed math sentences end with ASCII periods.
2. Update stale Phase156 public-reference header expectations.

Current failure
---------------
After repair30:
- all reflexive/eta-bridge focused tests pass: 17 passed;
- the Phase157 shallow-dependency test fails only because the public R3 support
  paragraph lacks its final period;
- Phase156 repair12 still expects the old three-reference public policy.

Generic punctuation repair
--------------------------
`normalize_toda_group_proof_narrative_display_math_periods()` previously added
a period only when a line both started and ended with `$`.

Now it adds a period to every non-square line that:
- contains inline/display math; and
- ends with `$`.

Thus these are covered uniformly:
- `$...$`
- `[R3]より, $...$`
- `[R2]より, $...$`
- other prose/reference prefixes ending in a mathematical statement.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
- normalize_toda_group_proof_narrative_display_math_periods()

Updated stale test
------------------
- tests/test_phase156_r5_repair12_reference_frontier.py

The internal frontier tests remain unchanged.
Only final public-header expectations are updated to the current five public
References:
- Proposition 5.6
- (5.3)
- Proposition 5.3
- Proposition 5.1
- Proposition 2.2

New test
--------
- tests/test_phase157_r20_repair31_reference_period_and_stale_frontier_tests.py

No documentation changes.
No repository-wide pytest.
