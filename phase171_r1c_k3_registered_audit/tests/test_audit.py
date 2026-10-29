"""Only newly added R1C audit helpers are tested; no full-suite pytest."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from phase171_r1c_k3_registered_audit import audit as target


def make_csv(path: Path, records: list[tuple[str, str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "generator"))
        for k, n, record_id in records:
            writer.writerow((k, n, record_id, "g"))


def complete_row(n: int) -> dict:
    return {"n": n, "k": 3, "group_dimension": n + 3,
            "target_typed": True, "target_coordinates": [n, 3],
            "root_conclusion_matches_target": True, "search_status": "complete",
            "search_complete": True, "proven_steps": 2, "open_goals": 0,
            "web_key": "generic-complete-proof", "web_partial": False,
            "web_steps": 2, "web_lines": 3, "web_error": None}


def test_inventory_deduplicates_csv_rows_and_sorts_n(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("3", "59", "0"), ("3", "4", "0"),
                    ("3", "4", "1"), ("2", "8", "0"), ("3", "2", "0")])
    assert target.registered_three_stem(path) == (
        {"n": 2, "k": 3, "csv_rows": 1},
        {"n": 4, "k": 3, "csv_rows": 2},
        {"n": 59, "k": 3, "csv_rows": 1},
    )


def test_inventory_skips_k3_stem_separator_without_counting_it(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "4", "0", "inf", "ν4"))
        writer.writerow(("3", "4", "1", "4", "E ν'"))
        writer.writerow(("3", "", "", "", ""))
        writer.writerow(("4", "2", "0", "4", "η2ν'"))
    assert target.registered_three_stem(path) == (
        {"n": 2, "k": 3, "csv_rows": 1},
        {"n": 4, "k": 3, "csv_rows": 2},
    )


def test_inventory_skips_actual_sphere_csv_stem_boundary_shape(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text(
        "k,n,id,orders,generator,P,P_coe,E,E_coe,H,H_coe,Element,gen_coe,hyouji,orders2\n"
        "3,3,0,4,nu_prime,,,,,,,,,,\n"
        "3,,,,,,,,,,,,,,\n"
        "4,2,0,4,other,,,,,,,,,,\n",
        encoding="utf-8-sig",
    )
    assert target.registered_three_stem(path) == (
        {"n": 3, "k": 3, "csv_rows": 1},
    )


def test_inventory_rejects_k3_row_with_empty_n_and_nonempty_data(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "", "1", "4", "ν"))
    with pytest.raises(ValueError, match="invalid n for k=3 at CSV row 3"):
        target.registered_three_stem(path)


def test_inventory_rejects_unregistered_stem(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("2", "3", "0")])
    with pytest.raises(ValueError, match="no explicitly"):
        target.registered_three_stem(path)


def test_inventory_rejects_invalid_n(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("3", "1", "0")])
    with pytest.raises(ValueError, match="invalid n"):
        target.registered_three_stem(path)


def test_inventory_requires_columns(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("n,k\n3,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="requires"):
        target.registered_three_stem(path)


def test_verified_row_must_match_fixed_k_and_variable_n() -> None:
    good = complete_row(11)
    assert target.qualifies_complete(good, 11)
    assert target.classify_worker(good, 11) == "COMPLETE_AND_WEB_VERIFIED"
    assert not target.qualifies_complete(good, 3)
    bad = {**good, "k": 2}
    assert not target.qualifies_complete(bad, 11)


def test_qualified_complete_requires_actual_web_and_root() -> None:
    row = complete_row(3)
    assert not target.qualifies_complete({**row, "web_partial": True}, 3)
    assert not target.qualifies_complete({**row, "web_error": "UnverifiedProofTree"}, 3)
    assert not target.qualifies_complete({**row, "root_conclusion_matches_target": False}, 3)
    assert not target.qualifies_complete({**row, "proven_steps": 0}, 3)


def test_classification_is_fail_closed() -> None:
    row = complete_row(4)
    assert target.classify_worker({**row, "target_typed": False}, 4) == "TYPED_TARGET_UNAVAILABLE"
    assert target.classify_worker({**row, "search_status": "partial"}, 4) == "PROOF_UNFINISHED"
    assert target.classify_worker({**row, "root_conclusion_matches_target": False}, 4) == "CONCLUSION_MISMATCH"
    assert target.classify_worker({**row, "web_key": "partial-proof"}, 4) == "WEB_UNVERIFIED"


def test_parse_worker_emitted_result() -> None:
    row = {**complete_row(3), "result": "COMPLETE_AND_WEB_VERIFIED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3) == row


def test_worker_rejects_mismatched_coordinates() -> None:
    row = {**complete_row(4), "result": "COMPLETE_AND_WEB_VERIFIED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3)["result"] == "WORKER_FAILURE"


def test_worker_rejects_wrong_classification_or_exit() -> None:
    row = {**complete_row(3), "result": "PROOF_UNFINISHED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3)["result"] == "WORKER_FAILURE"
    assert target.parse_worker_output(raw, 1, 3)["result"] == "WORKER_FAILURE"


def test_worker_rejects_missing_or_invalid_json() -> None:
    assert target.parse_worker_output("no marker", 0, 3)["result"] == "WORKER_FAILURE"
    assert target.parse_worker_output(target.SENTINEL + "{invalid", 0, 3)["result"] == "WORKER_FAILURE"


def test_summary_uses_registered_coordinate_not_csv_row_count() -> None:
    domain = ({"n": 2, "k": 3, "csv_rows": 1},
              {"n": 4, "k": 3, "csv_rows": 2})
    rows = [{"n": 2, "k": 3, "result": "COMPLETE_AND_WEB_VERIFIED"},
            {"n": 4, "k": 3, "result": "PROOF_UNFINISHED"}]
    assert target.summarize_rows(rows, domain) == (
        {"domain_checked": 2, "domain_complete": 1,
         "domain_gaps": 1, "worker_failures": 0}
    )
    with pytest.raises(ValueError, match="do not match"):
        target.summarize_rows(list(reversed(rows)), domain)


def test_summary_counts_worker_failures() -> None:
    domain = ({"n": 3, "k": 3, "csv_rows": 1},)
    rows = [{"n": 3, "k": 3, "result": "WORKER_FAILURE"}]
    assert target.summarize_rows(rows, domain)["worker_failures"] == 1


def test_report_outputs_are_utf8_and_unabridged(tmp_path: Path) -> None:
    report = {"domain": [{"n": 4, "csv_rows": 2}],
              "rows": [{"n": 4, "k": 3, "result": "PROOF_UNFINISHED",
                        "diagnostics": ["生成元の型付き対応"]}],
              "domain_checked": 1, "domain_complete": 0,
              "domain_gaps": 1, "worker_failures": 0}
    json_path, md_path = tmp_path / "audit.json", tmp_path / "audit.md"
    target.write_json(json_path, report)
    target.write_markdown(md_path, report)
    assert json.loads(json_path.read_text(encoding="utf-8")) == report
    assert "\\pi_{7}^{4}" in md_path.read_text(encoding="utf-8")
    assert "CSV行" in md_path.read_text(encoding="utf-8")
