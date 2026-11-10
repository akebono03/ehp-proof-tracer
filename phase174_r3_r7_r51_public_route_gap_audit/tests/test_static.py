"""R51 remains a read-only public-route diagnosis."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r51_python_files_parse_without_ellipsis() -> None:
    for relative in ("audit.py", "source_guard.py", "tests/test_static.py",
                     "tests/test_guard.py", "tests/test_public.py"):
        tree = ast.parse((PACKAGE / relative).read_text(encoding="utf-8"))
        assert not any(isinstance(item, ast.Constant) and item.value is Ellipsis
                       for item in ast.walk(tree))


def test_r51_does_not_install_math_or_replace_renderer() -> None:
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "search_group_from_registered_goal(" in audit
    assert "build_standard_web_group_proof_view(" in audit
    assert "inspect_integrated_root_frontier()" in audit
    assert "ProofStep(" not in audit
    assert "write_text(" not in audit.split("def main()")[0]
    assert "FULL_PYTEST=False" in script
    assert "pytest -q" in script
    for illegal in ("git reset", "git clean", "install.py", "patch.py"):
        assert illegal not in script


def test_r51_public_provider_is_not_replaced_by_curated_r50_provider() -> None:
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "shared_expansion_provider(screened, proof_target=goal)" in audit
    assert "bridge=original, context_sink=contexts.append" in audit
    assert "source_bound_missing" in audit
    assert "R50" in audit
