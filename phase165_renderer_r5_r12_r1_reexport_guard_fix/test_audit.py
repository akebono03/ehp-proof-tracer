"""Focused unit tests; no project-wide pytest."""
import ast
from pathlib import Path
from tempfile import TemporaryDirectory

from audit import audit, local_calls, production_files, references_in, review


def test_from_import_call():
    tree = ast.parse("from old import target as t\nt()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"import", "call"}


def test_module_import_call():
    tree = ast.parse("import old as obj\nobj.target()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"module_import", "call"}


def test_unrelated_symbol_excluded():
    tree = ast.parse("from old import different\ndifferent()\n")
    assert references_in(tree, "old", "target") == []


def test_local_calls():
    tree = ast.parse("def first():\n    target()\n\ndef second():\n    other()\n")
    assert local_calls(tree, "target") == [{"function": "first", "line": 2}]


def test_backup_files_excluded():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "active.py").write_text("pass\n", encoding="utf-8")
        (root / "active.phase165_r48_backup.py").write_text("pass\n", encoding="utf-8")
        selected = [p.name for p, _ in production_files(root)]
        assert selected == ["active.py"]


def test_audit_fail_closed_when_r5_r11_missing():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        assert result["status"] == "PRECONDITION_FAILED"
        assert not result["guards"]["r5_r11_shared_file_exists"]


def test_review_contains_decisions():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        text = review(result)
        assert "関数別の依存" in text
        assert "PRECONDITION_FAILED" in text


def test_shared_reexport_is_valid_r5_r11_state():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "phase162_ehp_leaf_inputs.py").write_text(
            "def _phase162_ehp_leaves():\n    return ()\n", encoding="utf-8"
        )
        old = "phase162_web_narrative_integration.py"
        (root / old).write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n" +
            "\n".join("def " + n + "():\n    pass" for n in (
                "build_phase162_web_validated_isomorphism_markdown",
                "_build_phase162_legacy_validated_isomorphism_markdown",
                "_build_phase162_existing_group_connection",
                "_format_phase162_proof_sentences",
                "_compose_phase162_group_conclusion",
            )) + "\n", encoding="utf-8"
        )
        (root / "phase162_pi5_3_web_replay.py").write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n", encoding="utf-8"
        )
        (root / "phase162_r3_narrative_connection.py").write_text(
            "\n".join("def " + n + "():\n    pass" for n in (
                "render_phase162_r3_narrative",
                "render_phase162_r3_with_public_references",
                "_phase162_legacy_ehp_body",
            )) + "\n", encoding="utf-8"
        )
        result = audit(root)
        assert result["status"] == "REVIEW_REQUIRED"
        assert result["guards"]["all_old_entry_symbols_defined_or_shared_reexported"]
        key = "phase162_web_narrative_integration:_phase162_ehp_leaves"
        assert result["functions"][key]["decision"] == "RETAIN_SHARED_REEXPORT"


def test_missing_shared_reexport_still_fails_closed():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "phase162_ehp_leaf_inputs.py").write_text(
            "def _phase162_ehp_leaves():\n    return ()\n", encoding="utf-8"
        )
        (root / "phase162_web_narrative_integration.py").write_text(
            "pass\n", encoding="utf-8"
        )
        (root / "phase162_pi5_3_web_replay.py").write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n", encoding="utf-8"
        )
        result = audit(root)
        assert result["status"] == "PRECONDITION_FAILED"
        assert not result["guards"]["legacy_web_reexports_shared_leaves"]
