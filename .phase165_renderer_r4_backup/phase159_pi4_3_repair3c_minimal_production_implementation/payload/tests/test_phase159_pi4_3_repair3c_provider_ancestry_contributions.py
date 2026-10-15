from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  _necessity_for_chain,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
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
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def _phase159_repair3c_context():
  report = build_standard_toda_report(
    n=3,
    k=1,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
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
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      sidecar,
      arguments,
    )
  )
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  return (
    presentation,
    sidecar,
    blocks,
    arguments,
    proof_chains,
    base_markdown,
  )


def test_phase159_repair3c_pi4_3_upstream_steps_enter_chain_and_necessity():
  (
    presentation,
    sidecar,
    blocks,
    arguments,
    proof_chains,
    _base_markdown,
  ) = _phase159_repair3c_context()

  argument = arguments[0]
  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
    )
  )
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  assert conclusion_step is not None

  (
    chain_ids,
    _anchors,
    _distances,
    necessity,
  ) = _necessity_for_chain(
    presentation,
    local_body,
    proof_chains[0],
    conclusion_step,
  )

  target_types = (
    TodaDeltaImageUpToSignStatement,
    TodaDeltaImageFreeCyclicStatement,
    TodaSuspensionKernelFreeCyclicStatement,
    TodaSuspensionSurjectiveStatement,
  )
  target_steps = tuple(
    step
    for block in local_body
    for step in block.steps
    if isinstance(
      step.conclusion,
      target_types,
    )
  )

  assert {
    type(step.conclusion)
    for step in target_steps
  } == set(target_types)

  for step in target_steps:
    step_id = id(step)
    assert step_id in chain_ids
    assert necessity.get(
      step_id,
      (),
    )


def test_phase159_repair3c_pi4_3_image_and_kernel_have_semantic_rendering():
  (
    presentation,
    _sidecar,
    _blocks,
    _arguments,
    _proof_chains,
    _base_markdown,
  ) = _phase159_repair3c_context()

  rendered_by_type = {
    type(node.proof_step.conclusion):
      _render_generic_narrative_step(
        node.proof_step
      )
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      (
        TodaDeltaImageFreeCyclicStatement,
        TodaSuspensionKernelFreeCyclicStatement,
      ),
    )
  }

  assert rendered_by_type[
    TodaDeltaImageFreeCyclicStatement
  ] == (
    r"$\operatorname{Im}\Delta = "
    r"\mathbb{Z}\{2\eta_{2}\}$."
  )
  assert rendered_by_type[
    TodaSuspensionKernelFreeCyclicStatement
  ] == (
    r"$\ker E = "
    r"\mathbb{Z}\{2\eta_{2}\}$."
  )


def test_phase159_repair3c_pi4_3_ordered_contributions_expose_body_chain():
  (
    presentation,
    sidecar,
    blocks,
    arguments,
    proof_chains,
    base_markdown,
  ) = _phase159_repair3c_context()

  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )

  assert len(ordered) == 1

  rendered = tuple(
    _render_generic_narrative_step(
      contribution.proof_step
    )
    for contribution in ordered[0]
  )

  direct_delta = (
    r"$\Delta\left(\iota_{5}\right) = "
    r"\pm 2\eta_{2}$"
  )
  image_delta = (
    r"$\operatorname{Im}\Delta = "
    r"\mathbb{Z}\{2\eta_{2}\}$."
  )
  kernel_e = (
    r"$\ker E = "
    r"\mathbb{Z}\{2\eta_{2}\}$."
  )
  e_surjective = (
    r"$E: \pi_{3}^{2} \to "
    r"\pi_{4}^{3}$ は全射である."
  )

  for expected in (
    direct_delta,
    image_delta,
    kernel_e,
    e_surjective,
  ):
    assert expected in rendered

  assert (
    rendered.index(direct_delta)
    < rendered.index(image_delta)
    < rendered.index(kernel_e)
  )
