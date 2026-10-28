def project_verified_direct_sum_transport(
    model: object, order: tuple[int, ...],
) -> VerifiedDirectSumTransportDisplay | None:
    """Replace exclusive, typed E-image steps with their proved E^r endpoints.

    The caller must already have replayed the complete Proof Tree. This
    projection independently checks the root source, (4.5) map, every typed
    GeneratorImage premise, proof ancestry and registered citation association.
    It never obtains proof evidence from a group label or display string.
    """
    steps = getattr(model, "steps", ())
    root_index = getattr(model, "root_index", None)
    citations = getattr(model, "step_citation_numbers", ())
    if (not isinstance(steps, tuple) or not isinstance(order, tuple)
            or not isinstance(citations, tuple)
            or len(citations) != len(steps)
            or type(root_index) is not int
            or not 0 <= root_index < len(steps)
            or root_index not in order
            or len(set(order)) != len(order)
            or any(type(index) is not int or not 0 <= index < len(steps)
                   for index in order)):
        return None

    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None

    root = steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or len(root.premises) < 4
            or not isinstance(root.conclusion, Relation)
            or root.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(root.conclusion.rhs, DirectSumGroup)):
        return None
    prior, iso, *image_steps = root.premises
    prior_index, iso_index = by_identity.get(id(prior)), by_identity.get(id(iso))
    if (prior_index is None or iso_index is None
            or prior_index not in order or iso_index not in order
            or not isinstance(prior.conclusion, Relation)
            or prior.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(prior.conclusion.rhs, DirectSumGroup)
            or iso.rule is not ProofRule.INFERENCE
            or not isinstance(iso.conclusion, Toda45IsomorphismStatement)
            or not isinstance(iso.conclusion.map, TodaIteratedSuspensionMap)):
        return None

    source_structure, target_structure = prior.conclusion.rhs, root.conclusion.rhs
    left = source_structure.summands
    right = target_structure.summands
    r = iso.conclusion.map.exponent
    if (type(r) is not int or r < 2 or len(left) < 2
            or len(left) != len(right)
            or not all(isinstance(group, (FiniteCyclicGroup, FreeCyclicGroup))
                       for group in left + right)
            or iso.conclusion.map.source_group != prior.conclusion.lhs
            or iso.conclusion.map.target_group != root.conclusion.lhs):
        return None

    expected = generator_images_for_group_transport(prior.conclusion, root.conclusion)
    if (expected is None or len(expected) != r * len(left)
            or len(image_steps) != len(expected)
            or any(step.rule is not ProofRule.INFERENCE
                   or not isinstance(step.conclusion, GeneratorImage)
                   or step.conclusion != image
                   or by_identity.get(id(step)) not in order
                   for step, image in zip(image_steps, expected))):
        return None

    # R10EN: each direct-sum image needs its own registered GIVEN ancestor.
    from phase169_r10en_shared_citation_provenance.core import (
        verified_generator_image_citation_numbers,
    )
    numbers = verified_generator_image_citation_numbers(
        model, order, image_steps, require_each=True,
    )
    if numbers is None:
        return None

    # R10EL: the shared strict contract preserves all-or-nothing direct-sum
    # suppression, including external-consumer and individual-citation checks.
    from phase169_r10el_shared_generator_suppression.core import (
        exclusive_generator_inference_indices,
    )
    hidden = exclusive_generator_inference_indices(
        model, order, image_steps, root_index, require_all=True,
    )
    if hidden is None:
        return None

    formulae: list[str] = []
    for source, target in zip(left, right):
        # This public printer reads the already-typed generator; it cannot
        # introduce an equation or authorize a family relation.
        source_tex = render_toda_public_group_generator_latex(source.generator)
        target_tex = render_toda_public_group_generator_latex(target.generator)
        if not source_tex or not target_tex:
            return None
        formulae.append(rf"$E^{{{r}}}({source_tex})={target_tex}$")
    if not formulae:
        return None
    labels = ", ".join(f"[R{number}]" for number in numbers)
    statement = f"{labels}より, " + "、".join(formulae) + "."
    return VerifiedDirectSumTransportDisplay(
        root_index=root_index,
        hidden_indices=tuple(sorted(hidden)),
        statement=statement,
        citation_numbers=numbers,
    )
