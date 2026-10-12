import copy
import hashlib
import json
from pathlib import Path

import pytest

from phase163_r4_r79_fixed_statement_preview import CLAIMS, OWNERS, build_preview, load_sources, write_results

ROOT = Path(__file__).resolve().parents[2]


def fixture_sources():
    sources = {name: ["" for _ in range(1100)] for _, _, name, _, _ in OWNERS.values()}
    for owner, (kind, locator, name, begin, end) in OWNERS.items():
        sources[name][begin - 1] = f"\\begin{{{kind.value}}}\\label{{{owner}}}"
        sources[name][end - 1] = f"\\end{{{kind.value}}}"
    for owner, name, start, end, slug in CLAIMS:
        sources[name][start-1] += "\\begin{equation}" if slug == "ehp_exact_sequence" else "\\["
        sources[name][end-1] += "\\]"
    return sources


def fixture_r78():
    owners=["prop:1-6"]*3+["thm:2.4"]*4+["prop:2.5"]*2+["prop:4.2"]
    return {"phase":"163 R4-R78","preview_proof_internal_count":10,
            "records":[{"preview_status":"PROOF_INTERNAL_PREVIEW",
                        "preview_assertion_id":f"preview:proof-step:{i}",
                        "source_owner_label":owner,"original_excerpt_sha256":"digest"}
                       for i, owner in enumerate(owners)]}


def test_expected_fixed_counts():
    result=build_preview(fixture_r78(), fixture_sources())
    assert result["fixed_counts_by_owner"]=={"prop:1-6":3,"thm:2.4":2,"prop:2.5":2,"prop:4.2":1}
    assert result["preview_proof_internal_count"]==10


def test_fixed_source_bounded_not_proof():
    result=build_preview(fixture_r78(),fixture_sources())
    for r in result["fixed_statement_previews"]:
        assert "\\[" in r["claim_text"] or "\\begin{equation}" in r["claim_text"]
        assert "Proof." not in r["claim_text"]


def test_duplicate_internal_ids_rejected():
    bad=fixture_r78()
    bad["records"][1]["preview_assertion_id"]=bad["records"][0]["preview_assertion_id"]
    with pytest.raises(ValueError): build_preview(bad,fixture_sources())


def test_modified_statement_boundary_rejected():
    src=fixture_sources()
    src["Toda_01_corrected.tex"][964]=""
    with pytest.raises(ValueError):build_preview(fixture_r78(),src)


def test_invalid_phase_rejected():
    bad=fixture_r78();bad["phase"]="163 R4-R77"
    with pytest.raises(ValueError):build_preview(bad,fixture_sources())


def test_hash_changes_rejected(tmp_path):
    (tmp_path/"one.tex").write_bytes(b"a")
    with pytest.raises(ValueError):load_sources(tmp_path,expected_hashes={"one.tex":hashlib.sha256(b"b").hexdigest()})


def test_write_report(tmp_path):
    result=build_preview(fixture_r78(),fixture_sources())
    write_results(result,tmp_path)
    doc=json.loads((tmp_path/"fixed_statement_preview.json").read_text(encoding="utf-8"))
    assert len(doc["fixed_statement_previews"])==8
    assert "正式 ID" in (tmp_path/"report.md").read_text(encoding="utf-8")


def test_real_r78_if_present():
    p=ROOT/"phase163_r4_r78_output"/"registry_preview.json"
    if not p.exists():
        pytest.skip("R78 output only available on user project")
    data=json.loads(p.read_text(encoding="utf-8"))
    result=build_preview(data,fixture_sources())
    assert result["preview_fixed_statement_count"]==8


def test_no_production_change():
    result=build_preview(fixture_r78(),fixture_sources())
    assert result["production_registry_modified"] is False
    assert result["production_ids_allocated"] is False
    assert result["semantic_registration_allowed_count"]==0
