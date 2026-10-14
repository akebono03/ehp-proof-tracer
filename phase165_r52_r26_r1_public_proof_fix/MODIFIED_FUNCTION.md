# _build_prop51_step() — full installed function

```python
def _build_prop51_step() -> ProofStep:
  phase49 = _build_phase49_result()
  phase50 = _build_phase50_result()

  # phase165_r52_r26_r1_shared_pi32_lookup
  # The pi3^2 proof is regenerated using common typed inference rules.
  # This does not reintroduce any pi3^2-specific rule or GIVEN result.
  from pathlib import Path
  from hopf_facts import ETA_2
  from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
  from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
  from phase165_r52_partial_proof import ProofSearchStatus
  adopted_path = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
  adopted_bridge = build_shared_typed_bridge(
    sources=(build_adopted_typed_reference_registry(adopted_path),),
  )
  pi32_search = search_shared_group_goal(
    n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=adopted_bridge,
  )
  if pi32_search.status is not ProofSearchStatus.COMPLETE:
    raise ValueError("shared pi_3^2 proof is incomplete")
  if not any(step.rule is ProofRule.INFERENCE for step in pi32_search.proven_steps):
    raise ValueError("shared pi_3^2 result has no inferred ProofStep")

  pi3_2_step = _find_unique_step(
    pi32_search.proven_steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=2,
      )
      and isinstance(
        step.conclusion.rhs,
        FreeCyclicGroup,
      )
    ),
    "pi_3^2",
  )

  eta2_hopf_step = _find_unique_step(
    phase49[
      "result"
    ].steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_H_MAP
      and getattr(
        step.conclusion.lhs.expression,
        "name",
        None,
      )
      == "η₂"
    ),
    "H(eta_2)",
  )

  delta_step = _find_unique_step(
    phase50[
      "result"
    ].steps,
    lambda step: (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and isinstance(
        step.conclusion.positive_value,
        Multiple,
      )
      and step.conclusion.positive_value.coefficient
      == 2
      and (
        step.inference_rule
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        .locator
        == "Proposition 5.1"
      )
    ),
    "Delta(iota_5)=+-2eta_2",
  )

  n = ScalarSymbol(
    name="n",
  )

  stable_step = build_toda_45_stable_isomorphism_step(
    n=3,
    k=1,
    m=n,
  )

  transported_result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        phase50[
          "final_group_step"
        ],
        stable_step,
      ),
    )
  )

  transported_step = _find_unique_step(
    transported_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
    ),
    "higher eta transported group",
  )

  eta_n_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      n
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta3_definition_step = create_legacy_given_proof_step(
    conclusion=toda_eta_family_definition_statement(
      3
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta3_result = run_inference_until_stable_with_history(
    toda_eta3_suspension_relation_inference_rule(),
    (
      eta3_definition_step,
    ),
  )

  eta3_relation_step = _find_unique_step(
    eta3_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == eta3_definition_step.conclusion.element
    ),
    "eta_3 suspension relation",
  )

  higher_bridge_result = (
    run_inference_until_stable_with_history(
      toda_higher_eta_family_bridge_inference_rule(),
      (
        eta_n_definition_step,
        eta3_relation_step,
      ),
    )
  )

  higher_bridge_step = _find_unique_step(
    higher_bridge_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.rhs
      == eta_n_definition_step.conclusion.element
    ),
    "higher eta bridge",
  )

  higher_result = run_inference_until_stable_with_history(
    toda_higher_eta_finite_cyclic_generator_inference_rule(),
    (
      transported_step,
      higher_bridge_step,
    ),
  )

  higher_step = _find_unique_step(
    higher_result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == transported_step.conclusion.lhs
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.generator
      == eta_n_definition_step.conclusion.element
    ),
    "higher eta group",
  )

  expected = TodaProp51FiniteDimensionalStatement(
    pi3_2_group_relation=pi3_2_step.conclusion,
    eta2_hopf_relation=eta2_hopf_step.conclusion,
    delta_iota5_relation=delta_step.conclusion,
    higher_eta_group_relation=higher_step.conclusion,
  )

  result = run_inference_until_stable_with_history(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    (
      pi3_2_step,
      eta2_hopf_step,
      delta_step,
      higher_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: step.conclusion == expected,
    "Toda Proposition 5.1",
  )

```
