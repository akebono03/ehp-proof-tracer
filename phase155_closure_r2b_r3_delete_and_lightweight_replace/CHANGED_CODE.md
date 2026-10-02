# Phase 155 Closure-R2B-R3 changed code

## Changed repository files

- `tests/test_phase144_6_r5_43_6.py`
- `tests/test_phase144_6_r5_43_8.py`
- `tests/test_phase144_6_r5_43_9.py`
- `tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py`
- `tests/phase155_audit_only_nodeids.txt`

## Deleted test functions

- `test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected`
- `test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch`
- `test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates`
- `test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains`
- `test_phase144_6_r5_43_8_has_one_hidden_signature_sequence`
- `test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences`
- `test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind`
- `test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data`

## Replaced test function

`test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations`

```python
def test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations():
  from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
    _context,
  )
  from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
  )
  from toda_group_proof_narrative_contribution_ordering import (
    build_toda_group_proof_narrative_ordered_contributions,
  )

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    3,
    3,
  )

  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )

  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )

  children = {}

  for edge in presentation.edges:
    children.setdefault(
      id(
        edge.premise_step
      ),
      set(),
    ).add(
      id(
        edge.parent_step
      )
    )

  def reachable(
    source_id,
    target_id,
  ):
    if source_id == target_id:
      return False

    stack = list(
      children.get(
        source_id,
        (),
      )
    )
    seen = set()

    while stack:
      current = stack.pop()

      if current == target_id:
        return True

      if current in seen:
        continue

      seen.add(
        current
      )
      stack.extend(
        children.get(
          current,
          (),
        )
      )

    return False

  populated = tuple(
    contributions
    for contributions in ordered
    if contributions
  )

  assert populated

  for contributions in populated:
    step_ids = tuple(
      id(
        contribution.proof_step
      )
      for contribution in contributions
    )

    assert len(
      step_ids
    ) == len(
      set(
        step_ids
      )
    )

    position_by_id = {
      step_id: position
      for position, step_id in enumerate(
        step_ids
      )
    }

    for left_id in step_ids:
      for right_id in step_ids:
        if not reachable(
          left_id,
          right_id,
        ):
          continue

        assert (
          position_by_id[
            left_id
          ]
          < position_by_id[
            right_id
          ]
        )
```

## Import changes

No top-level import block changes. The replacement uses local imports.
