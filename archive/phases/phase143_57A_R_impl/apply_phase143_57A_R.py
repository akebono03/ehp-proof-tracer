from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEST_PATH = (
  ROOT
  / "tests"
  / "test_phase143_57a_step_calculation_chain.py"
)

OLD = r'''def test_phase143_57a_transition_validates_step_types():
  step = ProofStep(
    conclusion="source",
  )

  with pytest.raises(
    TypeError,
    match="target_step must be a ProofStep",
  ):
    TodaGroupProofNarrativeStepTransition(
      role=(
        TodaGroupProofNarrativeStepTransitionRole
        .CALCULATION_CHAIN
      ),
      source_step=step,
      target_step="target",
    )
'''

NEW = r'''def test_phase143_57a_transition_validates_step_types():
  (
    presentation,
    _blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  step = presentation.nodes[
    0
  ].proof_step

  assert isinstance(
    step,
    ProofStep,
  )

  with pytest.raises(
    TypeError,
    match="target_step must be a ProofStep",
  ):
    TodaGroupProofNarrativeStepTransition(
      role=(
        TodaGroupProofNarrativeStepTransitionRole
        .CALCULATION_CHAIN
      ),
      source_step=step,
      target_step="target",
    )
'''


def main() -> None:
  text = TEST_PATH.read_text(
    encoding="utf-8"
  )

  if OLD not in text:
    raise RuntimeError(
      "expected Phase 143-57A test function "
      "was not found; no file was changed"
    )

  updated = text.replace(
    OLD,
    NEW,
    1,
  )
  TEST_PATH.write_text(
    updated,
    encoding="utf-8",
  )
  print(
    f"updated {TEST_PATH}"
  )


if __name__ == "__main__":
  main()
