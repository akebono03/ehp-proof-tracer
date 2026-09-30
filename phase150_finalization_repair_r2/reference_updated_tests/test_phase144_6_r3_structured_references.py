from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
)


def test_phase144_6_r3_inference_rule_preserves_structured_literature_reference():
  reference = LiteratureReference(
    label="Toda Prop.5.1",
    author="H. Toda",
    title="Composition Methods in Homotopy Groups of Spheres",
    year=1962,
    locator="Proposition 5.1",
  )
  rule = InferenceRule(
    name="test rule",
    literature_reference=reference,
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  assert (
    extract_toda_group_proof_step_literature_reference(step)
    is reference
  )


def test_phase144_6_r3_rule_name_reference_is_inferred_without_structured_reference():
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="Toda Proposition 5.1 text only",
    ),
  )

  reference = extract_toda_group_proof_step_literature_reference(step)

  assert reference is not None
  assert reference.label == "Toda Proposition 5.1"
  assert reference.locator == "Proposition 5.1"


def test_phase144_6_r3_reference_renderer_uses_structured_locator_not_rule_name():
  reference = LiteratureReference(
    label="Toda Prop.5.1",
    locator="Proposition 5.1",
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="internal implementation name",
      literature_reference=reference,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(step,),
  )

  rendered = render_toda_group_proof_narrative_reference_entries_markdown(
    (entry,)
  )

  assert "**[R1] Proposition 5.1.**" in rendered
  assert "internal implementation name" not in rendered
