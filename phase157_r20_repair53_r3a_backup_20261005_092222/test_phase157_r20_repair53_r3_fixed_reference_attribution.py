from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
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
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
)


RULE_NAME = (
  "Toda Proposition 5.15 sigma_8 n=8 "
  "Proposition 4.4 decomposition specialization"
)


def _repair53_r3_data():
  report = build_standard_toda_report(
    n=8,
    k=7,
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

  prop44_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        TodaProp44IsomorphismStatement,
      )
      and node.proof_step.inference_rule is not None
      and node.proof_step.inference_rule.name
      == RULE_NAME
    )
  )

  return (
    raw,
    presentation,
    prop44_step,
  )


def test_phase157_r20_repair53_r3_n8_prop44_is_fixed_statement():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  boundary = classify_toda_literature_statement_step(
    prop44_step
  )

  assert boundary is not None
  assert (
    boundary.classification
    == TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert (
    boundary.reference_locator
    == "Proposition 4.4"
  )
  assert (
    boundary.component_key
    == "nu4_decomposition_isomorphism"
  )


def test_phase157_r20_repair53_r3_reference_identity_uses_prop44():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  reference = (
    extract_toda_group_proof_step_literature_reference(
      prop44_step
    )
  )

  assert reference is not None
  assert reference.locator == "Proposition 4.4"
  assert reference.label == "Toda Proposition 4.4"


def test_phase157_r20_repair53_r3_graph_entries_split_prop44_from_prop515():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  locators = tuple(
    entry.reference.locator
    for entry in entries
  )

  assert "Proposition 4.4" in locators
  assert "Proposition 5.15" in locators

  prop44_entry = next(
    entry
    for entry in entries
    if entry.reference.locator
    == "Proposition 4.4"
  )

  assert prop44_step in prop44_entry.proof_steps


def test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  assert "Toda Proposition 4.4 の分解同型" in rendered
  assert "Proposition 5.15" in rendered
  assert (
    r"\pi_{14}^{7} = "
    r"\mathbb{Z}/8\{\sigma'\}"
    in rendered
  )
  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )


def test_phase157_r20_repair53_r3_fragment_normalization_remains_active():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  assert "である." not in paragraphs
  assert "を得る." not in paragraphs
