"""Focused offline tests for the R3 report readout; no production imports."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase173_r3_frontier_readout.readout import (
    EXPECTED_HEAD,
    format_report,
    load_report,
)


def sample_report() -> dict:
    return {
        "head": EXPECTED_HEAD,
        "mode": "AUDIT_ONLY",
        "rows": [
            {
                "n": n,
                "k": 3,
                "source_locator": "Proposition 5.6",
                "screened_given_count": 26 if n == 4 else 27,
                "target_direct_given_count": 0,
                "root_candidate_count": 1 if n == 4 else 3,
                "roots": [
                    {
                        "rule": "mock inference candidate",
                        "children": [
                            {
                                "type": "Relation",
                                "repr": "Relation(mock)",
                                "child_proposal_count": 0,
                                "child_proposal_rules": [],
                                "exact_screened_given": False,
                            }
                        ],
                    }
                    for _ in range(1 if n == 4 else 3)
                ],
                "prior_sources": [
                    {
                        "n": 3,
                        "k": 3,
                        "eligible": True,
                        "reason": "prior_fixed_source",
                        "stable_source": False,
                    }
                ],
            }
            for n in (4, 5)
        ],
    }


def write_report(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_valid_report_formats_all_roots(tmp_path: Path) -> None:
    report = load_report(write_report(tmp_path / "audit.json", sample_report()))
    text = format_report(report)
    assert text.count("  ROOT ") == 4
    assert "pi_7^4" in text
    assert "pi_8^5" in text
    assert "proposals=0 exact_given=False" in text
    assert "OBSERVATION_IS_NOT_A_PROOF=True" in text


def test_missing_report_fails(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="not found"):
        load_report(tmp_path / "missing.json")


@pytest.mark.parametrize("field,value", [
    ("head", "unknown"),
    ("mode", "PROOF_COMPLETE"),
    ("rows", []),
])
def test_invalid_top_level_rejected(tmp_path: Path, field: str, value: object) -> None:
    data = sample_report()
    data[field] = value
    with pytest.raises(ValueError):
        load_report(write_report(tmp_path / "audit.json", data))


def test_direct_target_given_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["target_direct_given_count"] = 1
    with pytest.raises(ValueError, match="direct GIVEN"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_truncated_root_list_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][1]["roots"].pop()
    with pytest.raises(ValueError, match="truncated"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_target_order_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"].reverse()
    with pytest.raises(ValueError, match="coordinates"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_malformed_root_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"] = None
    with pytest.raises(ValueError, match="Malformed"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_duplicate_child_reports_unprobed(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"][0] = {
        "type": "Relation", "repr": "Relation(duplicate)"
    }
    text = format_report(load_report(write_report(tmp_path / "audit.json", data)))
    assert "NOT_PROBED_DUPLICATE" in text


def test_probe_error_reported(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"][0]["child_probe_error"] = "ValueError: x"
    text = format_report(load_report(write_report(tmp_path / "audit.json", data)))
    assert "PROBE_ERROR: ValueError: x" in text
