from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toda_prop56_zero_bootstrap.py"
TEST = ROOT / "tests" / "test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py"

NEW_FUNCTION = 'def _build_prop51_step() -> ProofStep:\n  phase49 = _build_phase49_result()\n  phase50 = _build_phase50_result()\n\n  pi3_2_step = _find_unique_step(\n    phase49[\n      "result"\n    ].steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and step.conclusion.lhs\n      == TodaPrimaryGroup(\n        group_dimension=3,\n        sphere_dimension=2,\n      )\n      and isinstance(\n        step.conclusion.rhs,\n        FreeCyclicGroup,\n      )\n    ),\n    "pi_3^2",\n  )\n\n  eta2_hopf_step = _find_unique_step(\n    phase49[\n      "result"\n    ].steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and isinstance(\n        step.conclusion.lhs,\n        MapApplication,\n      )\n      and step.conclusion.lhs.map\n      == EHP_H_MAP\n      and getattr(\n        step.conclusion.lhs.expression,\n        "name",\n        None,\n      )\n      == "η₂"\n    ),\n    "H(eta_2)",\n  )\n\n  delta_step = _find_unique_step(\n    phase50[\n      "result"\n    ].steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        TodaDeltaImageUpToSignStatement,\n      )\n      and isinstance(\n        step.conclusion.positive_value,\n        Multiple,\n      )\n      and step.conclusion.positive_value.coefficient\n      == 2\n      and (\n        step.inference_rule\n        is not None\n      )\n      and (\n        step.inference_rule\n        .literature_reference\n        is not None\n      )\n      and (\n        step.inference_rule\n        .literature_reference\n        .locator\n        == "Proposition 5.1"\n      )\n    ),\n    "Delta(iota_5)=+-2eta_2",\n  )\n\n  n = ScalarSymbol(\n    name="n",\n  )\n\n  stable_step = build_toda_45_stable_isomorphism_step(\n    n=3,\n    k=1,\n    m=n,\n  )\n\n  transported_result = (\n    run_inference_until_stable_with_history(\n      toda_45_pi4_3_finite_cyclic_transport_inference_rule(),\n      (\n        phase50[\n          "final_group_step"\n        ],\n        stable_step,\n      ),\n    )\n  )\n\n  transported_step = _find_unique_step(\n    transported_result.steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and step.conclusion.lhs\n      == TodaPrimaryGroup(\n        group_dimension=ScalarSum(\n          left=n,\n          right=1,\n        ),\n        sphere_dimension=n,\n      )\n    ),\n    "higher eta transported group",\n  )\n\n  eta_n_definition_step = ProofStep(\n    conclusion=toda_eta_family_definition_statement(\n      n\n    ),\n    premises=(),\n    rule=ProofRule.GIVEN,\n  )\n\n  eta3_definition_step = ProofStep(\n    conclusion=toda_eta_family_definition_statement(\n      3\n    ),\n    premises=(),\n    rule=ProofRule.GIVEN,\n  )\n\n  eta3_result = run_inference_until_stable_with_history(\n    toda_eta3_suspension_relation_inference_rule(),\n    (\n      eta3_definition_step,\n    ),\n  )\n\n  eta3_relation_step = _find_unique_step(\n    eta3_result.steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and step.conclusion.lhs\n      == eta3_definition_step.conclusion.element\n    ),\n    "eta_3 suspension relation",\n  )\n\n  higher_bridge_result = (\n    run_inference_until_stable_with_history(\n      toda_higher_eta_family_bridge_inference_rule(),\n      (\n        eta_n_definition_step,\n        eta3_relation_step,\n      ),\n    )\n  )\n\n  higher_bridge_step = _find_unique_step(\n    higher_bridge_result.steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and step.conclusion.rhs\n      == eta_n_definition_step.conclusion.element\n    ),\n    "higher eta bridge",\n  )\n\n  higher_result = run_inference_until_stable_with_history(\n    toda_higher_eta_finite_cyclic_generator_inference_rule(),\n    (\n      transported_step,\n      higher_bridge_step,\n    ),\n  )\n\n  higher_step = _find_unique_step(\n    higher_result.steps,\n    lambda step: (\n      isinstance(\n        step.conclusion,\n        Relation,\n      )\n      and step.conclusion.lhs\n      == transported_step.conclusion.lhs\n      and isinstance(\n        step.conclusion.rhs,\n        FiniteCyclicGroup,\n      )\n      and step.conclusion.rhs.generator\n      == eta_n_definition_step.conclusion.element\n    ),\n    "higher eta group",\n  )\n\n  expected = TodaProp51FiniteDimensionalStatement(\n    pi3_2_group_relation=pi3_2_step.conclusion,\n    eta2_hopf_relation=eta2_hopf_step.conclusion,\n    delta_iota5_relation=delta_step.conclusion,\n    higher_eta_group_relation=higher_step.conclusion,\n  )\n\n  result = run_inference_until_stable_with_history(\n    toda_prop51_finite_dimensional_integration_inference_rule(),\n    (\n      pi3_2_step,\n      eta2_hopf_step,\n      delta_step,\n      higher_step,\n    ),\n  )\n\n  return _find_unique_step(\n    result.steps,\n    lambda step: step.conclusion == expected,\n    "Toda Proposition 5.1",\n  )\n'
TEST_TEXT = 'from expression import (\n  Multiple,\n)\nfrom standard_production_repository import (\n  build_standard_production_proof_repository,\n)\nfrom toda_prop56_zero_bootstrap import (\n  _build_prop51_step,\n)\nfrom toda_rules import (\n  TodaDeltaImageUpToSignStatement,\n  TodaProp51FiniteDimensionalStatement,\n)\n\n\ndef test_phase159_repair1c_prop51_builder_uses_direct_phase50_delta():\n  prop51_step = _build_prop51_step()\n\n  assert isinstance(\n    prop51_step.conclusion,\n    TodaProp51FiniteDimensionalStatement,\n  )\n\n  delta_relation = (\n    prop51_step\n    .conclusion\n    .delta_iota5_relation\n  )\n\n  assert isinstance(\n    delta_relation,\n    TodaDeltaImageUpToSignStatement,\n  )\n  assert isinstance(\n    delta_relation.positive_value,\n    Multiple,\n  )\n  assert (\n    delta_relation\n    .positive_value\n    .coefficient\n    == 2\n  )\n\n  delta_premises = tuple(\n    premise\n    for premise in prop51_step.premises\n    if isinstance(\n      premise.conclusion,\n      TodaDeltaImageUpToSignStatement,\n    )\n  )\n\n  assert len(\n    delta_premises\n  ) == 1\n\n  delta_step = (\n    delta_premises[0]\n  )\n\n  assert (\n    delta_step.inference_rule\n    is not None\n  )\n  assert (\n    delta_step\n    .inference_rule\n    .literature_reference\n    is not None\n  )\n  assert (\n    delta_step\n    .inference_rule\n    .literature_reference\n    .locator\n    == "Proposition 5.1"\n  )\n\n\ndef test_phase159_repair1c_standard_production_repository_builds():\n  repository = (\n    build_standard_production_proof_repository()\n  )\n\n  assert repository is not None\n'


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8"
  )

  start_marker = (
    "def _build_prop51_step() -> ProofStep:"
  )
  end_marker = (
    "\ndef _build_n3_suspension_isomorphism_step("
  )

  start = source.find(
    start_marker
  )
  if start < 0:
    raise RuntimeError(
      "_build_prop51_step() not found"
    )

  end = source.find(
    end_marker,
    start,
  )
  if end < 0:
    raise RuntimeError(
      "_build_prop51_step() end boundary not found"
    )

  updated = (
    source[:start]
    + NEW_FUNCTION
    + source[end:]
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair1c applied."
  )
  print(
    "Changed: toda_prop56_zero_bootstrap.py"
  )
  print(
    "Changed function: _build_prop51_step()"
  )
  print(
    "Added: tests/"
    "test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
