# Phase 171 R20R13R4 — テストのみ修正

変更対象：`phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py`。

変更関数：`test_orphan_blank_lines_do_not_break_three_verified_eta_equations`（全文）。

import の変更はない。変更後の import 全文：

```python
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    combine_adjacent_verified_eta_sentences,
    verified_eta_display_sentences,
)
```

## 変更したテスト関数全文

```python
def test_orphan_blank_lines_do_not_break_three_verified_eta_equations(eligible):
    a, b, c = tuple(eligible)
    lines = ["証明", "", a, "", "", "", b, "", c, "", "□"]
    actual = combine_adjacent_verified_eta_sentences(lines, SimpleNamespace())
    merged = r"[R3]より, $E(\eta_{2})=\eta_{3},\quad E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}$."
    assert merged in actual
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1
    assert a not in actual and b not in actual and c not in actual
    assert actual[-1] == "□"
```

## 置換後のテストファイル全文

```python
"""Focused separator-only fix; real proof still verifies via R20R13 audit."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    combine_adjacent_verified_eta_sentences,
    verified_eta_display_sentences,
)


@pytest.fixture
def eligible(monkeypatch):
    values = {
        r"[R3]より, $E(\eta_{2})=\eta_{3}$.":
            ("[R3]より, ", r"E(\eta_{2})=\eta_{3}"),
        r"[R3]より, $E(\eta_{3}^{2})=\eta_{4}^{2}$.":
            ("[R3]より, ", r"E(\eta_{3}^{2})=\eta_{4}^{2}"),
        r"[R3]より, $E(\eta_{2}^{3})=\eta_{3}^{3}$.":
            ("[R3]より, ", r"E(\eta_{2}^{3})=\eta_{3}^{3}"),
    }
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: values,
    )
    return values


def test_orphan_blank_lines_do_not_break_three_verified_eta_equations(eligible):
    a, b, c = tuple(eligible)
    lines = ["証明", "", a, "", "", "", b, "", c, "", "□"]
    actual = combine_adjacent_verified_eta_sentences(lines, SimpleNamespace())
    merged = r"[R3]より, $E(\eta_{2})=\eta_{3},\quad E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}$."
    assert merged in actual
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1
    assert a not in actual and b not in actual and c not in actual
    assert actual[-1] == "□"


def test_no_merge_across_other_proof_sentence(eligible):
    a, b, c = tuple(eligible)
    barrier = r"[R5]より, $2\nu'=\eta_{3}^{3}$."
    original = [a, "", "", barrier, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert barrier in actual
    assert not any(r"E(\eta_{2})=\eta_{3},\quad" in s for s in actual)
    assert any(r"E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}" in s for s in actual)


def test_no_merge_across_different_citation(eligible, monkeypatch):
    a, b, c = tuple(eligible)
    other_line = "[R4]より, $" + eligible[b][1] + "$."
    differing = dict(eligible)
    differing[other_line] = ("[R4]より, ", eligible[b][1])
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: differing,
    )
    original = [a, "", "", other_line, "", "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert actual == original


def test_uncertified_lines_stay_unchanged(eligible):
    a, b, c = tuple(eligible)
    unknown = r"[R3]より, $E(\kappa)=\lambda$."
    original = [a, "", "", unknown, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert unknown in actual


def test_complete_real_pi63_three_eta_equations_in_one_line():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    lines = body.splitlines()
    grouped = [line for line in lines
               if line.startswith("[R3]より, $E(") and r",\quad E(" in line]
    assert any(
        all(eta in line for eta in (
            r"E(\eta_{2})=\eta_{3}",
            r"E(\eta_{3}^{2})=\eta_{4}^{2}",
            r"E(\eta_{2}^{3})=\eta_{3}^{3}",
        )) for line in grouped
    )
    assert r"\operatorname{ord}" in body
    assert r"\neq0" in body
    assert "短完全列となる. 両端" not in body
    assert len(model.citations) == 8
    assert "[R3] Chapter V, i)." in reference

```

## 新規インストーラ全文

```python
"""Phase 171 R20R13R4: guarded test-only fix for list.count assertion.

No production code or mathematical inference is modified. The existing
R20R13R2/R3 workflow is rerun after repairing the single faulty assertion.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = Path("phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py")
PROJECTION = Path("phase171_r20r13_eta_sentence_layout/projection.py")
RENDERER = Path("phase168_r3_5_model_renderer.py")
ORIGINAL_SHA256 = "40cab7a2e70ccc1dec44b97a15c7706ffaa83e23cb22e0a75f93568a99e7be60"
CORRECTED_SHA256 = "319f9be268c49264a799d45f841ae0fd2a153399ff27dd7c4eafdd795660dbfe"
PROJECTION_SHA256 = "701c1ec9de253a8f0df68bae1ac711b449a4516ab6d03d6132be7ab84615d006"
OLD = '    assert actual.count("[R3]より, ") == 1\n'
NEW = '    assert sum(line.startswith("[R3]より, ") for line in actual) == 1\n'


def normalized(raw: bytes) -> str:
    return raw.decode("utf-8-sig").replace("\r\n", "\n")


def sha256(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def preflight() -> tuple[str, bytes, bytes, bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R13R4 requires the develop branch")
    head = git("rev-parse", "HEAD")
    path = ROOT / TARGET
    projection = ROOT / PROJECTION
    renderer = ROOT / RENDERER
    if not path.is_file() or not projection.is_file() or not renderer.is_file():
        raise RuntimeError("R20R13R2/R3 test, projection, or renderer is missing")
    if sha256(normalized(projection.read_bytes())) != PROJECTION_SHA256:
        raise RuntimeError("R20R13R2 projection is not the reviewed corrected content")
    if "format_complete_proof_sentences(lines, model)" not in renderer.read_text(encoding="utf-8-sig"):
        raise RuntimeError("R20R13 renderer hook is missing")
    source = path.read_bytes()
    plain = normalized(source)
    digest = sha256(plain)
    if digest == CORRECTED_SHA256:
        return head, source, source, True
    if digest != ORIGINAL_SHA256 or plain.count(OLD) != 1:
        raise RuntimeError("test source differs from reviewed R20R13R2; no overwrite")
    corrected = plain.replace(OLD, NEW, 1)
    if sha256(corrected) != CORRECTED_SHA256:
        raise RuntimeError("corrected test hash mismatch")
    bom = b"\xef\xbb\xbf" if source.startswith(b"\xef\xbb\xbf") else b""
    eol = "\r\n" if b"\r\n" in source else "\n"
    updated = bom + corrected.replace("\n", eol).encode("utf-8")
    return head, source, updated, False


def changed_test_function(source: str) -> str:
    import ast
    tree = ast.parse(source)
    candidates = [
        item for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and item.name == "test_orphan_blank_lines_do_not_break_three_verified_eta_equations"
    ]
    if len(candidates) != 1:
        raise RuntimeError("expected exactly one corrected test function")
    node = candidates[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def output_documentation(source: bytes) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    content = normalized(source)
    lines = [
        "# Phase 171 R20R13R4 — テストのみ修正\n\n",
        "変更対象：`phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py`。\n\n",
        "変更関数：`test_orphan_blank_lines_do_not_break_three_verified_eta_equations`（全文）。\n\n",
        "import の変更はない。変更後の import 全文：\n\n",
        "```python\n",
        "from __future__ import annotations\n\n",
        "from types import SimpleNamespace\n\n",
        "import pytest\n\n",
        "from phase171_r20r13_eta_sentence_layout.projection import (\n",
        "    combine_adjacent_verified_eta_sentences,\n",
        "    verified_eta_display_sentences,\n",
        ")\n",
        "```\n\n",
        "## 変更したテスト関数全文\n\n```python\n",
        changed_test_function(content), "```\n\n",
        "## 置換後のテストファイル全文\n\n```python\n",
        content, "\n```\n\n",
        "## 新規インストーラ全文\n\n```python\n",
        (HERE / "install.py").read_text(encoding="utf-8"), "\n```\n\n",
        "## 新規テスト全文\n\n```python\n",
        (HERE / "tests/test_install.py").read_text(encoding="utf-8"), "\n```\n",
    ]
    (OUTPUT / "CODE_FULL_JA.md").write_text("".join(lines), encoding="utf-8")
    (OUTPUT / "test_correction.py.FULL").write_bytes(source)


def run(*, dry_run: bool = False) -> None:
    head, before, after, already = preflight()
    print("PHASE171_R20R13R4_BRANCH=develop", flush=True)
    print("PHASE171_R20R13R4_HEAD=" + head, flush=True)
    print("PHASE171_R20R13R4_PROJECTION_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R13R4_TEST_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R13R4_ALREADY_INSTALLED=" + str(already), flush=True)
    if dry_run:
        print("PHASE171_R20R13R4_DRY_RUN=PASS", flush=True)
        return
    if not already:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / "test_correction.py.before_r4").write_bytes(before)
        (ROOT / TARGET).write_bytes(after)
        print("PHASE171_R20R13R4_PATCHED=" + TARGET.as_posix(), flush=True)
    output_documentation(after)
    print("PHASE171_R20R13R4_PRODUCTION_MODIFIED=False", flush=True)
    print("PHASE171_R20R13R4_RESULT=PASS_TEST_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

```

## 新規テスト全文

```python
"""Guarded repair checks: a list contains lines, not substrings."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase171_r20r13r4_test_count_fix import install


def test_exact_reviewed_single_assertion_replacement():
    source = install.normalized(
        (install.HERE / "reviewed_test.py").read_bytes()
    )
    assert install.sha256(source) in (
        install.ORIGINAL_SHA256, install.CORRECTED_SHA256,
    )
    fixed = source.replace(install.OLD, install.NEW)
    assert install.sha256(fixed) == install.CORRECTED_SHA256
    assert "sum(line.startswith" in fixed
    assert "actual.count(" not in fixed


def test_count_validates_prefixed_lines_not_a_separate_list_member():
    actual = ["証明", "", r"[R3]より, $E(\\eta_{2})=\\eta_{3},\\quad E(\\eta_{3}^{2})=\\eta_{4}^{2}$.", "□"]
    assert actual.count("[R3]より, ") == 0
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1


def test_unknown_test_content_is_rejected(monkeypatch, tmp_path):
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unreviewed test")
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("untrusted projection", encoding="utf-8")
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("untrusted projection"))
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "any-head")
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        install.preflight()
    assert target.read_bytes() == b"unreviewed test"


def test_reviewed_original_test_can_be_patched(monkeypatch, tmp_path):
    reviewed = (install.HERE / "reviewed_test.py").read_bytes()
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(reviewed)
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("reviewed synthetic projection", encoding="utf-8")
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("reviewed synthetic projection"))
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "new HEAD")
    head, before, after, already = install.preflight()
    assert head == "new HEAD"
    assert before == reviewed
    assert already is False
    assert install.sha256(install.normalized(after)) == install.CORRECTED_SHA256
    assert target.read_bytes() == reviewed


def test_corrected_test_is_idempotent(monkeypatch, tmp_path):
    reviewed = (install.HERE / "reviewed_test.py").read_text(encoding="utf-8")
    corrected = reviewed.replace(install.OLD, install.NEW, 1).encode("utf-8")
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(corrected)
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("reviewed synthetic projection", encoding="utf-8")
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("reviewed synthetic projection"))
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "new HEAD")
    head, before, after, already = install.preflight()
    assert already is True
    assert before == after == corrected

```
