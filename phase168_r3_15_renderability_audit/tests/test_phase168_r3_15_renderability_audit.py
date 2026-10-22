from unittest.mock import patch
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_15_renderability_audit import audit_reasoned_renderability, _attempt
from proof import ProofRule, ProofStep


def _case():
    step = ProofStep(conclusion=object(), premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.PARTIAL, proven_steps=(step,))
    return result, build_proof_narrative_model(result)


def test_attempt_returns_latex():
    assert _attempt(lambda _: r"\pi_3^2", object()) == (r"\pi_3^2", None)


def test_attempt_handles_exception():
    value, error = _attempt(lambda _: 1 / 0, object())
    assert value is None and error == "ZeroDivisionError"


def test_attempt_rejects_nonstring():
    assert _attempt(lambda _: ("a",), object()) == (None, "empty_or_non_string")


def test_audit_tracks_each_renderer_independently():
    result, model = _case()
    with patch('phase168_r3_15_renderability_audit.build_reasoned_narrative_lines') as body, \
         patch('phase168_r3_15_renderability_audit.render_toda_proof_statement_latex', return_value='T'), \
         patch('phase168_r3_15_renderability_audit.render_repository_conclusion_latex', side_effect=TypeError('x')), \
         patch('phase168_r3_15_renderability_audit._group_proof_statement_latex', return_value=(None, 'Object')):
        body.return_value = (type('Line', (), {'step_index': 0, 'conclusion_latex': None})(),)
        found = audit_reasoned_renderability(result, model)
    assert len(found) == 1
    assert found[0].candidates[0][1] == 'T'
    assert found[0].candidates[1][2] == 'TypeError'
    assert found[0].candidates[2][1] is None
