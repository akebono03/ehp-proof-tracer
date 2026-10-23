from pathlib import Path

from phase168_r3_39c_source_leaf_audit.audit import audit


def test_report_contains_direct_and_symbolic_sources():
    root = Path(__file__).resolve().parents[2]
    result = audit(root)
    assert result["direct"]
    assert result["general"]
    assert all("symbolic_source_matches" in row for row in result["direct"])


def test_report_marks_unmatched_direct_leaves():
    root = Path(__file__).resolve().parents[2]
    result = audit(root)
    direct = {row["assertion_id"]: row for row in result["direct"]}
    assert result["unmatched_direct"] == [
        row["assertion_id"] for row in result["direct"]
        if not row["symbolic_source_matches"]
    ]
    assert all(identifier in direct for identifier in result["unmatched_direct"])
