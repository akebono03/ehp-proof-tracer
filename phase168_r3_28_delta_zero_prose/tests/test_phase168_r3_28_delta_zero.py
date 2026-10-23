from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from toda_rules import TodaDeltaZeroStatement
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_delta_zero_typed_prose_uses_map_groups():
    statement = TodaDeltaZeroStatement(
        map=TodaDeltaMap(
            source_group=TodaPrimaryGroup(3, 3),
            target_group=TodaPrimaryGroup(1, 1),
        )
    )
    rendered = typed_sentence(statement, None)
    assert r"\Delta: \pi_{3}^{3}\to \pi_{1}^{1}" in rendered
    assert "零写像である" in rendered


def test_pi32_delta_zero_appears_from_proof_tree():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=2, k=1, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    assert any(isinstance(s.conclusion, TodaDeltaZeroStatement) for s in model.steps)
    rendered = render_model_backed_narrative_markdown(result, model)
    assert r"\Delta: \pi_{3}^{3}\to \pi_{1}^{1}" in rendered
    assert "零写像である" in rendered
    assert rendered.count("次の完全列を考える") == 1
