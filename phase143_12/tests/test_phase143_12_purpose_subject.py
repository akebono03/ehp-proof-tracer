import pytest

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def _arguments(n: int, k: int):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(group_result, max_depth=3)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  return build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )


@pytest.mark.parametrize("n,k", ((3, 3), (5, 3), (8, 7), (9, 7)))
def test_phase143_12_group_structure_subject_is_extracted(n, k):
  argument = next(
    argument for argument in _arguments(n, k)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
  )
  subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
  assert subject is not None
  assert subject.group_dimension == n + k
  assert subject.sphere_dimension == n


def test_phase143_12_pi6_3_order_subject_is_nu_prime():
  argument = next(
    argument for argument in _arguments(3, 3)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
  )
  subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
  assert subject is not None
  assert subject.name == "ν′"


def test_phase143_12_pi8_5_definition_subject_is_nu5():
  argument = next(
    argument for argument in _arguments(5, 3)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
  )
  subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
  assert subject is not None
  assert subject.name in ("ν₅", "ν_5")


def test_phase143_12_pi16_9_definition_subject_is_sigma9():
  argument = next(
    argument for argument in _arguments(9, 7)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
  )
  subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
  assert subject is not None
  assert subject.name in ("σ₉", "σ_9")


def test_phase143_12_rejects_non_argument():
  with pytest.raises(
    TypeError,
    match="argument must be a TodaGroupProofNarrativeArgument",
  ):
    extract_toda_group_proof_narrative_argument_purpose_subject(object())
