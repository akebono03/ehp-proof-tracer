from proof import (
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _dummy_step(
  value,
):
  return ProofStep(
    conclusion=value,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _pi6_2_rendered():
  report = build_standard_toda_report(
    n=2,
    k=4,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase153_r10_filters_unused_entries_and_renumbers_markers():
  entries = (
    TodaGroupProofNarrativeReferenceEntry(
      number=1,
      reference=LiteratureReference(
        label="Toda Lemma 1.1",
        locator="Lemma 1.1",
      ),
      proof_steps=(
        _dummy_step(
          "unused",
        ),
      ),
    ),
    TodaGroupProofNarrativeReferenceEntry(
      number=2,
      reference=LiteratureReference(
        label="Toda Proposition 2.2",
        locator="Proposition 2.2",
      ),
      proof_steps=(
        _dummy_step(
          "used-a",
        ),
      ),
    ),
    TodaGroupProofNarrativeReferenceEntry(
      number=3,
      reference=LiteratureReference(
        label="Toda Equation (3.3)",
        locator="(3.3)",
      ),
      proof_steps=(
        _dummy_step(
          "used-b",
        ),
      ),
    ),
    TodaGroupProofNarrativeReferenceEntry(
      number=4,
      reference=LiteratureReference(
        label="Toda Proposition 4.4",
        locator="Proposition 4.4",
      ),
      proof_steps=(
        _dummy_step(
          "unused-b",
        ),
      ),
    ),
  )
  statement_lines = {
    2: (
      "statement-a",
    ),
    3: (
      "statement-b",
    ),
  }

  filtered_entries, filtered_lines, filtered_body = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      entries,
      statement_lines,
      "まず、[R2]を用いる。\nさらに、[R3]を用いる。",
    )
  )

  assert tuple(
    entry.reference.locator
    for entry in filtered_entries
  ) == (
    "Proposition 2.2",
    "(3.3)",
  )
  assert tuple(
    entry.number
    for entry in filtered_entries
  ) == (
    1,
    2,
  )
  assert filtered_lines == {
    1: (
      "statement-a",
    ),
    2: (
      "statement-b",
    ),
  }
  assert filtered_body == (
    "まず、[R1]を用いる。\n"
    "さらに、[R2]を用いる。"
  )


def test_phase153_r10_pi6_2_keeps_only_used_references():
  rendered = _pi6_2_rendered()

  assert "**[R1] Proposition 5.6.**" in rendered
  assert "**[R2] (5.2).**" in rendered

  assert "Lemma 5.7" not in rendered
  assert "Proposition 4.4" not in rendered

  assert "**[R3]" not in rendered
  assert "**[R4]" not in rendered


def test_phase153_r10_pi6_2_body_uses_renumbered_references():
  rendered = _pi6_2_rendered()
  marker = "## 証明\n\n"
  body = rendered.split(
    marker,
    1,
  )[1]

  assert "[R1]を用いる。" in body
  assert "[R2]を用いる。" in body
  assert "[R3]" not in body
  assert "[R4]" not in body

  assert (
    r"\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}"
    in body
  )
