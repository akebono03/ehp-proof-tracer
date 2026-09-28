from collections import defaultdict

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _build_data(
  max_depth,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  if max_depth is None:
    replay = (
      build_toda_group_result_proof_replay(
        group_result
      )
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      sidecar,
      arguments,
    )
  )
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  public_markdown = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    proof_chains,
    contributions,
    base_markdown,
    public_markdown,
  )


def _step_label(
  proof_step,
):
  try:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )
  except Exception as error:
    rendered = (
      "<render-error:"
      + type(error).__name__
      + ">"
    )

  return (
    rendered
    if rendered
    else type(
      proof_step.conclusion
    ).__name__
  )


def _step_key(
  proof_step,
):
  return (
    f"id={id(proof_step)} "
    f"type={type(proof_step.conclusion).__name__} "
    f"text={_step_label(proof_step)!r}"
  )


def _argument_step_ids(
  argument,
):
  result = set()

  for block in argument.supporting_blocks:
    for proof_step in block.steps:
      result.add(
        id(
          proof_step
        )
      )

  for proof_step in argument.conclusion_block.steps:
    result.add(
      id(
        proof_step
      )
    )

  return result


def _find_pi5_3_steps(
  presentation,
):
  candidates = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    text = _step_label(
      proof_step
    )
    normalized = (
      text
      .replace(" ", "")
      .replace(r"\left", "")
      .replace(r"\right", "")
    )

    if (
      r"\pi_{5}^{3}" in normalized
      or "pi_5^3" in normalized
      or "π_5^3" in normalized
    ):
      candidates.append(
        proof_step
      )

  return tuple(
    candidates
  )


def _print_argument_inventory(
  arguments,
):
  print("Argument inventory")
  print("-" * 78)

  for index, argument in enumerate(
    arguments
  ):
    conclusion = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    print(
      f"A{index:02d} "
      f"role={argument.role.value} "
      f"supporting_blocks={len(argument.supporting_blocks)} "
      f"children={argument.child_argument_indices}"
    )
    if conclusion is not None:
      print(
        "  conclusion: "
        + _step_key(
          conclusion
        )
      )

    for block_index, block in enumerate(
      argument.supporting_blocks
    ):
      print(
        f"  support[{block_index}] "
        f"role={block.role.value} "
        f"steps={len(block.steps)}"
      )
      for proof_step in block.steps:
        print(
          "    "
          + _step_key(
            proof_step
          )
        )


def _print_definition_diagnosis(
  presentation,
  blocks,
  arguments,
  contributions,
  markdown,
):
  definition_indices = tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    )
  )

  print("")
  print("Definition owner diagnosis")
  print("-" * 78)
  print(
    "definition_argument_indices="
    + repr(
      definition_indices
    )
  )

  definition_block_steps = tuple(
    proof_step
    for block in blocks
    if block.role.value == "definition"
    for proof_step in block.steps
  )
  print(
    "definition_block_step_count="
    + str(
      len(
        definition_block_steps
      )
    )
  )

  for proof_step in definition_block_steps:
    step_id = id(
      proof_step
    )
    owners = tuple(
      index
      for index, argument in enumerate(
        arguments
      )
      if step_id in _argument_step_ids(
        argument
      )
    )
    contribution_owners = tuple(
      (
        contribution.owner_argument_index,
        contribution.owner_argument_role.value,
        contribution.contribution_role.value,
        contribution.placement.value,
      )
      for argument_contributions in contributions
      for contribution in argument_contributions
      if contribution.proof_step is proof_step
    )
    rendered = _step_label(
      proof_step
    )

    print(
      "definition-step: "
      + _step_key(
        proof_step
      )
    )
    print(
      "  argument_owners="
      + repr(
        owners
      )
    )
    print(
      "  contribution_owners="
      + repr(
        contribution_owners
      )
    )
    print(
      "  rendered_in_final="
      + str(
        bool(
          rendered
          and rendered in markdown
        )
      )
    )

  node_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  print(
    "definition_steps_all_in_presentation="
    + str(
      all(
        id(
          proof_step
        ) in node_ids
        for proof_step in definition_block_steps
      )
    )
  )


def _print_pi5_3_diagnosis(
  presentation,
  arguments,
  contributions,
  markdown,
):
  print("")
  print("pi_5^3 supporting-step owner diagnosis")
  print("-" * 78)

  candidates = (
    _find_pi5_3_steps(
      presentation
    )
  )
  print(
    "pi5_3_candidate_count="
    + str(
      len(
        candidates
      )
    )
  )

  for proof_step in candidates:
    step_id = id(
      proof_step
    )
    argument_owners = tuple(
      (
        index,
        argument.role.value,
      )
      for index, argument in enumerate(
        arguments
      )
      if step_id in _argument_step_ids(
        argument
      )
    )
    contribution_owners = tuple(
      (
        contribution.owner_argument_index,
        contribution.owner_argument_role.value,
        contribution.contribution_role.value,
        contribution.placement.value,
        contribution.provider_keys,
      )
      for argument_contributions in contributions
      for contribution in argument_contributions
      if contribution.proof_step is proof_step
    )
    parents = tuple(
      edge.parent_step
      for edge in presentation.edges
      if edge.premise_step is proof_step
    )
    premises = tuple(
      edge.premise_step
      for edge in presentation.edges
      if edge.parent_step is proof_step
    )
    rendered = _step_label(
      proof_step
    )

    print(
      "pi5_3-step: "
      + _step_key(
        proof_step
      )
    )
    print(
      "  argument_owners="
      + repr(
        argument_owners
      )
    )
    print(
      "  contribution_owners="
      + repr(
        contribution_owners
      )
    )
    print(
      "  rendered_in_final="
      + str(
        bool(
          rendered
          and rendered in markdown
        )
      )
    )
    print(
      "  premise_steps="
      + repr(
        tuple(
          _step_key(
            step
          )
          for step in premises
        )
      )
    )
    print(
      "  parent_steps="
      + repr(
        tuple(
          _step_key(
            step
          )
          for step in parents
        )
      )
    )


def _print_contribution_inventory(
  contributions,
):
  print("")
  print("Contribution inventory")
  print("-" * 78)

  for argument_index, items in enumerate(
    contributions
  ):
    print(
      f"A{argument_index:02d} contributions={len(items)}"
    )
    for contribution in items:
      print(
        "  "
        + _step_key(
          contribution.proof_step
        )
      )
      print(
        "    owner="
        f"A{contribution.owner_argument_index:02d}/"
        f"{contribution.owner_argument_role.value} "
        f"role={contribution.contribution_role.value} "
        f"placement={contribution.placement.value} "
        f"providers={contribution.provider_keys}"
      )


def _diagnose(
  label,
  max_depth,
):
  print("=" * 78)
  print(label)
  print("=" * 78)

  (
    presentation,
    blocks,
    sidecar,
    arguments,
    proof_chains,
    contributions,
    base_markdown,
    public_markdown,
  ) = _build_data(
    max_depth
  )

  print(
    f"nodes={len(presentation.nodes)} "
    f"blocks={len(blocks)} "
    f"arguments={len(arguments)} "
    f"proof_chains={len(proof_chains)}"
  )
  print(
    "argument_roles="
    + repr(
      tuple(
        argument.role.value
        for argument in arguments
      )
    )
  )
  print(
    "generic_with_contributions_equals_public="
    + str(
      base_markdown
      == public_markdown
    )
  )

  _print_argument_inventory(
    arguments
  )
  _print_definition_diagnosis(
    presentation,
    blocks,
    arguments,
    contributions,
    public_markdown,
  )
  _print_pi5_3_diagnosis(
    presentation,
    arguments,
    contributions,
    public_markdown,
  )
  _print_contribution_inventory(
    contributions
  )

  print("")
  print("Final Narrative")
  print("-" * 78)
  print(
    public_markdown
  )
  print("")


def main():
  _diagnose(
    "A. depth=2 presentation",
    2,
  )
  _diagnose(
    "B. full/default presentation",
    None,
  )
  print("=" * 78)
  print("Diagnosis complete.")
  print("No production repair was attempted after rollback.")
  print("=" * 78)


if __name__ == "__main__":
  main()
