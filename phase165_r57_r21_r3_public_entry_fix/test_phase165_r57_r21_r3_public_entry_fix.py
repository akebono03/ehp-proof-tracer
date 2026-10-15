"""R57-R21-R3 narrow public renderer regression tests."""
from __future__ import annotations

from pathlib import Path
import pytest
from install import install, effective_definition


def _fixture(tmp_path: Path, implementation: str) -> Path:
    (tmp_path / "phase165_r52_partial_proof.py").write_text(
        "from __future__ import annotations\n" + implementation, encoding="utf8"
    )
    (tmp_path / "toda_group_proof_generic_narrative_renderer.py").write_text(
        "def render_toda_partial_proof_narrative_markdown(result):\n    return 'test'\n",
        encoding="utf8",
    )
    return tmp_path


def test_r3_updates_last_effective_public_entry(tmp_path: Path):
    code = (
        "def render_partial_proof_markdown(result):\n    return 'old'\n\n"
        "def render_partial_proof_markdown(result):\n    return render_old(result)\n"
    )
    root = _fixture(tmp_path, code)
    status = install(root, Path(__file__).resolve().parent)
    assert status == "INSTALLED"
    updated = (root / "phase165_r52_partial_proof.py").read_text(encoding="utf8")
    assert "render_toda_partial_proof_narrative_markdown" in effective_definition(updated)
    assert "return render_old(result)" not in effective_definition(updated)


def test_r3_reinstall_is_idempotent(tmp_path: Path):
    root = _fixture(tmp_path, "def render_partial_proof_markdown(result):\n    return render_old(result)\n")
    package = Path(__file__).resolve().parent
    assert install(root, package) == "INSTALLED"
    first = (root / "phase165_r52_partial_proof.py").read_bytes()
    assert install(root, package) == "ALREADY_INSTALLED"
    assert (root / "phase165_r52_partial_proof.py").read_bytes() == first


def test_r3_unknown_entry_rejected(tmp_path: Path):
    root = _fixture(tmp_path, "def render_partial_proof_markdown(result):\n    return 42\n")
    with pytest.raises(RuntimeError, match="unrecognized"):
        install(root, Path(__file__).resolve().parent)


def test_r3_existing_targeted_render_contract():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=3, k=1)
    rendered = render_partial_proof_markdown(result)
    assert "## 証明対象" in rendered
    assert "## 使用する結果" in rendered
    assert "## 証明\n" in rendered
    heading = rendered.split("## 証明対象", 1)[1].split("## 使用する結果", 1)[0]
    assert "\\pi_{5}^{5}" not in heading
    assert any(t in heading for t in ("\\pi_{4}^{3}", "π43", "π_4^3"))
