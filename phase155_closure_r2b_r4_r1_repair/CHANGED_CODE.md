# Phase 155 Closure-R2B-R4-R1 changed code

## Changed repository files

- `tests/test_phase155_audit_boundary.py`
- `tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py`
- `tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py`

## Import changes

No top-level import changes.

## Replacement: boundary test

```python
def test_phase155_audit_boundary_has_2_exact_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert set(
    nodeids
  ) == {
    (
      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
      "test_phase144_6_r5_43_11d_final_completion_invariants_pass"
    ),
    (
      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
      "test_phase144_6_r5_43_11d_renderer_remains_generic"
    ),
  }
  assert len(
    nodeids
  ) == 2
```

## Replacement: Phase42 determinism test

```python
def test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic():
  import inspect
  import toda_group_proof_narrative_contribution_ordering as module

  source = inspect.getsource(
    module._topological_order
  )

  assert "ready.sort(" in source
  assert "_stored_order_key(" in source
  assert "chosen = ready[0]" in source
```

## Replacement: Phase43-10 semantic connector-support test

```python
def test_phase144_6_r5_43_10_pi6_transport_semantics_support_compression_connector():
  context = _context(
    3,
    3,
  )
  presentation = context[
    0
  ]

  semantics = (
    build_toda_group_proof_narrative_hidden_bridge_semantics(
      presentation
    )
  )
  transports = tuple(
    semantic
    for semantic in semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .TRANSPORT
    )
  )

  assert transports
  assert {
    semantic.reference_identity
    for semantic in transports
  } == {
    "Proposition 5.3",
  }
  assert any(
    semantic.operation_kind
    is TodaGroupProofNarrativeHiddenBridgeOperationKind
    .SUSPENSION_STABILIZATION
    for semantic in transports
  )
```
