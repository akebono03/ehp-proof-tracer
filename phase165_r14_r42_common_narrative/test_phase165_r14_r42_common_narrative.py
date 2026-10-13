"""Focused regression tests for generic typed steps and reference sources."""
from pathlib import Path

from phase165_r14_r38_direct_registry import reconstruct_registered_pi32
from phase165_r14_r34_backward_search import pi32_goal
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference
from phase165_r14_r40_replay import build_phase165_r40_pi32_common_replay
from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown

TEX=Path(__file__).resolve().parent.parent/'phase165_r14_r39_toda51.tex'

def _all_steps(root):
    visited=set()
    def visit(s):
        if id(s) in visited:return
        visited.add(id(s))
        yield s
        for child in s.premises:
            yield from visit(child)
    return tuple(visit(root))

def _result():
    return build_standard_toda_report(n=2,k=1).candidates[0].source_candidate.group_result

def test_registered_goal_is_unchanged():
    _,root=reconstruct_registered_pi32(TEX)
    assert root.conclusion==pi32_goal()

def test_typed_reference_leaves_keep_locators():
    _,root=reconstruct_registered_pi32(TEX)
    refs={extract_toda_group_proof_step_literature_reference(step).locator
          for step in _all_steps(root)
          if not step.premises and extract_toda_group_proof_step_literature_reference(step) is not None}
    assert {'(5.1)','Proposition 4.2','Proposition 5.1'} <= refs

def test_generic_generator_image_is_math():
    _,root=reconstruct_registered_pi32(TEX)
    steps=[s for s in _all_steps(root) if type(s.conclusion).__name__=='GeneratorImage']
    assert len(steps)==1
    value=_render_generic_narrative_step(steps[0])
    assert 'GeneratorImage' not in value
    assert 'H(' in value and r'\eta' in value

def test_generic_map_isomorphism_is_japanese():
    _,root=reconstruct_registered_pi32(TEX)
    steps=[s for s in _all_steps(root) if type(s.conclusion).__name__=='MapIsomorphism']
    assert len(steps)>=1
    value=_render_generic_narrative_step(steps[0])
    assert '同型' in value and 'generic' not in value

def test_common_narrative_still_uses_real_presentation():
    replay=build_phase165_r41_pi32_common_replay(_result(),2,'narrative')
    presentation=build_toda_group_proof_presentation(replay)
    text=render_toda_group_proof_narrative_markdown(presentation)
    assert 'GeneratorImage' not in text
    assert 'generic injective and surjective imply isomorphism' not in text
    assert '完全列' in text
