"""Tests for the read-only evidence extractor."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import evaluate_static_guards, flatten, selected


def test_flatten_keeps_nested_dict_and_list_paths():
    assert flatten({"observed": {"goals": [{"status": "open"}]}}) == [
        {"path": "observed.goals[0].status", "value": "open"},
    ]


def test_selected_retains_original_values():
    assert selected(flatten({"other": 4, "observed": {"zero": True}})) == [
        {"path": "observed.zero", "value": True},
    ]


def test_no_fabricated_observed_payload():
    assert selected(flatten({"unrelated": "x"})) == []


def test_static_inventory_reports_missing_guards():
    guards = evaluate_static_guards("screened_general_law(bridge)")
    assert guards["screened_general_law"] is True
    assert guards["exact_relation_match"] is False
