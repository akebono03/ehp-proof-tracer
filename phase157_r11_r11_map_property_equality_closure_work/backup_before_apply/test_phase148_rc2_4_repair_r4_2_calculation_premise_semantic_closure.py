import inspect

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


EQ1 = r"2\nu' = \eta_{3}\eta_{4}\eta_{5}"
EQ2 = (
  r"\eta_{3}\eta_{4}\eta_{5} = "
  r"\eta_{3}^{3}"
)
EQ3 = r"2\nu' = \eta_{3}^{3}"


def _pi6_3_group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _depth2_presentation():
  replay = (
    build_toda_group_result_proof_replay(
      _pi6_3_group_result(),
      max_depth=2,
    )
  )
  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _contains_rendered_fragment(
  presentation,
  fragment,
):
  return any(
    fragment
    in _render_generic_narrative_step(
      node.proof_step
    )
    for node in presentation.nodes
  )


def _rendered_web_text(
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


def test_phase148_rc2_4_repair_r4_2_depth2_closure_adds_direct_equality_calculation_premises():
  presentation = (
    _depth2_presentation()
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  assert not _contains_rendered_fragment(
    presentation,
    EQ1,
  )
  assert not _contains_rendered_fragment(
    presentation,
    EQ2,
  )
  assert _contains_rendered_fragment(
    presentation,
    EQ3,
  )

  assert _contains_rendered_fragment(
    closure,
    EQ1,
  )
  assert _contains_rendered_fragment(
    closure,
    EQ2,
  )
  assert _contains_rendered_fragment(
    closure,
    EQ3,
  )


def test_phase148_rc2_4_repair_r4_2_calculation_closure_is_one_level_only():
  presentation = (
    _depth2_presentation()
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  original_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  closure_ids = {
    id(
      node.proof_step
    )
    for node in closure.nodes
  }
  added_steps = tuple(
    node.proof_step
    for node in closure.nodes
    if id(
      node.proof_step
    ) not in original_ids
  )

  added_equality_steps = tuple(
    step
    for step in added_steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      is RelationType.EQUALITY
    )
  )

  assert any(
    EQ1
    in _render_generic_narrative_step(
      step
    )
    for step in added_equality_steps
  )
  assert any(
    EQ2
    in _render_generic_narrative_step(
      step
    )
    for step in added_equality_steps
  )

  for added_step in added_equality_steps:
    for premise_step in added_step.premises:
      if (
        not isinstance(
          premise_step.conclusion,
          Relation,
        )
        or premise_step.conclusion.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      if id(
        premise_step
      ) in original_ids:
        continue

      assert id(
        premise_step
      ) not in closure_ids


def test_phase148_rc2_4_repair_r4_2_depth2_public_renderer_restores_numbered_chain():
  presentation = (
    _depth2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$"
    in rendered
  )
  assert (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
    in rendered
  )
  assert (
    "(1) と (2) より, "
    in rendered
  )
  assert (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
    in rendered
  )


def test_phase148_rc2_4_repair_r4_2_web_depth2_restores_numbered_chain_without_raw_exactness():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = (
    _rendered_web_text(
      view
    )
  )

  assert r"\tag{1}" in rendered
  assert r"\tag{2}" in rendered
  assert r"\tag{3}" in rendered
  assert "(1) と (2) より, " in rendered
  assert (
    "は完全である"
    not in rendered
  )
  assert (
    r"\text{ is exact}"
    not in rendered
  )


def test_phase148_rc2_4_repair_r4_2_web_depth2_preserves_core_result_and_short_exact_sequence():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = (
    _rendered_web_text(
      view
    )
  )

  assert (
    r"\operatorname{ord}\left(\nu'\right) = 4"
    in rendered
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    in rendered
  )
  assert (
    r"\xrightarrow{E} \pi_{6}^{3}"
    in rendered
  )
  assert (
    r"\xrightarrow{H} \pi_{6}^{5}"
    in rendered
  )
  assert (
    r"\longrightarrow 0"
    in rendered
  )


def test_phase148_rc2_4_repair_r4_2_closure_has_no_pi6_or_rule_name_hardcoding():
  source = inspect.getsource(
    build_toda_group_proof_narrative_semantic_closure_presentation
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "equality transitivity",
    "Toda 5.3 nu-prime",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
