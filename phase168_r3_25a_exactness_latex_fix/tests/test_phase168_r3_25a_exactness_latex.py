from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_merged_exactness_arrows_are_valid_single_backslash_latex():
    bridge = build_shared_typed_bridge()
    for n, k, arrow_count in ((2, 1, 4), (3, 1, 3)):
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        assert result.status is ProofSearchStatus.COMPLETE
        model = build_linked_proof_narrative_model(result, bridge)
        output = render_model_backed_narrative_markdown(result, model)
        assert output.count(r"\xrightarrow{") == arrow_count
        assert r"\\xrightarrow" not in output
        assert r"\\Delta" not in output
        assert output.count("次の完全列を考える") == 1
