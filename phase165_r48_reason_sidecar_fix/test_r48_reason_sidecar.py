from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_reasons import _exactness_to_map_property_reason
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def presentation():
    report = build_standard_toda_report(n=2, k=1)
    result = report.candidates[0].source_candidate.group_result
    replay = build_phase165_r41_pi32_common_replay(result, 2, 'narrative')
    return build_toda_group_proof_presentation(replay)


def test_h_injective_reason():
    step = next(n.proof_step for n in presentation().nodes
                if type(n.proof_step.conclusion).__name__ == 'MapInjective')
    reason = _exactness_to_map_property_reason(step)
    assert reason is not None
    assert len(reason.premise_steps) == 2


def test_h_surjective_reason():
    step = next(n.proof_step for n in presentation().nodes
                if type(n.proof_step.conclusion).__name__ == 'MapSurjective')
    reason = _exactness_to_map_property_reason(step)
    assert reason is not None
    assert len(reason.premise_steps) == 2


def test_public_narrative_shows_reason():
    rendered = render_toda_group_proof_narrative_markdown(presentation())
    assert '完全性より' in rendered


def test_root_conclusion_preserved():
    rendered = render_toda_group_proof_narrative_markdown(presentation())
    assert r'\pi_{3}^{2}' in rendered
    assert r'\eta_{2}' in rendered
