from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from homotopy_groups import TodaSuspensionMap
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import ordered_proof_ancestry

def test_suspension_conclusion_retained():
    result=search_group_from_registered_goal(n=3,k=1)
    roots=[s for s in result.proven_steps if s.conclusion==result.conclusion]
    assert len(roots)==1
    steps=ordered_proof_ancestry(roots[0])
    assert any(isinstance(s.conclusion, GeneratorSuspension) and isinstance(s.conclusion.map,TodaSuspensionMap) for s in steps)

def test_public_narrative_still_has_generator_suspension():
    from web_group_proof import build_standard_web_group_proof_view
    view=build_standard_web_group_proof_view(3,1,2,'narrative')
    text='\n'.join(s if isinstance(s,str) else str(getattr(s,'prefix',''))+str(getattr(s,'statement_latex','') or '')+str(getattr(s,'suffix','')) for s in view.rendered_lines)
    assert 'E(\\eta_{2})' in text
