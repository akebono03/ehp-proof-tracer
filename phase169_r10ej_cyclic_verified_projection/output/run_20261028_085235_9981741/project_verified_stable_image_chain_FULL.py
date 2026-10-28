def project_verified_stable_image_chain(
    model: object, order: tuple[int, ...],
) -> VerifiedStableImageChainDisplay | None:
    """Compress only rooted, checked, at-least-three-fold proven image chains.

    A presentation cannot create or verify proof steps: the caller supplies the
    already-verified model.  This function additionally checks the exact source,
    isomorphism, every image map, every generator endpoint and references.
    Return None rather than removing a statement with a separate consumer.
    """
    steps = getattr(model, "steps", ())
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, (tuple, list))
            or type(root_index) is not int
            or root_index < 0 or root_index >= len(steps)
            or root_index not in order):
        return None
    root = steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(root.conclusion, Relation)
            or root.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(root.conclusion.lhs, TodaPrimaryGroup)
            or not isinstance(root.conclusion.rhs, FiniteCyclicGroup)
            or len(root.premises) < 5):
        return None
    source_step, iso_step, *images = root.premises
    if (not isinstance(source_step.conclusion, Relation)
            or source_step.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(source_step.conclusion.lhs, TodaPrimaryGroup)
            or not isinstance(source_step.conclusion.rhs, FiniteCyclicGroup)
            or source_step.conclusion.rhs.order != root.conclusion.rhs.order
            or iso_step.rule is not ProofRule.INFERENCE
            or not isinstance(iso_step.conclusion, Toda45IsomorphismStatement)
            or not isinstance(iso_step.conclusion.map, TodaIteratedSuspensionMap)):
        return None
    src = source_step.conclusion
    dst = root.conclusion
    n, q = src.lhs.sphere_dimension, src.lhs.group_dimension
    m, p = dst.lhs.sphere_dimension, dst.lhs.group_dimension
    r = len(images)
    if (not all(type(v) is int for v in (n, q, m, p))
            or n < 2 or q < n or n < q - n + 2
            or m - n != r or p - q != r
            or iso_step.conclusion.map != TodaIteratedSuspensionMap(
                exponent=r, source_group=src.lhs, target_group=dst.lhs,
            )):
        return None

    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None
    image_indices = []
    expected_generator = src.rhs.generator
    for i, image_step in enumerate(images):
        image_index = by_identity.get(id(image_step))
        image = image_step.conclusion
        if (image_index is None or image_index not in order
                or image_index == root_index
                or image_step.rule is not ProofRule.INFERENCE
                or not isinstance(image, GeneratorImage)
                or not isinstance(image.map, TodaSuspensionMap)
                or image.map != TodaSuspensionMap(
                    TodaPrimaryGroup(q + i, n + i),
                    TodaPrimaryGroup(q + i + 1, n + i + 1),
                )
                or image.source_generator != expected_generator):
            return None
        expected_generator = image.target_generator
        image_indices.append(image_index)
    if expected_generator != dst.rhs.generator or len(set(image_indices)) != r:
        return None
    for image_index in image_indices:
        image_step = steps[image_index]
        if any(
            consumer_index != root_index
            for consumer_index, consumer in enumerate(steps)
            if any(parent is image_step for parent in consumer.premises)
        ):
            return None
    # A public LaTeX spelling is permitted only for the already-typed,
    # independently proven generator.  The public printer supplies notation,
    # never a missing GeneratorImage or a new mathematical inference.
    def display_generator_tex(generator):
        value = element_tex(generator)
        if value:
            return value
        from expression import Composition
        if not isinstance(generator, Composition):
            return None
        from toda_human_readable_renderer import render_toda_public_group_generator_latex
        return render_toda_public_group_generator_latex(generator)

    source_tex = display_generator_tex(src.rhs.generator)
    target_tex = display_generator_tex(dst.rhs.generator)
    if not source_tex or not target_tex:
        return None

    hidden = set(image_indices)
    # The image chain may use intermediate GeneratorImages and
    # GeneratorSuspensions for its factors (e.g. nu^2 or eta o mu).
    # Inspect ONLY ancestors of the root's independently proved images.
    # Hide a typed inference only when it has no own citation and every
    # consumer is already hidden (or the compressed root).  This fixed point
    # keeps shared or separately cited evidence visible, and never edits the
    # model or its actual dependencies.
    eligible_ancestors = set()
    pending = [premise for image_step in images for premise in image_step.premises]
    visited = set()
    while pending:
        ancestor = pending.pop()
        identity = id(ancestor)
        if identity in visited:
            continue
        visited.add(identity)
        index = by_identity.get(identity)
        if index is None or index not in order:
            return None
        if (index != root_index
                and ancestor.rule is ProofRule.INFERENCE
                and isinstance(ancestor.conclusion, (GeneratorImage, GeneratorSuspension))
                and not model.step_citation_numbers[index]):
            eligible_ancestors.add(index)
        pending.extend(ancestor.premises)

    changed = True
    while changed:
        changed = False
        for index in sorted(eligible_ancestors - hidden):
            ancestor = steps[index]
            consumers = {
                consumer_index
                for consumer_index, consumer in enumerate(steps)
                if any(parent is ancestor for parent in consumer.premises)
            }
            if consumers and consumers.issubset(hidden | {root_index}):
                hidden.add(index)
                changed = True

    # Citations are copied from actual linked GIVEN ancestors of the image
    # proofs, not inferred from the symbols eta/nu/sigma or from rule names.
    cited = set()
    for image_step in images:
        pending = [image_step]
        visited = set()
        while pending:
            candidate = pending.pop()
            if id(candidate) in visited:
                continue
            visited.add(id(candidate))
            index = by_identity.get(id(candidate))
            if index is not None and candidate.rule is ProofRule.GIVEN:
                cited.update(model.step_citation_numbers[index])
            pending.extend(candidate.premises)
    citation_numbers = tuple(
        citation.number for citation in model.citations if citation.number in cited
    )
    # Never replace individually cited evidence with an uncited displayed claim.
    if not citation_numbers:
        return None
    return VerifiedStableImageChainDisplay(
        root_index=root_index,
        exponent=r,
        source_tex=source_tex,
        target_tex=target_tex,
        hidden_indices=tuple(sorted(hidden)),
        citation_numbers=citation_numbers,
    )
