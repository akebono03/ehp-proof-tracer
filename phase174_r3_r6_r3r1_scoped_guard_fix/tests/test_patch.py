"""Verify that a local edit is never silently replaced by the installer."""
from __future__ import annotations

import subprocess

import pytest

from phase174_r3_r6_r3_common_narrative.patch import (
    transform_renderer,
    transform_typed,
)
from phase174_r3_r6_r3r1_scoped_guard_fix.patch import (
    git_blob_sha,
    inspect_scoped_change,
    normalize_text,
)

TYPED = (
    "from __future__ import annotations\n"
    "import math\n"
    "\n"
    "def unrelated_helper():\n"
    "    return 1\n"
    "\n"
    "def typed_sentence(statement, step):\n"
    "    map_sentence = map_property_sentence(statement, step)\n"
    "    return map_sentence\n"
)

RENDERER = (
    "from __future__ import annotations\n"
    "import math\n"
    "\n"
    "def unrelated_helper():\n"
    "    return 1\n"
    "\n"
    "def render_model_backed_narrative_markdown(result, model):\n"
    "    for citation in model.citations:\n"
    "        if not incomplete:\n"
    "            displayed = display_prior_reference_locator(citation, model)\n"
    "            if displayed is not None:\n"
    "                locator = displayed\n"
    "        lines.append(f\"**[R{citation.number}] {locator}.**\")\n"
    "        body_line = body_by_step.get(index)\n"
    "        sentence = typed_sentence(step.conclusion, step)\n"
    "        if sentence is not None:\n"
    "            pass\n"
)


def _repo(tmp_path, path: str, baseline: str):
    subprocess.run(("git", "init", "-q"), cwd=tmp_path, check=True)
    subprocess.run(("git", "config", "user.name", "Test"), cwd=tmp_path, check=True)
    subprocess.run(("git", "config", "user.email", "test@example.invalid"), cwd=tmp_path, check=True)
    target = tmp_path / path
    target.write_text(baseline, encoding="utf-8", newline="\n")
    subprocess.run(("git", "add", path), cwd=tmp_path, check=True)
    subprocess.run(("git", "commit", "-qm", "reviewed baseline"), cwd=tmp_path, check=True)
    return target, git_blob_sha(baseline.encode("utf-8"))


def test_preserves_unrelated_local_semantic_edits_and_crlf(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    modified = TYPED.replace("return 1", "return 17").replace("\n", "\r\n")
    target.write_bytes(modified.encode("utf-8"))
    change = inspect_scoped_change(
        tmp_path, path, "typed_sentence", transform_typed, blob,
    )
    assert change.unrelated_worktree_difference
    assert b"    return 17\r\n" in change.updated
    assert b"    return 1\r\n" not in change.updated
    assert b"    return 17\r\n" in change.original
    assert b"project_verified_index_two_statement" in change.updated
    assert change.updated.count(b"\r\n") == change.updated.count(b"\n")
    assert target.read_bytes() == change.original  # even DryRun never writes


def test_preserves_mixed_newlines_and_bom_without_normalizing_unrelated_lines(tmp_path) -> None:
    path = "phase168_r3_5_model_renderer.py"
    target, blob = _repo(tmp_path, path, RENDERER)
    raw = "\ufeff" + RENDERER.replace("return 1\n", "return 20\r\n")
    target.write_bytes(raw.encode("utf-8"))
    change = inspect_scoped_change(
        tmp_path, path, "render_model_backed_narrative_markdown", transform_renderer, blob,
    )
    assert change.updated.startswith(b"\xef\xbb\xbf")
    assert b"return 20\r\n" in change.updated
    assert b"display_cited_nu_family_locator" in change.updated
    assert b"project_verified_cyclic_extension_reason" in change.updated
    assert normalize_text(change.updated) == transform_renderer(normalize_text(change.original))


def test_rejects_locally_modified_target_function(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    modified = TYPED.replace("return map_sentence", "return None")
    target.write_text(modified, encoding="utf-8")
    with pytest.raises(ValueError, match="inside typed_sentence"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, blob)
    assert target.read_text(encoding="utf-8") == modified


def test_rejects_unreviewed_import_changes(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    target.write_text(TYPED.replace("import math", "import cmath"), encoding="utf-8")
    with pytest.raises(ValueError, match="import changes"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, blob)


def test_rejects_unknown_reviewed_git_blob(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, _ = _repo(tmp_path, path, TYPED)
    with pytest.raises(ValueError, match="Unreviewed Git HEAD blob"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, "0" * 40)
    assert target.read_text(encoding="utf-8") == TYPED
