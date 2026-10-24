from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
from proof import Relation, RelationType


def _case(n, k):
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    return result, model


def test_pi43_quotient_is_moved_after_its_proven_domain():
    result, model = _case(3, 1)
    entries = project_narrative_order(model)
    flat = []
    for entry in entries:
        flat.append(entry.step_index)
        flat.extend(entry.after_indices)
    quotient_indices = [i for i, s in enumerate(model.steps)
                        if isinstance(s.conclusion, QuotientIsomorphismStatement)]
    assert quotient_indices
    for index in quotient_indices:
        step = model.steps[index].conclusion
        if index not in flat:
            continue
        previous = flat[:flat.index(index)]
        if any(isinstance(model.steps[j].conclusion, Relation)
               and model.steps[j].conclusion.relation_type is RelationType.EQUALITY
               and model.steps[j].conclusion.lhs == step.domain for j in previous):
            assert flat.index(index) > min(flat.index(j) for j in previous
                if isinstance(model.steps[j].conclusion, Relation)
                and model.steps[j].conclusion.lhs == step.domain)
    rendered = render_model_backed_narrative_markdown(result, model)
    assert "準同型定理" in rendered
    assert rendered.count("次の完全列を考える") == 1


def test_pi32_all_steps_preserved_without_suppression():
    result, model = _case(2, 1)
    entries = project_narrative_order(model)
    indices = [i for item in entries for i in (item.step_index, *item.after_indices)]
    assert sorted(indices) == list(range(len(model.steps)))
    rendered = render_model_backed_narrative_markdown(result, model)
    assert r"\operatorname{Im}\Delta=\ker E=0" in rendered
    assert rendered.count("次の完全列を考える") == 1
