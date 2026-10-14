# R57-R8 installed code

## Modified complete functions

### phase165_r52_r9_shared_math.py

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)

    from phase165_r57_r7_stable_expansion import (
        expand_registered_toda45_finite_cyclic_goal,
    )
    from phase165_r57_r8_eta_specialization import (
        expand_registered_eta_specialization,
    )

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        options = []
        if (isinstance(goal, Relation)
                and goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.rhs, FreeCyclicGroup)
                and isinstance(goal.lhs, TodaPrimaryGroup)):
            for image in available:
                if not isinstance(image, GeneratorImage):
                    continue
                if (getattr(image.map, "source_group", None) != goal.lhs
                        or image.source_generator != goal.rhs.generator):
                    continue
                options.append(GoalExpansion(
                    reverse_free_cyclic_transport_rule(),
                    (MapIsomorphism(image.map),
                     Relation(image.map.target_group,
                              FreeCyclicGroup(image.target_generator)),
                     image),
                ))
        options.extend(expand_registered_toda45_finite_cyclic_goal(goal, tuple(available)))
        options.extend(expand_registered_eta_specialization(goal, tuple(available)))
        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            expand_existing_pi43_rules,
            *extra_providers,
        ):
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        return tuple(options)
    return expand
```

### phase165_r55_nk_only_goal.py

```python


# R57-R8 REGISTERED GENERIC GOAL SPECIALIZATION
_phase165_r57_r8_previous_registered_group_goal_candidates = registered_group_goal_candidates

def registered_group_goal_candidates(bridge, *, n: int, k: int):
    """Extend the previous R55 selection with derived symbolic-reference goals."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates
    existing = _phase165_r57_r8_previous_registered_group_goal_candidates(bridge=bridge, n=n, k=k)
    if not isinstance(existing, tuple):
        raise TypeError("R55 selector must return a tuple")
    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)
    typed_bridge = bridge
    candidates = specialized_eta_group_goal_candidates(group, typed_bridge)
    output = list(existing)
    for candidate in candidates:
        if not any(type(candidate) is type(old) and candidate == old for old in output):
            output.append(candidate)
    return tuple(output)
```
