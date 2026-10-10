import csv
from pathlib import Path

import pytest

from phase163_r4_r4_role_classification import (
    build_classification,
    classify_site,
    classify_unlinked,
    write_audit,
)


def test_mapped_rule_is_only_a_candidate():
    row = classify_site({"file": "toda_rules.py", "line": 5,
                         "name": "Toda example", "status": "listed_in_boundary_mapping"})
    assert row["role_candidate"] == "literature_mapping_candidate"
    assert row["manual_review_required"] == "yes"


def test_unmapped_toda_rule_is_not_automatically_generic():
    row = classify_site({"file": "toda_rules.py", "line": 8,
                         "name": "Toda unknown", "status": "not_listed_in_boundary_mapping"})
    assert row["role_candidate"] == "toda_rule_unclassified"


def test_non_toda_rule_is_candidate_only():
    row = classify_site({"file": "relation_rules.py", "line": 4,
                         "name": "composition", "status": "not_listed_in_boundary_mapping"})
    assert row["role_candidate"] == "general_inference_candidate"
    assert row["manual_review_required"] == "yes"


def test_dynamic_name_not_assigned_a_mathematical_role():
    row = classify_site({"file": "toda_rules.py", "line": 2,
                         "name": None, "status": "dynamic_name_unverified"})
    assert row["role_candidate"] == "dynamic_rule_name_unverified"


def test_unlinked_is_not_equivalent_to_missing_mathematical_statement():
    row = classify_unlinked({"locator": "(5.1)", "key": "k", "role": "OTHER"})
    assert row["mathematical_equivalence_confirmed"] == "no"
    assert row["status"] == "unlinked_by_literal_name"


def test_counts_preserve_constructor_site_unit():
    result = build_classification({"rule_sites": [
        {"file": "toda_rules.py", "line": 1, "name": "x", "status": "not_listed_in_boundary_mapping"},
        {"file": "toda_rules.py", "line": 2, "name": "x", "status": "not_listed_in_boundary_mapping"},
    ], "unlinked_components": []})
    assert result["counts"]["toda_unmapped_literal_sites"] == 2
    assert result["counts"]["distinct_literal_rule_names"] == 1


def test_requires_live_sources_without_fabrication(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_audit(tmp_path, tmp_path / "out")
