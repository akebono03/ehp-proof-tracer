def toda_45_generic_zero_group_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_zero = (
      premises[
        0
      ].conclusion
    )
    isomorphism = (
      premises[
        1
      ].conclusion
    )

    transport_map = (
      isomorphism.map
    )

    return (
      _concrete_toda_group_matches_structural_group(
        source_zero.group,
        transport_map.source_group,
      )
    )

  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        1
      ].conclusion
    )

    return TodaPrimaryGroupZeroStatement(
      group=(
        isomorphism
        .map
        .target_group
      ),
    )

  return InferenceRule(
    name=(
      "Toda 4.5 generic "
      "zero-group transport"
    ),
    description=(
      "Transport a zero Toda primary "
      "group through a supplied Toda "
      "(4.5) iterated-suspension "
      "isomorphism. The target group is "
      "zero. No theorem-specific stable "
      "stem rule is used."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          Toda45IsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )