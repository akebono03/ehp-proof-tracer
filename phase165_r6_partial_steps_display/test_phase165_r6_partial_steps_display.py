from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from proof import ProofRule, ProofStep


def test_partial_narrative_displays_observed_given_and_inference_without_qed():
    given = ProofStep(conclusion='known premise', premises=(), rule=ProofRule.GIVEN)
    inferred = ProofStep(conclusion='derived fact', premises=(given,), rule=ProofRule.INFERENCE)
    result = make_partial_proof_result(
        n=3,
        k=1,
        status=ProofSearchStatus.PARTIAL,
        proven_steps=(given, inferred),
        open_goals=('unresolved target',),
    )
    text = render_partial_proof_markdown(result)
    assert '与件: known premise' in text
    assert '推論: derived fact' in text
    assert text.index('known premise') < text.index('derived fact')
    assert 'unresolved target' in text
    assert '□' not in text


def test_partial_narrative_has_no_made_up_steps():
    result = make_partial_proof_result(
        n=200,
        k=90,
        status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=('no applicable rule',),
        open_goals=(TodaPrimaryGroup(290, 200),),
    )
    text = render_partial_proof_markdown(result)
    assert '確認済み ProofStep' not in text
    assert r'\pi_{290}^{200}' in text
    assert '未解決 Goal' in text
    assert '□' not in text
