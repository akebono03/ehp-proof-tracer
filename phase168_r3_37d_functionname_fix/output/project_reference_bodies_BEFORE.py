def project_reference_bodies(registry, assertion_ids):
    if registry is None:
        return ()
    result = []
    for assertion_id in assertion_ids:
        statement = registry.assertion(assertion_id).content
        sentence = typed_sentence(statement, None)
        if sentence is None:
            latex, fallback = _group_proof_statement_latex(statement)
            if latex is not None and fallback is None:
                sentence = '$' + latex + '$.'
        if sentence is not None and sentence not in result:
            result.append(sentence)
    return tuple(result)
