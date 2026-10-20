"""Phase 166 R3-D: read-only public pi3^2 regression checks."""
import pytest

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import ProofRule, Relation


@pytest.fixture(scope="module")
def pi32_result():
    return search_group_from_registered_goal(n=2, k=1)


@pytest.fixture(scope="module")
def pi32_markdown(pi32_result):
    return render_partial_proof_markdown(pi32_result)


def test_pi32_search_is_complete_with_exact_goal(pi32_result):
    expected = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert pi32_result.status is ProofSearchStatus.COMPLETE
    assert pi32_result.conclusion == expected
    assert pi32_result.open_goals == ()
    assert pi32_result.proven_steps
    assert any(step.conclusion == expected for step in pi32_result.proven_steps)


def test_pi32_has_actual_given_and_inference_steps(pi32_result):
    rules = {step.rule for step in pi32_result.proven_steps}
    assert ProofRule.GIVEN in rules
    assert ProofRule.INFERENCE in rules
    assert not pi32_result.open_goals


def test_pi32_reference_section_and_order(pi32_markdown):
    text = pi32_markdown
    assert "## 使用する結果" in text
    assert "[R1] (5.1)." in text
    assert "[R2] Proposition 5.1." in text
    assert text.index("[R1] (5.1).") < text.index("[R2] Proposition 5.1.")
    assert r"\pi_{i}^{1} = 0" in text
    assert r"H(\eta_{2}) = \iota_{3}" in text


def test_pi32_exact_sequence_and_mathematical_steps(pi32_markdown):
    text = pi32_markdown
    assert text.count("次の完全列を考える") == 1
    assert r"\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}" in text
    assert "は単射" in text
    assert "は全射" in text
    assert "は同型" in text
    assert "零写像" in text
    assert "完全性より" in text


def test_pi32_final_conclusion_once(pi32_markdown):
    text = pi32_markdown
    assert text.count("以上より,") == 1
    assert r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}" in text
    assert text.rstrip().endswith("□")
    assert "未解決 Goal" not in text
    assert "証明未完成" not in text


def test_pi32_public_web_view_is_complete():
    view = build_group_proof_progress_view(n=2, k=1, max_depth=2)
    assert view.n == 2
    assert view.k == 1
    assert view.mode == "narrative"
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert view.rendered_lines
    assert view.steps
    flattened = "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )
    assert "使用する結果" in flattened
    assert "(5.1)" in flattened
    assert "Proposition 5.1" in flattened
    assert "以上より" in flattened
    assert "□" in flattened
