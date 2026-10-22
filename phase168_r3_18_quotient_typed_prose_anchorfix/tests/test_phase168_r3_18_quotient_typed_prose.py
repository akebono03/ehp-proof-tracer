from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
from toda_group_proof_narrative_shared_components import _render_generic_narrative_statement_prose

def test_pi43_quotient_uses_homomorphism_theorem():
    result=search_group_from_registered_goal(n=3,k=1,bridge=build_shared_typed_bridge())
    items=[s.conclusion for s in result.proven_steps if isinstance(s.conclusion,QuotientIsomorphismStatement)]
    assert len(items)==1
    prose=_render_generic_narrative_statement_prose(items[0])
    assert "準同型定理より" in prose
    assert r"\cong" in prose
    assert r"\mathbb{Z}" in prose
    assert "first isomorphism" not in prose

def test_unrelated_statement_is_not_rewritten():
    assert _render_generic_narrative_statement_prose(object()) is None
