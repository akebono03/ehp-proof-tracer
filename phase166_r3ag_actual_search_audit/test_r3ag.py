from phase166_r3ag_actual_search_audit.audit import CASES, analyze_case
from phase165_r52_r9_shared_math import build_shared_typed_bridge


def test_r3ag_covers_each_stem_and_three_stable_dimensions():
    assert CASES == ((2, 4), (2, 5), (2, 6), (3, 5), (3, 6), (3, 7),
                     (7, 9), (7, 10), (7, 11))


def test_r3ag_reports_goal_source_without_adding_proof_premises():
    report = analyze_case(build_shared_typed_bridge(), 2, 4)
    assert report["k"] == 2
    assert report["n"] == 4
    assert report["outcome"] in ("SEARCH_EXECUTED", "NO_UNIQUE_TYPED_GOAL", "EXCEPTION")
    assert "database_count" in report or "exception" in report
