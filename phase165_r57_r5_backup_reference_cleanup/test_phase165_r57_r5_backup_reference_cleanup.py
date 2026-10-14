"""R57-R5: classify live references before deleting a dead helper."""
import ast
from pathlib import Path

import pytest

from install import classify_reference, remove_dead_helper, references_in_live_sources


def _fixture_source():
    return (
        "def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(p):\n"
        "    return 'old'\n\n"
        "def render_toda_group_proof_narrative_markdown(p):\n"
        "    return 'shared'\n\n"
        "_phase160_r7_previous_public_narrative_renderer = render_toda_group_proof_narrative_markdown\n\n"
        "def render_toda_group_proof_narrative_markdown(p):\n"
        "    return _phase160_r7_previous_public_narrative_renderer(p)\n"
    )


def test_r57_r5_classifies_backups_separately(tmp_path):
    assert classify_reference(tmp_path / "renderer.phase165_r44_pre_cleanup.py", tmp_path) == "backup"
    assert classify_reference(tmp_path / "renderer.phase165_r43_backup.py", tmp_path) == "backup"
    assert classify_reference(tmp_path / "test_live.py", tmp_path) == "test"
    assert classify_reference(tmp_path / "production.py", tmp_path) == "production"


def test_r57_r5_only_backup_mentions_do_not_prevent_cleanup(tmp_path):
    target = tmp_path / "toda_group_proof_narrative_renderer.py"
    target.write_text(_fixture_source(), encoding="utf-8")
    (tmp_path / "renderer.phase165_r43_backup.py").write_text("# _phase159_render_pi_n_plus_1_n_stable_transport_narrative", encoding="utf-8")
    report = references_in_live_sources(tmp_path, target)
    assert not report["production"] and not report["test"]
    assert report["backup"] == ["renderer.phase165_r43_backup.py"]
    updated, removed = remove_dead_helper(target.read_text(encoding="utf-8"))
    assert removed
    assert "def _phase159_render_pi_n_plus_1_n_stable_transport_narrative" not in updated
    namespace = {}
    exec(compile(updated, "<r575>", "exec"), namespace)
    assert namespace["render_toda_group_proof_narrative_markdown"](None) == "shared"


def test_r57_r5_reports_production_and_test_references(tmp_path):
    target = tmp_path / "toda_group_proof_narrative_renderer.py"
    target.write_text(_fixture_source(), encoding="utf-8")
    (tmp_path / "consumer.py").write_text("from x import _phase159_render_pi_n_plus_1_n_stable_transport_narrative", encoding="utf-8")
    (tmp_path / "test_consumer.py").write_text("# _phase159_render_pi_n_plus_1_n_stable_transport_narrative", encoding="utf-8")
    report = references_in_live_sources(tmp_path, target)
    assert report["production"] == ["consumer.py"]
    assert report["test"] == ["test_consumer.py"]


def test_r57_r5_keeps_any_helper_called_by_surviving_renderer():
    source = _fixture_source().replace("return 'shared'", "return _phase159_render_pi_n_plus_1_n_stable_transport_narrative(p)")
    with pytest.raises(RuntimeError, match="referenced"):
        remove_dead_helper(source)


def test_r57_r5_cleanup_idempotent_and_preserves_both_public_functions():
    source, changed = remove_dead_helper(_fixture_source())
    assert changed
    assert len([n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "render_toda_group_proof_narrative_markdown"]) == 2
    again, changed = remove_dead_helper(source)
    assert not changed and again == source
