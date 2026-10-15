import inspect
from pathlib import Path
from install import transform
from toda_calculation_facade import build_standard_toda_report
from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown

def presentation():
    report=build_standard_toda_report(n=2,k=1)
    group=report.candidates[0].source_candidate.group_result
    replay=build_phase165_r41_pi32_common_replay(group,2,"narrative")
    return build_toda_group_proof_presentation(replay)

def test_old_reason_linker_not_used():
    import toda_group_proof_narrative_renderer as module
    source=Path(module.__file__).read_text(encoding="utf8")
    assert "def _phase159_r1_6c_link_proof_reasons(" not in source

def test_new_reason_generator_from_proofstep():
    import toda_group_proof_generic_narrative_renderer as module
    assert "phase165_r48_unified_exactness" in inspect.getsource(
        module._render_generic_narrative_proof_block)

def test_three_exactness_dependencies():
    steps=[n.proof_step for n in presentation().nodes]
    count=sum(1 for step in steps if step.inference_rule is not None
              and any(type(p.conclusion).__name__=="TodaProp42ExactnessStatement"
                      for p in step.premises))
    assert count==3

def test_public_reason_and_result():
    result=render_toda_group_proof_narrative_markdown(presentation())
    assert "完全性より" in result
    assert r"\pi_{3}^{2}" in result
    assert "以上より" in result
