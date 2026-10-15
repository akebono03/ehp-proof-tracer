from pathlib import Path
from audit import inspect, save_report, calls_in, is_audit, read_source, TARGETS
import ast
import json

def make_project(tmp_path:Path):
    (tmp_path/"tests").mkdir()
    (tmp_path/"phase162_ehp_leaf_inputs.py").write_text("def _phase162_ehp_leaves(): return ()\n",encoding="utf-8")
    (tmp_path/"phase162_pi5_3_web_replay.py").write_text(
        "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n"
        "def replay(): return _phase162_ehp_leaves()\n",encoding="utf-8")
    (tmp_path/"phase162_web_narrative_integration.py").write_text(
        "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n"
        "def build_phase162_web_validated_isomorphism_markdown(): return _phase162_ehp_leaves()\n",encoding="utf-8")
    (tmp_path/"phase162_r3_narrative_connection.py").write_text(
        "def render_phase162_r3_narrative(): return 1\n"
        "def render_phase162_r3_with_public_references(): return render_phase162_r3_narrative()\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_proof_chain_renderer.py").write_text(
        "def render_toda_group_proof_narrative_from_proof_chains_markdown(): return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_concrete_transport.py").write_text(
        "def render_concrete_transport_proof_from_steps(): return ''\n",encoding="utf-8")
    (tmp_path/"web_group_proof.py").write_text("def build_standard_web_group_proof_view(): return None\n",encoding="utf-8")
    for module, names in TARGETS.items():
        path=tmp_path/(module+".py")
        present=path.read_text(encoding="utf-8")
        for name in names:
            if "def "+name+"(" not in present and not (name=="_phase162_ehp_leaves" and module=="phase162_web_narrative_integration"):
                present += "def "+name+"(): return None\n"
        path.write_text(present,encoding="utf-8")

def test_r14_reexport_is_not_missing(tmp_path):
    make_project(tmp_path)
    r=inspect(tmp_path)
    assert r["status"]=="REVIEW_REQUIRED"
    assert r["decisions"]["phase162_web_narrative_integration:_phase162_ehp_leaves"]["state"]=="REEXPORTED"

def test_r14_application_calls_block_removal(tmp_path):
    make_project(tmp_path)
    (tmp_path/"client.py").write_text(
        "from phase162_r3_narrative_connection import render_phase162_r3_narrative\n"
        "def client(): return render_phase162_r3_narrative()\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["decisions"]["phase162_r3_narrative_connection:render_phase162_r3_narrative"]["decision"]=="KEEP_APPLICATION_CALLER"

def test_r14_test_contract_detected(tmp_path):
    make_project(tmp_path)
    (tmp_path/"tests"/"test_old.py").write_text(
        "from phase162_r3_narrative_connection import render_phase162_r3_narrative\n"
        "def test_old(): assert render_phase162_r3_narrative() == 1\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["decisions"]["phase162_r3_narrative_connection:render_phase162_r3_narrative"]["decision"]=="KEEP_TEST_API_PENDING_MIGRATION"

def test_r14_missing_reexport_is_failure(tmp_path):
    make_project(tmp_path)
    (tmp_path/"phase162_web_narrative_integration.py").write_text(
        "def build_phase162_web_validated_isomorphism_markdown(): return 1\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["status"]=="PRECONDITION_FAILED"

def test_r14_bom_and_archives(tmp_path):
    make_project(tmp_path)
    (tmp_path/"client.py").write_bytes(b"\xef\xbb\xbf"+b"def client(): return 1\n")
    (tmp_path/"phase162_r3_narrative_connection.phase165_r43_backup.py").write_text("def broken(:\n",encoding="utf-8")
    assert inspect(tmp_path)["guards"]["no_parse_errors"]

def test_r14_report_outputs(tmp_path):
    make_project(tmp_path)
    r=inspect(tmp_path)
    save_report(r,tmp_path/"reports")
    assert json.loads((tmp_path/"reports"/"audit.json").read_text(encoding="utf-8"))["phase"]=="165 R5-R14"
    assert "一括撤去" in (tmp_path/"reports"/"review.md").read_text(encoding="utf-8")

def test_r14_audit_classification():
    assert is_audit(Path("audit_phase144.py"))
    assert not is_audit(Path("phase162_web_narrative_integration.py"))

def test_r14_call_parser():
    assert calls_in(ast.parse("run(); object.render()"))=={"run","render"}
