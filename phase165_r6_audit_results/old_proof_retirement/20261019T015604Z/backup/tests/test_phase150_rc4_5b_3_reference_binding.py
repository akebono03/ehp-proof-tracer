import inspect

from expression import HomotopyElement
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeReferenceApplicationSemantic,
  TodaGroupProofNarrativeReferenceIdentity,
  TodaGroupProofNarrativeVariableBinding,
)


def _pi6_data():
  presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(3, 3)
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  return presentation, semantic_sidecar, reason_sidecar


def test_phase150_rc4_5b_3_pi6_has_one_typed_reference_application():
  presentation, semantic_sidecar, reason_sidecar = _pi6_data()
  applications = semantic_sidecar.reference_application_semantics
  assert len(applications) == 1
  application = applications[0]
  assert isinstance(
    application,
    TodaGroupProofNarrativeReferenceApplicationSemantic,
  )
  assert application.reference == TodaGroupProofNarrativeReferenceIdentity(
    label="Lemma 5.2",
  )
  assert len(application.bindings) == 1
  binding = application.bindings[0]
  assert isinstance(binding, TodaGroupProofNarrativeVariableBinding)
  assert isinstance(binding.formal_variable, HomotopyElement)
  assert binding.formal_variable.name == "β"
  assert isinstance(binding.instantiated_expression, HomotopyElement)
  assert binding.instantiated_expression.name == "ν′"


def test_phase150_rc4_5b_3_reference_application_targets_definition_step():
  presentation, semantic_sidecar, reason_sidecar = _pi6_data()
  application = semantic_sidecar.reference_application_semantics[0]
  reason = reason_sidecar.reasons[0]
  assert (
    reason.kind
    is TodaGroupProofNarrativeReasonKind.DEFINITION_APPLICABILITY
  )
  assert application.dependent_step is reason.conclusion_step
  assert reason.reference_application is application


def test_phase150_rc4_5b_3_renderer_uses_typed_reference_and_binding():
  presentation, semantic_sidecar, reason_sidecar = _pi6_data()
  sentence = render_toda_group_proof_narrative_reason_sentence(
    reason_sidecar.reasons[0]
  )
  assert sentence == (
    "この前提条件を満たすので, Lemma 5.2 を適用できる.\n"
    "Lemma 5.2 の $\\beta$ を $\\nu'$ と定めると, "
  )


def test_phase150_rc4_5b_3_other_groups_do_not_invent_reference_application():
  for n, k in ((5, 3), (4, 6), (5, 7), (8, 7), (9, 7)):
    presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(n, k)
    assert semantic_sidecar.reference_application_semantics == ()


def test_phase150_rc4_5b_3_renderer_has_no_specific_branch():
  source = inspect.getsource(
    render_toda_group_proof_narrative_reason_sentence
  )
  for token in (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Lemma 5.2",
    '"β"',
    "'β'",
  ):
    assert token not in source
