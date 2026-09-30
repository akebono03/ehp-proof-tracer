from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
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
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
)


def _group_result(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _web_text(
  view,
):
  parts = []

  for line in view.rendered_lines:
    if line.segments:
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          parts.append(
            "$"
            + segment.value
            + "$"
          )
        else:
          parts.append(
            segment.value
          )
      parts.append(
        "\n"
      )
      continue

    parts.append(
      line.prefix
    )
    if line.statement_latex is not None:
      parts.append(
        "$"
        + line.statement_latex
        + "$"
      )
    parts.append(
      line.suffix
    )
    parts.append(
      "\n"
    )

  return "".join(
    parts
  )


def _normalized_exactness_rendering(
  proof_step,
):
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  suffix = r" \text{ is exact}$"

  if rendered.endswith(
    suffix
  ):
    return (
      rendered[
        :-len(
          suffix
        )
      ]
      + "$ は完全である."
    )

  return rendered


def _build_case(
  label,
  n,
  k,
):
  replay = (
    build_toda_group_result_proof_replay(
      _group_result(
        n,
        k,
      ),
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      closure,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  view = (
    build_standard_web_group_proof_view(
      n,
      k,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = _web_text(
    view
  )

  return (
    presentation,
    closure,
    sidecar,
    blocks,
    arguments,
    rendered,
  )


def _block_indexes_for_step(
  blocks,
  proof_step,
):
  return tuple(
    index
    for index, block in enumerate(
      blocks
    )
    if any(
      proof_step is candidate
      for candidate in block.steps
    )
  )


def _argument_records(
  closure,
  blocks,
  sidecar,
  arguments,
  proof_step,
):
  records = []

  for argument_index, argument in enumerate(
    arguments
  ):
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        closure,
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
        closure,
        blocks,
        argument,
      )
    )

    matching_components = tuple(
      component
      for component in components
      if any(
        proof_step is candidate
        for block in component.evidence_blocks
        for candidate in block.steps
      )
    )
    exposures = tuple(
      classify_toda_group_proof_narrative_exactness_component_exposure(
        relevant_groups,
        components,
        component,
      ).value
      for component in matching_components
    )

    supporting = tuple(
      index
      for index, block in enumerate(
        blocks
      )
      if (
        any(
          block is candidate
          for candidate in argument.supporting_blocks
        )
        and any(
          proof_step is candidate
          for candidate in block.steps
        )
      )
    )
    conclusion = tuple(
      index
      for index, block in enumerate(
        blocks
      )
      if (
        block is argument.conclusion_block
        and any(
          proof_step is candidate
          for candidate in block.steps
        )
      )
    )

    if (
      matching_components
      or supporting
      or conclusion
    ):
      records.append(
        (
          argument_index,
          argument.role.value,
          {
            "evidence": bool(
              matching_components
            ),
            "exposure": exposures,
            "supporting": supporting,
            "conclusion": conclusion,
          },
        )
      )

  return tuple(
    records
  )


def audit_case(
  label,
  n,
  k,
):
  (
    presentation,
    closure,
    sidecar,
    blocks,
    arguments,
    rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  exactness_steps = tuple(
    node.proof_step
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  visible = tuple(
    proof_step
    for proof_step in exactness_steps
    if (
      _normalized_exactness_rendering(
        proof_step
      )
      in rendered
    )
  )

  print("=" * 100)
  print(label)
  print("=" * 100)
  print(
    "input_nodes="
    + str(
      len(
        presentation.nodes
      )
    )
    + " closure_nodes="
    + str(
      len(
        closure.nodes
      )
    )
    + " blocks="
    + str(
      len(
        blocks
      )
    )
    + " arguments="
    + str(
      len(
        arguments
      )
    )
  )
  print(
    "exactness_steps="
    + str(
      len(
        exactness_steps
      )
    )
    + " visible="
    + str(
      len(
        visible
      )
    )
  )

  for index, proof_step in enumerate(
    exactness_steps
  ):
    normalized = (
      _normalized_exactness_rendering(
        proof_step
      )
    )
    is_visible = (
      proof_step in visible
    )
    block_indexes = (
      _block_indexes_for_step(
        blocks,
        proof_step,
      )
    )
    block_roles = tuple(
      blocks[
        block_index
      ].role.value
      for block_index in block_indexes
    )
    argument_records = (
      _argument_records(
        closure,
        blocks,
        sidecar,
        arguments,
        proof_step,
      )
    )

    print()
    print(
      "EXACTNESS["
      + str(
        index
      )
      + "] visible="
      + str(
        is_visible
      )
    )
    print(
      "  normalized="
      + normalized
    )
    print(
      "  blocks="
      + str(
        tuple(
          zip(
            block_indexes,
            block_roles,
          )
        )
      )
    )
    print(
      "  arguments="
      + str(
        argument_records
      )
    )

  print()
  print("VISIBLE RAW EXACTNESS CONTEXT")
  for proof_step in visible:
    needle = (
      _normalized_exactness_rendering(
        proof_step
      )
    )
    position = rendered.find(
      needle
    )
    start = max(
      0,
      position - 350,
    )
    end = min(
      len(
        rendered
      ),
      position
      + len(
        needle
      )
      + 350,
    )
    print("-" * 100)
    print(
      rendered[
        start:end
      ]
    )

  return {
    "exactness_count": len(
      exactness_steps
    ),
    "visible_count": len(
      visible
    ),
    "visible": visible,
  }


def main():
  print(
    "Phase 148 RC2-4 Repair R5 "
    "two-group exactness exposure-path audit"
  )
  print(
    "Production changes: none"
  )

  for label, n, k in CASES:
    audit_case(
      label,
      n,
      k,
    )


if __name__ == "__main__":
  main()
