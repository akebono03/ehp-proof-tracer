"""Focused isolated tests for the R5-R9 audit utility."""
from pathlib import Path

from audit import analyze, markdown, shortest, source_files


def _fixture(tmp_path: Path):
    (tmp_path/"phase162_web_narrative_integration.py").write_text("def _phase162_ehp_leaves():\n    return ()\n",encoding="utf-8")
    (tmp_path/"phase162_r3_narrative_connection.py").write_text("def render_phase162_r3_narrative():\n    return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_proof_chain_renderer.py").write_text("def render_toda_group_proof_narrative_from_proof_chains_markdown():\n    return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_concrete_transport.py").write_text("def render_concrete_transport_proof_from_steps():\n    return ''\n",encoding="utf-8")
    (tmp_path/"web_group_proof.py").write_text("from phase165_r52_partial_proof import render_partial_proof_markdown\n",encoding="utf-8")
    (tmp_path/"phase162_pi5_3_web_replay.py").write_text("from phase162_web_narrative_integration import _phase162_ehp_leaves\ndef use():\n    return _phase162_ehp_leaves()\n",encoding="utf-8")
    tests=tmp_path/"tests"
    tests.mkdir()
    (tests/"test_old.py").write_text("from phase162_r3_narrative_connection import render_phase162_r3_narrative\n",encoding="utf-8")


def test_r9_dependency_blocks_wholesale_deletion(tmp_path):
    _fixture(tmp_path)
    result=analyze(tmp_path)
    old=result["targets"]["phase162_web_narrative_integration.py"]
    assert old["decision"]=="RETAIN_DEPENDENT_MODULE"
    assert any(x["symbol"]=="_phase162_ehp_leaves" for x in old["production_dependencies"])


def test_r9_test_only_dependency_is_not_auto_deleted(tmp_path):
    _fixture(tmp_path)
    old=analyze(tmp_path)["targets"]["phase162_r3_narrative_connection.py"]
    assert old["decision"]=="RETAIN_TEST_CONTRACT_REVIEW"
    assert old["production_dependency_count"]==0
    assert old["test_dependency_count"]==1


def test_r9_absence_does_not_imply_safe_deletion(tmp_path):
    _fixture(tmp_path)
    old=analyze(tmp_path)["targets"]["toda_group_proof_narrative_concrete_transport.py"]
    assert old["decision"]=="NO_STATIC_DEPENDENCY_REVIEW_DYNAMIC"


def test_r9_public_path_detected(tmp_path):
    _fixture(tmp_path)
    (tmp_path/"web_group_proof.py").write_text("from phase162_r3_narrative_connection import render_phase162_r3_narrative\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert not result["checks"]["normal_web_not_reaching_legacy"]


def test_r9_bom_and_archive_exclusion(tmp_path):
    _fixture(tmp_path)
    (tmp_path/"extra.phase165_r5_backup.py").write_text("invalid!",encoding="utf-8")
    (tmp_path/"bom.py").write_bytes(b"\xef\xbb\xbffrom phase162_r3_narrative_connection import render_phase162_r3_narrative\n")
    result=analyze(tmp_path)
    assert not result["parse_errors"]
    assert all("backup" not in p.name for p in source_files(tmp_path))


def test_r9_report_contains_decisions(tmp_path):
    _fixture(tmp_path)
    report=markdown(analyze(tmp_path))
    assert "RETAIN_DEPENDENT_MODULE" in report
    assert "RETAIN_TEST_CONTRACT_REVIEW" in report
    assert "## 制約と次の境界" in report


def test_r9_shortest_path():
    graph={"a.py":{"b.py"},"b.py":{"c.py"},"c.py":set()}
    assert shortest(graph,"a.py","c.py")==["a.py","b.py","c.py"]
    assert shortest(graph,"c.py","a.py") is None
