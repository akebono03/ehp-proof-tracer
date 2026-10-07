def toda_nu_squared_transport_generator_normalization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )
    higher_range = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      transported_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      transported_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      transported_relation.rhs.order
      != 2
    ):
      return False

    n = (
      transported_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_range.left
      != n
      or higher_range.right
      != 9
    ):
      return False

    if (
      transported_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=6,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    generator = (
      transported_relation
      .rhs
      .generator
    )

    if not isinstance(
      generator,
      IteratedSuspension,
    ):
      return False

    source_generator = (
      generator.expression
    )

    if not isinstance(
      source_generator,
      Composition,
    ):
      return False

    left_symbol = getattr(
      source_generator.left,
      "generator",
      None,
    )
    right_symbol = getattr(
      source_generator.right,
      "generator",
      None,
    )

    if (
      left_symbol
      != GeneratorSymbol(
        family="ν",
        index=8,
      )
      or right_symbol
      != GeneratorSymbol(
        family="ν",
        index=11,
      )
    ):
      return False

    return (
      generator.exponent
      == ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=8,
        ),
      )
    )

  def build_conclusion(
    premises,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )
    n = (
      transported_relation
      .lhs
      .sphere_dimension
    )
    n_plus_three = ScalarSum(
      left=n,
      right=3,
    )
    n_plus_six = ScalarSum(
      left=n,
      right=6,
    )

    nu_n = HomotopyElement(
      name="ν_n",
      dimension=n,
      source=n_plus_three,
      target=n,
      generator=GeneratorSymbol(
        family="ν",
        index=n,
      ),
    )
    nu_n_plus_three = HomotopyElement(
      name="ν_(n+3)",
      dimension=n_plus_three,
      source=n_plus_six,
      target=n_plus_three,
      generator=GeneratorSymbol(
        family="ν",
        index=n_plus_three,
      ),
    )

    return Relation(
      lhs=transported_relation.lhs,
      rhs=FiniteCyclicGroup(
        order=2,
        generator=Composition(
          left=nu_n,
          right=nu_n_plus_three,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda nu-squared "
      "transported-generator normalization"
    ),
    description=(
      "Normalize the generator of the "
      "order-two six-stem group already "
      "transported from nu_8 squared "
      "through E^(n-8) to the named "
      "nu_n squared generator. This rule "
      "does not derive the stable group "
      "transport itself."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )