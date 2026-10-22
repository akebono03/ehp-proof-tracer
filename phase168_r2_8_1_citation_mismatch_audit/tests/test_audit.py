from phase168_r2_8_1_citation_mismatch_audit.audit import CASES, classify_relation
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType


def test_nine_missing_targets_are_distinct():
    assert len(CASES) == 9
    assert len({(n, k) for n, k, locator in CASES}) == 9


def test_exact_match_is_distinguished():
    relation = Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, "g"), RelationType.EQUALITY)
    assert classify_relation(relation, relation) == "EXACT_MATCH"


def test_presentation_mismatch_is_distinguished():
    goal = Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, "a"), RelationType.EQUALITY)
    other = Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, "b"), RelationType.EQUALITY)
    assert classify_relation(goal, other) == "GENERATOR_OR_PRESENTATION_DIFFERENT"


def test_different_group_is_distinguished():
    goal = Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, "a"), RelationType.EQUALITY)
    other = Relation(TodaPrimaryGroup(5, 3), FiniteCyclicGroup(2, "a"), RelationType.EQUALITY)
    assert classify_relation(goal, other) == "DIFFERENT_GROUP"
