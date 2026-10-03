import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_owned_step_ids,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


def _data(
  depth: int,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  reasons = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  empty_lines = {
    entry.number: ()
    for entry in entries
  }
  entries, _ = exclude_toda_group_proof_narrative_root_reference(
    entries,
    empty_lines,
    presentation.root_step,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  return (
    presentation,
    arguments,
    reasons,
    entries,
    rendered,
  )


def test_phase156_r5_repair8_unreferenced_definition_step_is_reference_owned():
  (
    presentation,
    arguments,
    reasons,
    entries,
    rendered,
  ) = _data(
    2
  )

  owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      entries,
    )
  )

  definition_reason = next(
    reason
    for reason in reasons.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )

  assert id(
    definition_reason.conclusion_step
  ) in owned_step_ids
  assert (
    definition_reason.conclusion_step.inference_rule
    is None
  )

  definition_argument = next(
    argument
    for argument in arguments
    if (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      is definition_reason.conclusion_step
    )
  )

  assert id(
    extract_toda_group_proof_narrative_argument_conclusion_step(
      definition_argument
    )
  ) in owned_step_ids


def test_phase156_r5_repair8_different_explicit_reference_is_not_absorbed_into_53():
  (
    presentation,
    arguments,
    reasons,
    entries,
    rendered,
  ) = _data(
    2
  )

  definition_reason = next(
    reason
    for reason in reasons.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )
  precondition = definition_reason.premise_steps[
    0
  ]
  reference = (
    precondition
    .inference_rule
    .literature_reference
  )

  assert reference is not None
  assert reference.locator == "Proposition 5.1"


def test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth2():
  rendered = _data(
    2
  )[
    -1
  ]

  body_marker = (
    "次に, $\\nu'$ の位数を決定するために"
  )
  body_index = rendered.find(
    body_marker
  )

  assert body_index >= 0
  body = rendered[
    body_index:
  ]

  assert "(5.3)" in rendered[
    :body_index
  ]
  assert "Lemma 5.2.**" not in rendered[
    :body_index
  ]
  assert "Lemma 5.2" not in body
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in body
  )
  assert "$2\\eta_{3} = 0$" not in body
  assert "$\\nu'$ を定める." not in body


def test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth3():
  rendered = _data(
    3
  )[
    -1
  ]

  body_marker = (
    "次に, $\\nu'$ の位数を決定するために"
  )
  body_index = rendered.find(
    body_marker
  )

  assert body_index >= 0
  body = rendered[
    body_index:
  ]

  assert "(5.3)" in rendered[
    :body_index
  ]
  assert "Lemma 5.2.**" not in rendered[
    :body_index
  ]
  assert "Lemma 5.2" not in body
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in body
  )
  assert "$2\\eta_{3} = 0$" not in body
  assert "$\\nu'$ を定める." not in body


def test_phase156_r5_repair8_53_reference_keeps_public_consequences():
  rendered = _data(
    2
  )[
    -1
  ]
  reference_part = rendered.split(
    "まず",
    1,
  )[0]
  section = next(
    part
    for part in re.split(
      r"(?=\*\*\[R\d+\] )",
      reference_part,
    )
    if re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      part,
    )
  )

  assert "\\nu' \\in \\pi_{6}^{3}" in section
  assert "2\\nu'" in section
