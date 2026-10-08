from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def _phase161_r4_r5_repair11_data():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  return (
    raw,
    presentation,
  )


def test_phase161_r4_r5_repair11_uses_prop51_component_as_linkage_source():
  _, presentation = (
    _phase161_r4_r5_repair11_data()
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  sources_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )

  prop51_component_entry = next(
    entry
    for entry in entries
    if (
      entry.reference.locator
      == "Proposition 5.1"
      and any(
        (
          step.inference_rule is not None
          and step.inference_rule.name
          == "Toda Proposition 5.1 higher eta group relation"
        )
        for step in entry.proof_steps
      )
    )
  )

  prop51_sources = sources_by_number[
    prop51_component_entry.number
  ]

  assert any(
    (
      step.inference_rule is not None
      and step.inference_rule.name
      == "Toda Proposition 5.1 higher eta group relation"
    )
    for step in prop51_sources
  )


def test_phase161_r4_r5_repair11_public_prop51_links_to_concrete_pi4_3():
  raw, _ = (
    _phase161_r4_r5_repair11_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert "**[R2] Proposition 5.1.**" in reference

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in body
  )

  pi4_3_paragraph = next(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert "[R2]" in pi4_3_paragraph
  assert (
    pi4_3_paragraph.count(
      "[R2]"
    )
    == 1
  )


def test_phase161_r4_r5_repair11_keeps_pi4_2_contract():
  raw, _ = (
    _phase161_r4_r5_repair11_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 4.4" not in reference
  assert "[R2]より, [R1]より" not in body

  assert "$i=4$" in body
  assert (
    r"\pi_{4}^{3} \to \pi_{4}^{2}"
    in body
  )
  assert (
    r"\eta_{3} \mapsto "
    r"\eta_{2}\eta_{3}"
    in body
  )
  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
