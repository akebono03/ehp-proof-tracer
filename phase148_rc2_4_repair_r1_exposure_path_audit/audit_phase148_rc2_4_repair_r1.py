from toda_rules import (
  TodaProp42ExactnessStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _normalize_rendered_exactness(step):
  rendered = _render_generic_narrative_step(
    step
  )
  suffix = r" \text{ is exact}$"
  if rendered.endswith(suffix):
    return (
      rendered[:-len(suffix)]
      + "$ は完全である."
    )
  return rendered


def _build_exposure_map(
  presentation,
  blocks,
  sidecar,
  arguments,
  argument_index,
):
  argument = arguments[
    argument_index
  ]
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  result = {}

  for component in components:
    exposure = (
      classify_toda_group_proof_narrative_exactness_component_exposure(
        relevant_groups,
        components,
        component,
      )
    )
    for block in component.evidence_blocks:
      result[
        id(
          block
        )
      ] = exposure

  return (
    evidence,
    components,
    result,
  )


def main():
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      3,
      3,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  block_index_by_step_id = {
    id(
      step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for step in block.steps
  }

  exactness_steps = tuple(
    step
    for block in blocks
    for step in block.steps
    if isinstance(
      step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  print("=" * 88)
  print("Phase 148 RC2-4 Repair R1 — pi_6^3 Exposure-path Audit")
  print("Production changes: none")
  print("Repository test changes: none")
  print("=" * 88)
  print(
    f"blocks={len(blocks)} "
    f"arguments={len(arguments)} "
    f"exactness_statements={len(exactness_steps)}"
  )

  argument_data = []

  for argument_index, argument in enumerate(
    arguments
  ):
    evidence, components, exposure_map = (
      _build_exposure_map(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    direct_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )
    support_steps = tuple(
      support_step
      for premise_step in direct_premises
      for support_step in premise_step.premises
      if all(
        support_step is not existing_step
        for existing_step in direct_premises
      )
    )

    argument_data.append(
      (
        argument,
        evidence,
        components,
        exposure_map,
        local_body,
        direct_premises,
        support_steps,
      )
    )

    print()
    print(
      f"ARGUMENT[{argument_index}] role={argument.role.value}"
    )
    print(
      "  evidence block indices="
      + repr(
        tuple(
          blocks.index(
            block
          )
          for block in evidence
        )
      )
    )
    print(
      "  local-body block indices="
      + repr(
        tuple(
          blocks.index(
            block
          )
          for block in local_body
        )
      )
    )
    print(
      "  exposure="
      + repr(
        {
          blocks.index(
            next(
              block
              for block in blocks
              if id(
                block
              ) == block_id
            )
          ): exposure.value
          for block_id, exposure in exposure_map.items()
        }
      )
    )

  print()
  print("=" * 88)
  print("EXACTNESS STATEMENT REVERSE TRACE")
  print("=" * 88)

  visible_count = 0
  visible_outside_exactness_role = 0
  visible_without_exposure_class = 0

  for exactness_index, step in enumerate(
    exactness_steps
  ):
    block_index = block_index_by_step_id[
      id(
        step
      )
    ]
    block = blocks[
      block_index
    ]
    rendered_step = (
      _normalize_rendered_exactness(
        step
      )
    )
    visible = (
      rendered_step in rendered
    )

    if visible:
      visible_count += 1
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        visible_outside_exactness_role += 1

    print()
    print(
      f"EXACTNESS[{exactness_index}] "
      f"block={block_index} "
      f"role={block.role.value} "
      f"visible={visible}"
    )
    print(
      "  rendered="
      + rendered_step
    )

    any_exposure = False

    for argument_index, (
      argument,
      evidence,
      _components,
      exposure_map,
      local_body,
      direct_premises,
      support_steps,
    ) in enumerate(
      argument_data
    ):
      exposure = exposure_map.get(
        id(
          block
        )
      )
      if exposure is not None:
        any_exposure = True

      print(
        f"  argument[{argument_index}] "
        f"role={argument.role.value} "
        f"evidence={block in evidence} "
        f"local_body={block in local_body} "
        f"direct_premise={step in direct_premises} "
        f"support={step in support_steps} "
        f"exposure="
        + (
          "NONE"
          if exposure is None
          else exposure.value
        )
      )

    if visible and not any_exposure:
      visible_without_exposure_class += 1

  print()
  print("=" * 88)
  print("PATH SUMMARY")
  print("=" * 88)
  print(
    f"visible exactness statements={visible_count}"
  )
  print(
    "visible exactness outside EXACTNESS-role blocks="
    + str(
      visible_outside_exactness_role
    )
  )
  print(
    "visible exactness with no RC2 exposure classification="
    + str(
      visible_without_exposure_class
    )
  )

  print()
  print("=" * 88)
  print("FINAL NARRATIVE")
  print("=" * 88)
  print(
    rendered
  )


if __name__ == "__main__":
  main()
