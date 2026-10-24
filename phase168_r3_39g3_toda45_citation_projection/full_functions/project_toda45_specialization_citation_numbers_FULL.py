def project_toda45_specialization_citation_numbers(model, step_index):
    """Bind Toda (4.5) citations only to their used general Proof Step."""
    step = model.steps[step_index]
    evidence = toda45_specialization_evidence(step)
    if evidence is None:
        return ()
    source_step, _ = evidence
    numbers = []
    for source_index, candidate in enumerate(model.steps):
        if candidate != source_step:
            continue
        for number in model.step_citation_numbers[source_index]:
            if number not in numbers:
                numbers.append(number)
    return tuple(numbers)


