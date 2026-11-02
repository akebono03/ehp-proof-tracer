"""Offline-safe, narrow installer guards."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r1_narrative_source_fix.install import (
    ANCHOR, HOOK, transform,
)


def representative_adapter() -> str:
    return (
        "def build_partial_web_group_proof_view():\n"
        "    if True:\n"
        "        if True:\n"
        "            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n"
        "    return markdown\n"
    )


def test_injects_only_after_verified_renderer() -> None:
    proposed = transform(representative_adapter())
    assert proposed.count(HOOK) == 1
    assert proposed.count(ANCHOR) == 1
    assert "if (n == 4 and k == 3" in proposed
    ast.parse(proposed)


def test_repeated_injection_rejected() -> None:
    with pytest.raises(RuntimeError, match="already exists"):
        transform(transform(representative_adapter()))


def test_missing_anchor_rejected() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform(representative_adapter().replace(ANCHOR, "            markdown = 'x'\n"))


def test_duplicate_anchor_rejected() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform(representative_adapter().replace(ANCHOR, ANCHOR + ANCHOR))


def test_hook_confined_to_narrative_model() -> None:
    proposed = transform(representative_adapter())
    assert proposed.index(ANCHOR) < proposed.index(HOOK)
    assert 'mode == "narrative"' in HOOK
    assert "ProofSearchStatus.COMPLETE" in HOOK


def test_existing_imports_remain_untouched() -> None:
    source = "from __future__ import annotations\nimport math\n\n" + representative_adapter()
    proposed = transform(source)
    assert proposed.startswith("from __future__ import annotations\nimport math\n\n")


def test_selected_production_function_unchanged_except_hook() -> None:
    contents = Path(__file__).resolve().parents[2] / "phase165_r52_r3_web_adapter.py"
    if not contents.exists():
        pytest.skip("Run in repository root for live source guard")
    source = contents.read_text(encoding="utf-8")
    if HOOK not in source:
        assert source.count(ANCHOR) == 1
        patched = transform(source)
        assert patched.count(HOOK) == 1
        assert patched.replace(HOOK, "", 1) == source
        return
    assert source.count(HOOK) == 1
    original = source.replace(HOOK, "", 1)
    assert original.count(ANCHOR) == 1
    assert transform(original) == source


def committed_public_fixture(tmp_path, monkeypatch):
    """A committed public hook with exact original blob and reviewed dependencies."""
    from hashlib import sha1

    from phase173_r4_r1_public_connection.install import (
        EXPECTED_DEPENDENCIES, HOOK as PUBLIC_HOOK,
        REVIEWED_DIAGONAL_HEADS,
    )
    from phase173_r4_r1_narrative_source_fix import install as installer

    original = b"def reviewed():\r\n    return 1\r\n"
    committed = original + PUBLIC_HOOK.replace("\n", "\r\n").encode("utf-8")
    def blob(data):
        return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()

    monkeypatch.setattr(installer, "EXPECTED_PUBLIC_BASE", blob(original))
    monkeypatch.setattr(installer, "EXPECTED_PUBLIC_COMMITTED", blob(committed))
    monkeypatch.setattr(installer, "EXPECTED_PUBLIC_INSTALLER", "reviewed-installer")

    file_bytes = {installer.PUBLIC_TARGET: committed}
    hashes = {installer.PUBLIC_TARGET: blob(committed)}
    for path, expected in EXPECTED_DEPENDENCIES.items():
        file_bytes[path] = b"verified dependency\n"
        hashes[path] = expected
    file_bytes[installer.PUBLIC_INSTALLER] = b"reviewed public installer\n"
    hashes[installer.PUBLIC_INSTALLER] = "reviewed-installer"
    file_bytes[installer.PUBLIC_ROUTE] = b"reviewed route\n"
    hashes[installer.PUBLIC_ROUTE] = installer.EXPECTED_PUBLIC_ROUTE
    diagonal = "phase173_r4_r1_source_bound_56/rule.py"
    file_bytes[diagonal] = b"SourceBoundGoal(diagonal, diagonal_source)\n"
    hashes[diagonal] = REVIEWED_DIAGONAL_HEADS[0]

    for path, value in file_bytes.items():
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(value)

    def fake_git(_root, *args):
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return hashes[args[1][5:]]
        raise AssertionError("Unexpected Git request: " + repr(args))

    monkeypatch.setattr(installer, "git", fake_git)
    monkeypatch.setattr(installer, "git_bytes", lambda _root, path: file_bytes[path])
    return installer, file_bytes


def test_reviewed_committed_public_connection_is_accepted(tmp_path, monkeypatch) -> None:
    installer, _ = committed_public_fixture(tmp_path, monkeypatch)
    assert installer.reviewed_public_state(tmp_path) == "COMMITTED_INSTALLED"


def test_reviewed_committed_public_connection_rejects_worktree_edit(tmp_path, monkeypatch) -> None:
    installer, _ = committed_public_fixture(tmp_path, monkeypatch)
    path = tmp_path / installer.PUBLIC_TARGET
    path.write_bytes(path.read_bytes() + b"# unexpected edit\n")
    with pytest.raises(RuntimeError, match="missing or modified"):
        installer.reviewed_public_state(tmp_path)


def test_reviewed_committed_public_connection_rejects_dependency_edit(tmp_path, monkeypatch) -> None:
    installer, files = committed_public_fixture(tmp_path, monkeypatch)
    path = next(p for p in files if p.endswith("lemma54_source_bridge/source.py"))
    (tmp_path / path).write_bytes(b"modified dependency\n")
    with pytest.raises(RuntimeError, match="dependency worktree changed"):
        installer.reviewed_public_state(tmp_path)
