def expand_cited_eta_generator(goal: object) -> tuple[GoalExpansion, ...]:
    if isinstance(goal, GeneratorSuspension):
        pair = _eta_pair(goal)
        if pair is None:
            return ()
        return (GoalExpansion(eta_definition_to_suspension_rule(goal), pair),)
    if isinstance(goal, GeneratorImage) and isinstance(goal.map, TodaSuspensionMap):
        witness = GeneratorSuspension(goal.map, goal.source_generator, goal.target_generator)
        if _eta_pair(witness) is not None:
            return (GoalExpansion(suspension_to_generator_image_rule(), (witness,)),)
        composite = _composition_eta_suspensions(goal)
        if composite is not None:
            return (GoalExpansion(composition_eta_suspension_image_rule(goal), composite),)
    return ()


