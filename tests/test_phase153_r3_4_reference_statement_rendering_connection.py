from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
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


def _phase153_r3_4_pi10_6_presentation():
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def test_phase153_r3_4_reference_renderer_accepts_statement_lines_without_breaking_old_api():
  reference = LiteratureReference(
    label="Toda test",
    locator="Proposition X",
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="test rule",
      literature_reference=reference,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      step,
    ),
  )

  legacy = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      (
        entry,
      )
    )
  )
  connected = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      (
        entry,
      ),
      {
        1: (
          "$A = B$",
        ),
      },
    )
  )

  assert legacy == (
    "使用する結果を先にまとめる.\n\n"
    "**[R1] Proposition X.**"
  )
  assert connected == (
    "使用する結果を先にまとめる.\n\n"
    "**[R1] Proposition X.**\n"
    "$A = B$"
  )


def test_phase153_r3_4_pi10_6_builds_selected_reference_statement_lines():
  presentation = (
    _phase153_r3_4_pi10_6_presentation()
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  r2 = next(
    entry
    for entry in entries
    if entry.reference.locator == "(4.5)"
  )

  assert r2.number in statement_lines
  assert statement_lines[
    r2.number
  ]
  assert any(
    "同型" in line
    or r"\cong" in line
    for line in statement_lines[
      r2.number
    ]
  )


def test_phase153_r3_4_public_pi10_6_reference_section_contains_r2_statement():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )

  reference_title = "**[R2] (4.5).**"
  title_index = rendered.index(
    reference_title
  )
  body_reference_index = rendered.index(
    "[R2] により、"
  )

  between = rendered[
    title_index
    + len(
      reference_title
    ):
    body_reference_index
  ]

  assert "同型" in between or r"\cong" in between


def test_phase153_r3_4_does_not_render_internal_fallback_name_in_reference_section():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )
  reference_section = rendered.split(
    "[R2] により、",
    1,
  )[0]

  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in reference_section
  )
