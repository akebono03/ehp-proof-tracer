def test_r10e5_two_inferred_images_are_required_to_prove_composition():
    goal = _image(8, 6, _square(8), _square(9))
    obligations = component_image_obligations(goal)
    assert obligations is not None
    rule = composite_generator_image_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE)
                  for item in obligations)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert matches[0].premises == steps
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(rule, steps[:1]) == ()
    assert find_inference_matches_for_rule(
        rule, (replace(steps[0], rule=ProofRule.GIVEN), steps[1]),
    ) == ()
    # The inference matcher accepts premises in arbitrary input order and
    # returns them in their typed premise-pattern order.
    reversed_matches = find_inference_matches_for_rule(rule, tuple(reversed(steps)))
    assert len(reversed_matches) == 1
    assert reversed_matches[0].premises == steps
    assert apply_inference_match(reversed_matches[0]).conclusion == goal
