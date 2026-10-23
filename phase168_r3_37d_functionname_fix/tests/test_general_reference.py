from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_pi54_general_toda45_reference_and_specialization():
    bridge=build_shared_typed_bridge()
    contexts=[]
    result=search_group_from_registered_goal(n=4,k=1,bridge=bridge,context_sink=contexts.append)
    assert len(contexts)==1
    model=build_linked_proof_narrative_model(result,contexts[0])
    markdown=render_model_backed_narrative_markdown(result,model)
    assert r"E^{m-n}:\pi_{n+k}^{n}" in markdown
    assert r"E: \pi_{4}^{3}\to \pi_{5}^{4}" in markdown
    assert r"\eta_n=E^{n-2}\eta_2" in markdown


def test_pi32_pi43_general_prop42_reference():
    for n,k in ((2,1),(3,1)):
        bridge=build_shared_typed_bridge()
        contexts=[]
        result=search_group_from_registered_goal(n=n,k=k,bridge=bridge,context_sink=contexts.append)
        assert len(contexts)==1
        model=build_linked_proof_narrative_model(result,contexts[0])
        markdown=render_model_backed_narrative_markdown(result,model)
        assert "Proposition 4.2 により" in markdown
        assert r"\xrightarrow{\Delta}" in markdown
