def finite_cyclic_suspension_transport_inference_rule() -> InferenceRule:
    """Transport a cyclic presentation only from three verified typed premises."""
    def guard(premises, bindings):
        if len(premises) != 3:
            return False
        source, isomorphism, image = (step.conclusion for step in premises)
        if (not isinstance(source, Relation)
                or source.relation_type is not RelationType.EQUALITY
                or not isinstance(source.rhs, FiniteCyclicGroup)
                or type(source.rhs.order) is not int
                or source.rhs.order < 1
                or not isinstance(isomorphism, TodaSuspensionIsomorphismStatement)
                or not isinstance(image, GeneratorImage)):
            return False
        mapping = isomorphism.map
        if not isinstance(mapping, TodaSuspensionMap):
            return False
        domain = mapping.source_group
        codomain = mapping.target_group
        if (not isinstance(domain, TodaPrimaryGroup)
                or not isinstance(codomain, TodaPrimaryGroup)
                or type(domain.group_dimension) is not int
                or type(domain.sphere_dimension) is not int
                or domain.group_dimension < domain.sphere_dimension
                or domain.sphere_dimension < 2):
            return False
        return (
            source.lhs == domain
            and codomain == TodaPrimaryGroup(
                domain.group_dimension + 1,
                domain.sphere_dimension + 1,
            )
            and image.map == mapping
            and image.source_generator == source.rhs.generator
        )

    def conclusion(premises):
        source, isomorphism, image = (step.conclusion for step in premises)
        return Relation(
            lhs=isomorphism.map.target_group,
            rhs=FiniteCyclicGroup(
                order=source.rhs.order,
                generator=image.target_generator,
            ),
            relation_type=RelationType.EQUALITY,
        )

    return InferenceRule(
        name="finite cyclic presentation transported by proved suspension isomorphism",
        description=(
            "Transport a finite cyclic group presentation by an actually proved "
            "suspension isomorphism and an actually proved generator image."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=TodaSuspensionIsomorphismStatement),
            PremisePattern(statement_type=GeneratorImage),
        ),
        match_guard=guard,
        conclusion_builder=conclusion,
    )
