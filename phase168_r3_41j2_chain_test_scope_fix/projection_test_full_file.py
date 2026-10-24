from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def _case(n, k):
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    return result, model


def test_pi32_three_windows_project_one_chain():
    result, model = _case(2, 1)
    chains = project_exactness_chains(model)
    assert len(chains) == 1
    assert len(chains[0].arrows) == 4
    assert len(chains[0].step_indices) == 3
    rendered = render_model_backed_narrative_markdown(result, model)
    assert rendered.count("次の完全列を考える") == 1
    # The Reference may contain the same general EHP arrow.
    # Count the concrete displayed arrow only in the proof section.
    reference, proof = rendered.split("\n証明\n", 1)
    assert proof.count(r"\xrightarrow{\Delta}") == 1


def test_pi43_two_windows_project_one_chain():
    result, model = _case(3, 1)
    chains = project_exactness_chains(model)
    assert len(chains) == 1
    assert len(chains[0].arrows) == 3
    assert len(chains[0].step_indices) == 2
    rendered = render_model_backed_narrative_markdown(result, model)
    assert rendered.count("次の完全列を考える") == 1
    assert "準同型定理" in rendered
