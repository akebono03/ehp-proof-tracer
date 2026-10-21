from phase166_r3al_112_target_audit.audit import audit_112_targets


def test_audit_all_112_without_searching_proofs():
    report = audit_112_targets()
    assert report["count"] == 112
    assert len(report["records"]) == 112
    assert report["production_code_modified"] is False
    assert all(record["status_unchanged"] for record in report["records"] if record["goal_count"] == 1)


def test_pi1513_eta_square_and_zero_pi92():
    records = {(r["n"], r["k"]): r for r in audit_112_targets()["records"]}
    assert r"\eta_{13}^{2}" in records[(13, 2)]["web_target"]
    assert records[(2, 7)]["web_target"] == r"\pi_{9}^{2} = 0"


def test_missing_targets_are_reported_not_invented():
    report = audit_112_targets()
    assert report["display_ok"] + report["display_issues"] == 112
    for item in report["issues"]:
        assert not item["ok"]
