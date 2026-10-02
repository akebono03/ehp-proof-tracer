# Phase 155 Closure-R2B-R4 changed code

## Changed repository files

- `tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py`
- `tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py`
- `tests/test_phase144_6_r5_43_1.py`
- `tests/test_phase144_6_r5_43_5.py`
- `tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py`
- `tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py`
- `tests/test_phase144_6_r5_43_11d_final_completion_audit.py`
- `tests/phase155_audit_only_nodeids.txt`

## Import changes

No top-level import block changes.

## Lightweight replacement 1

```python
def test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic():
  for n, k in (
    (
      8,
      7,
    ),
    (
      9,
      7,
    ),
  ):
    context = _context(
      n,
      k,
    )
    first = _production_from_context(
      context
    )
    second = _production_from_context(
      context
    )

    first_multi = tuple(
      tuple(
        id(
          row.proof_step
        )
        for row in argument_rows
      )
      for argument_rows in first
      if len(
        argument_rows
      ) > 1
    )
    second_multi = tuple(
      tuple(
        id(
          row.proof_step
        )
        for row in argument_rows
      )
      for argument_rows in second
      if len(
        argument_rows
      ) > 1
    )

    assert first_multi
    assert first_multi == second_multi
```

## Lightweight replacement 2

```python
def test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3():
  context = _context(
    3,
    3,
  )
  presentation, ordered = _ordered_from_context(
    context
  )
  pi6_connected = _connected_from_context(
    context
  )

  contributions = next(
    rows
    for rows in ordered
    if rows
  )
  c2 = _render_generic_narrative_step(
    contributions[
      1
    ].proof_step
  )
  c3 = _render_generic_narrative_step(
    contributions[
      2
    ].proof_step
  )

  c2_index = pi6_connected.find(
    c2
  )
  connector_index = pi6_connected.find(
    _EXPECTED_CONNECTOR,
    c2_index + len(
      c2
    ),
  )
  c3_index = pi6_connected.find(
    c3,
    connector_index + len(
      _EXPECTED_CONNECTOR
    ),
  )

  assert c2_index >= 0
  assert connector_index > c2_index
  assert c3_index > connector_index
```

## Final audit-only boundary

- `test_phase144_6_r5_43_11d_final_completion_invariants_pass`
- `test_phase144_6_r5_43_11d_renderer_remains_generic`
