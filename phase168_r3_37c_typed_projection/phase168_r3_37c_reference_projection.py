"""Common typed reference sentence projection. No source lookup."""
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex


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
