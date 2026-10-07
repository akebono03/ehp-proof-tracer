def _build_nu_squared_aggregate_step(
  context: dict[
    str,
    ProofStep,
  ],
  delta_injectivity_steps: tuple[
    ProofStep,
    ProofStep,
    ProofStep,
  ],
  pi10_4_step: ProofStep,
  delta_nu9_step: ProofStep,
  delta_eta11_squared_zero_step: ProofStep,
  delta_eta13_zero_step: ProofStep,
) -> ProofStep:
  n4_step, n5_step, n6_step = (
    delta_injectivity_steps
  )

  pi11_5_step = _build_pi11_5_step(
    context,
    n4_step,
    pi10_4_step,
    delta_nu9_step,
  )

  pi12_6_step = _build_pi12_6_step(
    context,
    n5_step,
    delta_eta11_squared_zero_step,
    pi11_5_step,
  )

  pi13_7_step = _build_pi13_7_step(
    context,
    n6_step,
    delta_eta13_zero_step,
    pi12_6_step,
  )

  pi14_8_step = _apply(
    toda_prop511_pi14_8_nu8_squared_inference_rule(),
    (
      pi13_7_step,
      _build_pi14_8_suspension_isomorphism_step(),
    ),
    "pi_14^8",
  )

  n = ScalarSymbol(
    name="n",
  )
  n_ge_9_step = _given(
    ScalarGreaterEqualStatement(
      left=n,
      right=9,
    )
  )

  stable_isomorphism_step = (
    build_toda_45_stable_isomorphism_step(
      n=8,
      k=6,
      m=n,
    )
  )

  stable_result = (
    run_inference_until_stable_with_history(
      (
        toda_45_generic_finite_cyclic_transport_inference_rule(),
        toda_nu_squared_transport_generator_normalization_inference_rule(),
      ),
      (
        pi14_8_step,
        stable_isomorphism_step,
        n_ge_9_step,
      ),
    )
  )

  expected_target = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=6,
    ),
    sphere_dimension=n,
  )

  higher_step = next(
    step
    for step in stable_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == expected_target
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and isinstance(
        step.conclusion.rhs.generator,
        Composition,
      )
    )
  )

  return _apply(
    toda_prop511_nu_squared_finite_dimensional_integration_inference_rule(),
    (
      pi11_5_step,
      pi12_6_step,
      pi13_7_step,
      pi14_8_step,
      higher_step,
      n_ge_9_step,
    ),
    "Prop.5.11 nu-squared aggregate",
  )
