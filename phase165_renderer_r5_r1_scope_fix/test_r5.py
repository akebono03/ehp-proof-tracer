"""Targeted checks of R4 retirement and R3's common narrative entry."""
from __future__ import annotations

from pathlib import Path

import pytest

from audit import FOCUS, audit


def _sample_project(tmp_path: Path) -> Path:
    for filename in FOCUS:
        (tmp_path / filename).write_text('from __future__ import annotations\n', encoding="utf-8")
    (tmp_path / "toda_group_proof_narrative_renderer.py").write_text(
        "def render_toda_group_proof_narrative_markdown(x):\n    return x\n"
        "def render_toda_partial_proof_narrative_markdown(x):\n    return x\n"
        "def render_narrative_proof_model(model):\n"
        "    if model.status is ProofSearchStatus.COMPLETE:\n"
        "        return render_completed_shared_narrative(model.source)\n"
        "    return render_toda_partial_proof_narrative_markdown(model.source)\n",
        encoding="utf-8",
    )
    (tmp_path / "phase165_r52_partial_proof.py").write_text(
        "def render_partial_proof_markdown(result):\n"
        "    return render_narrative_proof_model(build_narrative_proof_model(result))\n",
        encoding="utf-8",
    )
    (tmp_path / "web_group_proof.py").write_text(
        "def build_standard_web_group_proof_view():\n"
        "    return build_partial_web_group_proof_view()\n",
        encoding="utf-8",
    )
    (tmp_path / "phase165_r52_r3_web_adapter.py").write_text(
        "def build_partial_web_group_proof_view(result):\n"
        "    return render_partial_proof_markdown(result)\n",
        encoding="utf-8",
    )
    (tmp_path / "phase165_renderer_narrative_model.py").write_text(
        "class NarrativeProofModel:\n"
        "    def __init__(self):\n"
        "        self.proven_steps = ()\n"
        "        self.open_goals = ()\n",
        encoding="utf-8",
    )
    return tmp_path


def test_r5_auditor_accepts_single_static_route(tmp_path):
    project = _sample_project(tmp_path)
    result = audit(project)
    assert result["status"] == "STATIC_PASS_REVIEW_REQUIRED"
    assert all(result["checks"].values())


def test_r5_auditor_detects_deleted_module_restored(tmp_path):
    project = _sample_project(tmp_path)
    module = project / "toda_group_proof_generic_narrative_renderer"
    module.mkdir()
    (module / "__init__.py").write_text("", encoding="utf-8")
    assert not audit(project)["checks"]["no_legacy_alias"]


def test_r5_auditor_detects_old_import_with_bom(tmp_path):
    project = _sample_project(tmp_path)
    (project / "extra.py").write_text(
        "from toda_group_proof_generic_narrative_renderer import old\n", encoding="utf-8-sig"
    )
    result = audit(project)
    assert not result["checks"]["no_legacy_imports"]
    assert result["counts"]["legacy_import_statements"] == 1


def test_r5_auditor_detects_duplicate_public_function(tmp_path):
    project = _sample_project(tmp_path)
    target = project / "toda_group_proof_narrative_renderer.py"
    with target.open("a", encoding="utf-8") as stream:
        stream.write("\ndef render_toda_group_proof_narrative_markdown(x):\n    return x\n")
    assert not audit(project)["checks"]["one_public_complete_narrative_definition"]


def test_r5_partial_arbitrary_target_uses_canonical_dispatcher(monkeypatch):
    import toda_group_proof_narrative_renderer as canonical
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result, render_partial_proof_markdown
    result = make_partial_proof_result(
        n=200, k=90, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("missing typed inference",), diagnostics=("No applicable rule",),
    )
    original = canonical.render_narrative_proof_model
    calls = []

    def observed(model):
        calls.append(model)
        return original(model)

    monkeypatch.setattr(canonical, "render_narrative_proof_model", observed)
    markdown = render_partial_proof_markdown(result)
    assert len(calls) == 1
    assert calls[0].source is result
    assert r"\pi_{290}^{200}" in markdown
    assert "missing typed inference" in markdown
    assert "□" not in markdown


def test_r5_web_modes_do_not_synthesize_conclusion(monkeypatch):
    import phase165_r55_nk_only_goal as goals
    import toda_group_proof_narrative_renderer as canonical
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from web_group_proof import build_standard_web_group_proof_view
    partial = make_partial_proof_result(
        n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED,
        open_goals=("unproved group goal",),
    )
    monkeypatch.setattr(goals, "search_group_from_registered_goal", lambda *, n, k: partial)
    calls = []
    original = canonical.render_narrative_proof_model

    def observed(model):
        calls.append(model)
        return original(model)

    monkeypatch.setattr(canonical, "render_narrative_proof_model", observed)
    view = build_standard_web_group_proof_view(n=200, k=90, mode="narrative")
    assert view.partial_result
    assert view.rendered_lines
    assert len(calls) == 1
    assert calls[0].source is partial
    trace_view = build_standard_web_group_proof_view(n=200, k=90, mode="trace")
    assert trace_view.partial_result
    assert not trace_view.rendered_lines
    assert len(calls) == 1


def test_r5_complete_pi32_keeps_verified_public_contract():
    from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    markdown = render_partial_proof_markdown(result)
    assert "証明対象" in markdown
    assert "使用する結果" in markdown
    assert "証明" in markdown
    assert "□" in markdown
    assert "群構造の証明状態: unknown" not in markdown


def test_r5_excludes_archived_installer_and_backup_trees(tmp_path):
    project = _sample_project(tmp_path)
    for folder in ("phase165_renderer_r4_legacy_retirement", ".phase165_renderer_r4_backup", "historical_snapshot"):
        archive = project / folder
        archive.mkdir()
        (archive / "old.py").write_text(
            "from toda_group_proof_generic_narrative_renderer import old\n",
            encoding="utf-8",
        )
    result = audit(project)
    assert result["checks"]["no_legacy_imports"]
    assert result["counts"]["legacy_import_statements"] == 0
    assert result["counts"]["scan_scope"] == "project_root_and_tests_only"


def test_r5_includes_official_tests_package(tmp_path):
    project = _sample_project(tmp_path)
    test_root = project / "tests"
    test_root.mkdir()
    (test_root / "test_legacy.py").write_text(
        "from toda_group_proof_generic_narrative_renderer import old\n",
        encoding="utf-8",
    )
    result = audit(project)
    assert not result["checks"]["no_legacy_imports"]
    assert result["old_imports"] == [{"file": "tests/test_legacy.py", "line": 1}]
