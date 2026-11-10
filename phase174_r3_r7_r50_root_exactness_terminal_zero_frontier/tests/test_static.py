"""R50 is scoped to read-only canonical proof inspection with cited sources."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r50_modules_parse_and_do_not_contain_ellipsis() -> None:
    for relative in (
        "audit.py", "source_guard.py", "tests/test_static.py",
        "tests/test_guard.py", "tests/test_frontier.py",
    ):
        syntax = ast.parse((PACKAGE / relative).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(syntax)
        )


def test_r50_runner_is_focused_and_read_only() -> None:
    text = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in text
    assert "--import-mode=$Mode" in text
    assert "R49_FRONTIER_REGRESSION" in text
    assert "R3_EHP_ROOT_REGRESSION" in text
    assert "TODA51_ZERO_REGRESSION" in text
    assert "FULL_PYTEST=False" in text
    assert "git reset" not in text
    assert "git clean" not in text
    assert "install.py" not in text


def test_r50_only_uses_existing_toda51_and_prop42_inferences() -> None:
    text = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in text
    assert "search_registered_partial_proof(" in text
    assert '"Toda (5.1) general below-diagonal zero specialization"' in text
    assert "proof_has_toda51_zero_ancestor" in text
    assert "canonical_root_four_independent_inference_parents" in text
    assert "root_cited_ancestors" in text
    assert "web_http_checked" in text
    assert "new_givens" in text


def test_root_proof_is_not_marked_complete_unconditionally() -> None:
    text = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "result.status is ProofSearchStatus.COMPLETE" in text
    assert '"canonical_root_verified_complete"' in text
    assert "root_four_parents" in text
    assert "root_cited_ancestors" in text
    assert "terminal_cited" in text
