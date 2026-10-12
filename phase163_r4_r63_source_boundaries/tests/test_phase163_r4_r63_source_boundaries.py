import copy
import json
import os
from pathlib import Path

import pytest

from phase163_r4_r63_source_boundaries import (
    SPAN_PROPOSALS,
    audit_boundaries,
    load_inputs,
    write_reports,
)


@pytest.fixture
def evidence():
    root=Path(__file__).resolve().parents[2]
    inventory=root/"phase163_r4_r62_output"/"remaining_definitions.json"
    if not inventory.exists():
        # ZIP-independent local verification from user-provided preceding output.
        inventory=root/"remaining_definitions.json"
    tex_root=Path(os.environ.get("EHP_R63_TEX_ROOT",str(root)))
    return load_inputs(inventory,tex_root)


def test_sixteen_source_spans_cover_excerpts(evidence):
    data,sources=evidence
    result=audit_boundaries(data,sources)
    assert result["candidate_count"]==16
    assert result["source_excerpt_verified_count"]==16
    assert all(r["excerpt_exactly_contained"] for r in result["records"])


def test_all_upstream_candidates_covered(evidence):
    data,sources=evidence
    result=audit_boundaries(data,sources)
    assert {r["editorial_key"] for r in result["records"]}==set(SPAN_PROPOSALS)


def test_source_lines_are_within_proposed_span(evidence):
    data,sources=evidence
    result=audit_boundaries(data,sources)
    assert all(r["proposed_start_line"]<=r["source_line"]<=r["proposed_end_line"] for r in result["records"])


def test_split_notation_blocks_retained(evidence):
    data,sources=evidence
    result=audit_boundaries(data,sources)
    mapping={r["editorial_key"]:r for r in result["records"]}
    assert (mapping["nu_n_notation"]["proposed_start_line"],mapping["nu_n_notation"]["proposed_end_line"])==(605,607)
    assert (mapping["eta_n_cubed_notation"]["proposed_start_line"],mapping["eta_n_cubed_notation"]["proposed_end_line"])==(608,612)
    assert "SHARED_ADJACENT_NOTATION_BLOCK" in mapping["eta_n_cubed_notation"]["warning_codes"]


def test_complex_bracket_not_false_closed(evidence):
    data,sources=evidence
    r={x["editorial_key"]:x for x in audit_boundaries(data,sources)["records"]}["stable_toda_bracket"]
    assert r["proposed_end_line"]==1266
    assert "MATHEMATICAL_CONTEXT_OUTSIDE_SPAN" in r["warning_codes"]


def test_unknown_semantics_not_promoted(evidence):
    data,sources=evidence
    result=audit_boundaries(data,sources)
    assert result["mathematical_boundary_verified_count"]==0
    assert result["publication_position_verified_count"]==0
    assert all(not r["semantic_registration_allowed"] for r in result["records"])
    assert all(r["production_reference_id"] is None for r in result["records"])


def test_duplicate_key_rejected(evidence):
    data,sources=evidence
    mutated=copy.deepcopy(data)
    mutated["records"][1]["editorial_key"]=mutated["records"][0]["editorial_key"]
    with pytest.raises(ValueError):
        audit_boundaries(mutated,sources)


def test_changed_excerpt_rejected(evidence):
    data,sources=evidence
    mutated=copy.deepcopy(data)
    mutated["records"][0]["source_excerpt"]="fake TeX excerpt"
    with pytest.raises(ValueError,match="source excerpt changed"):
        audit_boundaries(mutated,sources)


def test_missing_source_rejected(evidence,tmp_path):
    data,sources=evidence
    with pytest.raises(FileNotFoundError):
        load_inputs(tmp_path/"missing.json",tmp_path)


def test_output_files(evidence,tmp_path):
    data,sources=evidence
    write_reports(audit_boundaries(data,sources),tmp_path)
    for n in ("source_boundaries.json","source_boundaries.csv","report.md"):
        assert (tmp_path/n).is_file()
    assert json.loads((tmp_path/"source_boundaries.json").read_text(encoding="utf-8"))["candidate_count"]==16
