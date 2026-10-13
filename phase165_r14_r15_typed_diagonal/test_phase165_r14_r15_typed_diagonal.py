from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r15_typed_diagonal import match_diagonal_toda51_claims, audit_r15


def test_diagonal_two_toda51_goals_matched():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2))
    rows = match_diagonal_toda51_claims(suspension)
    assert len(rows) == 3
    assert [row.source_locator for row in rows] == ['(5.1)', '(5.1)', None]
    assert all(row.verified is False and row.proof_eligible is False for row in rows)


def test_generic_diagonal_not_special_case():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(4,4), TodaPrimaryGroup(5,5))
    rows = match_diagonal_toda51_claims(suspension)
    assert len(rows) == 3
    assert rows[0].goal.lhs == TodaPrimaryGroup(4,4)


def test_non_diagonal_rejected():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(3,2), TodaPrimaryGroup(4,3))
    assert match_diagonal_toda51_claims(suspension) == ()


def test_generator_suspension_not_mistaken_for_toda51():
    rows = match_diagonal_toda51_claims(
        TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2)))
    assert rows[2].source_locator is None


def test_prop42_still_not_misclassified():
    report = audit_r15()
    assert report['prop42_source_candidate_count'] == 2
    assert report['prop42_selected'] is False
    assert report['proof_steps_created'] == 0
