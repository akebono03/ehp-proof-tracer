# Phase 150 Stall Root-Cause Audit R5-43-10

## Scope

Audit only. No production, existing-test, or documentation changes.

The full-suite trace stopped at:

`test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3`

GitHub inspection shows that this test itself performs only a small rendered
string assertion. Its `data_by_target` module-scoped fixture, however, builds
`_data_from_context()` for all six representative groups on first use.

Therefore this audit distinguishes fixture construction cost from assertion
cost and from accumulated same-process state.

## Cases

A. Target test alone in a fresh pytest process.

B. Whole R5-43-10 file in a fresh pytest process.

C. R5-42 immediately followed by R5-43-10 in one pytest process.

D. R5-43-1 through R5-43-10 in one pytest process.

All cases use `-vv --setup-show --durations` so fixture setup and test call
times are visible separately.

## Interpretation

- If A is already very slow, the six-group `data_by_target` construction is
  intrinsically expensive.
- If A is normal but B is slow, module-level interactions matter.
- If A/B are normal but C or D become slow, preceding Phase144-6 state causes
  cumulative degradation.
- If all four are normal while the full-suite trace stalls, the cause lies
  earlier than the R5-43 prefix and a broader same-process predecessor window
  is required.

This audit does not change caching or renderer behavior.
