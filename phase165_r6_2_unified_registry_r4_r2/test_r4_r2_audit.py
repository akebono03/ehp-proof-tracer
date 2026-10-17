from dataclasses import dataclass

from phase165_r6_2_unified_registry_r4_r2.r4_r2_audit import (
    classify_rule, evaluate_labeled, fingerprint, markdown, overlap_by_goal,
)


@dataclass(frozen=True)
class FakeRule:
    name: str
    conclusion_pattern: object = None
    premise_patterns: tuple = ()


@dataclass(frozen=True)
class FakeExpansion:
    rule: FakeRule
    subgoals: tuple


def test_fingerprint_stable():
    e = FakeExpansion(FakeRule("symmetry"), (2,))
    assert fingerprint(e) == ("symmetry", "(2,)")


def test_evaluate_counts_goals():
    e = FakeExpansion(FakeRule("x"), ())
    output = evaluate_labeled("p", lambda goal: (e,) if goal == 1 else (), (1, 2))
    assert output["goals_proposed"] == 1
    assert output["expansions"] == 1


def test_evaluate_tracks_error():
    def bad(goal):
        raise RuntimeError("bad")
    output = evaluate_labeled("p", bad, (1, 2))
    assert output["errors"] == {"RuntimeError": 2}


def test_overlap_counts_same_goal_only():
    e = FakeExpansion(FakeRule("x"), ())
    a = evaluate_labeled("a", lambda goal: (e,) if goal == 1 else (), (1, 2))
    b = evaluate_labeled("b", lambda goal: (e,) if goal == 2 else (), (1, 2))
    assert overlap_by_goal(a, b) == 0


def test_overlap_matches():
    e = FakeExpansion(FakeRule("x"), ())
    a = evaluate_labeled("a", lambda _: (e,), (1,))
    b = evaluate_labeled("b", lambda _: (e,), (1,))
    assert overlap_by_goal(a, b) == 1


def test_classification_no_pattern():
    assert classify_rule(FakeRule("x"), {"expansions": 0}, ()) == "INVERSE_UNAVAILABLE_NO_CONCLUSION_PATTERN"


def test_classification_missing_premises():
    r = FakeRule("x", conclusion_pattern=1)
    assert classify_rule(r, {"expansions": 0}, ()) == "INVERSE_UNAVAILABLE_NO_PREMISE_PATTERNS"


def test_classification_proposal_is_not_proof():
    assert classify_rule(FakeRule("x"), {"expansions": 1}, ()) == "APPLICABLE_CANDIDATE_ONLY"


def test_markdown():
    assert "候補帰属監査" in markdown({"status": "ATTRIBUTION_AUDITED"})
