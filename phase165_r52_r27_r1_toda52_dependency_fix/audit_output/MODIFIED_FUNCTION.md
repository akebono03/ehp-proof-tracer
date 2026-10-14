# Complete changed function

```python
def build_toda_52_composition_isomorphism_step() -> ProofStep:
  phase49 = _build_phase49_result()

  i = ScalarSymbol(
    name="i",
  )
  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )
  gamma = HomotopyElement(
    name="γ",
    dimension=i,
    source=i,
    target=3,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=1,
  )
  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=3,
  )
  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=2,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        first_summand,
        second_summand,
      ),
    ),
    target_group=target_group,
    alpha=eta_2,
    beta=beta,
    gamma=gamma,
    formula=Sum(
      left=Suspension(
        expression=beta,
      ),
      right=Composition(
        left=eta_2,
        right=gamma,
      ),
    ),
  )

  phase50 = _build_phase50_result()
  eta2_definition_steps = tuple(
    step
    for step in phase50["premise_steps"]
    if isinstance(step.conclusion, TodaPi32Eta2DefinitionStatement)
  )
  if len(eta2_definition_steps) != 1:
    raise ValueError(
      "expected exactly one existing eta2 definition source step"
    )

  premise_steps = (
    phase49[
      "premise_steps"
    ]
    + eta2_definition_steps
    + (
      create_legacy_given_proof_step(
        conclusion=ScalarGreaterEqualStatement(
          left=i,
          right=3,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      create_legacy_given_proof_step(
        conclusion=decomposition_map,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  rules = (
    phase49[
      "rules"
    ]
    + (
      toda_pi_i_minus_1_1_zero_inference_rule(),
      toda_prop44_eta2_n2_isomorphism_inference_rule(),
      toda_prop44_eta2_second_summand_restriction_inference_rule(),
      toda_52_eta2_composition_isomorphism_inference_rule(),
    )
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda52CompositionIsomorphismStatement,
    ),
    "Toda (5.2) composition isomorphism",
  )

```
