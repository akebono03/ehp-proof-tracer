from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
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


def _build_data(max_depth):
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result

  if max_depth is None:
    replay = build_toda_group_result_proof_replay(group_result)
  else:
    replay = build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )

  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  proof_chains = build_toda_group_proof_narrative_proof_chains(
    presentation,
    sidecar,
    arguments,
  )
  raw_markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  contributions = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    sidecar,
    arguments,
    proof_chains,
    current_markdown=raw_markdown,
  )
  contribution_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  public_markdown = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return (
    presentation,
    blocks,
    arguments,
    contributions,
    raw_markdown,
    contribution_markdown,
    public_markdown,
  )


def _render_step(proof_step):
  rendered = _render_generic_narrative_step(proof_step)
  if rendered:
    return rendered
  return type(proof_step.conclusion).__name__


def _step_line(proof_step):
  return (
    f"id={id(proof_step)} "
    f"type={type(proof_step.conclusion).__name__} "
    f"text={_render_step(proof_step)!r}"
  )


def _argument_step_ids(argument):
  return {
    id(proof_step)
    for block in (
      argument.supporting_blocks
      + (argument.conclusion_block,)
    )
    for proof_step in block.steps
  }


def _looks_like_pi5_3(proof_step):
  text = _render_step(proof_step)
  compact = text.replace(" ", "")
  return (
    r"\pi_{5}^{3}" in compact
    or "π_{5}^{3}" in compact
    or "π_5^3" in compact
    or "pi_5^3" in compact
  )


def _print_stage_presence(label, proof_step, raw, contribution, public):
  rendered = _render_step(proof_step)
  print(
    f"  {label}: "
    f"raw={rendered in raw if rendered else False} "
    f"after_contribution={rendered in contribution if rendered else False} "
    f"public={rendered in public if rendered else False}"
  )


def diagnose(label, max_depth):
  (
    presentation,
    blocks,
    arguments,
    contributions,
    raw_markdown,
    contribution_markdown,
    public_markdown,
  ) = _build_data(max_depth)

  print("=" * 80)
  print(label)
  print("=" * 80)
  print(
    f"nodes={len(presentation.nodes)} "
    f"blocks={len(blocks)} "
    f"arguments={len(arguments)}"
  )
  print(
    "roles="
    + repr(tuple(argument.role.value for argument in arguments))
  )
  print(
    "contribution_renderer_equals_public="
    + str(contribution_markdown == public_markdown)
  )

  print("")
  print("A. Argument conclusions")
  print("-" * 80)
  for index, argument in enumerate(arguments):
    conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    print(
      f"A{index:02d} role={argument.role.value} "
      f"children={argument.child_argument_indices} "
      f"supporting_blocks={len(argument.supporting_blocks)}"
    )
    if conclusion is not None:
      print("  conclusion " + _step_line(conclusion))

  print("")
  print("B. Definition ownership and disappearance stage")
  print("-" * 80)
  definition_arguments = tuple(
    index
    for index, argument in enumerate(arguments)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    )
  )
  print("definition_arguments=" + repr(definition_arguments))

  definition_steps = tuple(
    proof_step
    for block in blocks
    if block.role.value == "definition"
    for proof_step in block.steps
  )
  print("definition_steps=" + str(len(definition_steps)))

  for proof_step in definition_steps:
    owners = tuple(
      (index, argument.role.value)
      for index, argument in enumerate(arguments)
      if id(proof_step) in _argument_step_ids(argument)
    )
    contribution_owners = tuple(
      (
        item.owner_argument_index,
        item.owner_argument_role.value,
        item.contribution_role.value,
        item.placement.value,
        item.provider_keys,
      )
      for items in contributions
      for item in items
      if item.proof_step is proof_step
    )
    print("definition-step " + _step_line(proof_step))
    print("  argument_owners=" + repr(owners))
    print("  contribution_owners=" + repr(contribution_owners))
    _print_stage_presence(
      "presence",
      proof_step,
      raw_markdown,
      contribution_markdown,
      public_markdown,
    )

  print("")
  print("C. pi_5^3 ownership and final-output route")
  print("-" * 80)
  pi5_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if _looks_like_pi5_3(node.proof_step)
  )
  print("pi5_3_steps=" + str(len(pi5_steps)))

  for proof_step in pi5_steps:
    owners = tuple(
      (index, argument.role.value)
      for index, argument in enumerate(arguments)
      if id(proof_step) in _argument_step_ids(argument)
    )
    contribution_owners = tuple(
      (
        item.owner_argument_index,
        item.owner_argument_role.value,
        item.contribution_role.value,
        item.placement.value,
        item.provider_keys,
      )
      for items in contributions
      for item in items
      if item.proof_step is proof_step
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

    print("pi5_3-step " + _step_line(proof_step))
    print("  argument_owners=" + repr(owners))
    print("  contribution_owners=" + repr(contribution_owners))
    print(
      "  premises="
      + repr(tuple(_step_line(step) for step in premises))
    )
    print(
      "  parents="
      + repr(tuple(_step_line(step) for step in parents))
    )
    _print_stage_presence(
      "presence",
      proof_step,
      raw_markdown,
      contribution_markdown,
      public_markdown,
    )

  print("")
  print("D. Ordered contribution inventory")
  print("-" * 80)
  for index, items in enumerate(contributions):
    print(f"A{index:02d} contribution_count={len(items)}")
    for item in items:
      print(
        "  "
        + _step_line(item.proof_step)
      )
      print(
        "    "
        f"owner=A{item.owner_argument_index:02d}/"
        f"{item.owner_argument_role.value} "
        f"role={item.contribution_role.value} "
        f"placement={item.placement.value} "
        f"providers={item.provider_keys}"
      )

  print("")
  print("E. Final public Narrative")
  print("-" * 80)
  print(public_markdown)
  print("")


def main():
  diagnose(
    "depth=2 presentation",
    2,
  )
  diagnose(
    "full/default presentation",
    None,
  )
  print("=" * 80)
  print("R25-R5 DIAGNOSIS COMPLETE")
  print("No production repair was applied.")
  print("=" * 80)


if __name__ == "__main__":
  main()
