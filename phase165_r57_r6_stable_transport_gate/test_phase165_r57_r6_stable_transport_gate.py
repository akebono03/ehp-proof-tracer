"""R57-R6 read-only transport gate tests; no full pytest suite."""
import ast
from pathlib import Path

import pytest

from audit import audit_stable_transport_boundary


def _create_sources(tmp_path: Path, *, wired: bool = False) -> None:
    provider = "toda_45_generic_finite_cyclic_transport_inference_rule()" if wired else "expand_generic_iso_goal(goal)"
    files = {
        "phase165_r52_r9_shared_math.py": "def shared_expansion_provider():\n    " + provider + "\n",
        "toda_stable_group_transport.py": "def toda_45_generic_finite_cyclic_transport_inference_rule():\n    pass\n",
        "toda_stable_transport.py": "def build_canonical_toda_45_isomorphism_step():\n    pass\n",
        "toda_group_proof_narrative_renderer.py": "def _phase160_r7_render_stable_finite_cyclic_transport_narrative():\n    pass\n",
        "phase165_r55_nk_only_goal.py": "def search_group_from_registered_goal():\n    return list()\n",
    }
    for name, contents in files.items():
        (tmp_path / name).write_text(contents, encoding="utf-8")


def test_r576_existing_unwired_transport_is_flagged(tmp_path):
    _create_sources(tmp_path)
    result = audit_stable_transport_boundary(tmp_path)
    assert result["shared_search_provider_calls_transport_rule"] is False
    assert result["old_toda45_transport_rules"] == ["toda_45_generic_finite_cyclic_transport_inference_rule"]
    assert result["delete_live_transport_renderer_allowed"] is False
    assert result["proof_for_pi5_4_established"] is False


def test_r576_wired_transport_is_detected(tmp_path):
    _create_sources(tmp_path, wired=True)
    assert audit_stable_transport_boundary(tmp_path)["shared_search_provider_calls_transport_rule"] is True


def test_r576_missing_source_fails_closed(tmp_path):
    _create_sources(tmp_path)
    (tmp_path / "toda_stable_transport.py").unlink()
    with pytest.raises(FileNotFoundError, match="Missing installed"):
        audit_stable_transport_boundary(tmp_path)


def test_r576_does_not_modify_source(tmp_path):
    _create_sources(tmp_path)
    before = {path.name: path.read_bytes() for path in tmp_path.glob("*.py")}
    audit_stable_transport_boundary(tmp_path)
    assert before == {path.name: path.read_bytes() for path in tmp_path.glob("*.py")}
