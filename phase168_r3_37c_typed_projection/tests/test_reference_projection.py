from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_pi54_reference_and_specific_iso():
    bridge=build_shared_typed_bridge()
    contexts=[]
    result=search_group_from_registered_goal(n=4,k=1,bridge=bridge,context_sink=contexts.append)
    assert result.status.value=='complete'
    assert len(contexts)==1
    model=build_linked_proof_narrative_model(result,contexts[0])
    refs={c.reference.locator:c for c in model.citations}
    assert refs['Proposition 5.1'].statement_bodies
    assert refs['(4.5)'].assertion_ids
    markdown=render_model_backed_narrative_markdown(result,model)
    assert r'E: \pi_{4}^{3}\to \pi_{5}^{4}' in markdown
    assert '同型' in markdown


def test_no_source_guessing_for_pi32_pi43():
    for n,k in ((2,1),(3,1)):
        bridge=build_shared_typed_bridge()
        contexts=[]
        result=search_group_from_registered_goal(n=n,k=k,bridge=bridge,context_sink=contexts.append)
        assert len(contexts)==1
        model=build_linked_proof_narrative_model(result,contexts[0])
        assert all(c.assertion_ids for c in model.citations)
