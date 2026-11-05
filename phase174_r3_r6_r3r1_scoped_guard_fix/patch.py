"""Source-reviewed, function-scoped installer for the preceding R3-R6-R3 patch.

This repair writes only inserted lines into two previously reviewed functions.
Other local text (including mixed Windows newlines) is preserved byte for byte.
Unreviewed changes *inside* either target function or its imports fail closed.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from difflib import SequenceMatcher, unified_diff
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r6_r3_common_narrative import patch as previous

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
REVIEWED_HEAD = "ecbb2fea225c5b88000629d9c025934fcc2d7075"
TARGETS = (
    ("phase168_r3_27_typed_statement_projection.py", "typed_sentence", previous.transform_typed),
    ("phase168_r3_5_model_renderer.py", "render_model_backed_narrative_markdown", previous.transform_renderer),
)


@dataclass(frozen=True)
class ScopedChange:
    path: str
    original: bytes
    updated: bytes
    original_normalized: str
    updated_normalized: str
    unrelated_worktree_difference: bool


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def git_head_file(root: Path, path: str) -> bytes:
    result = subprocess.run(
        ("git", "show", "HEAD:" + path),
        cwd=root, capture_output=True, check=True,
    )
    return result.stdout


def normalize_text(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def statement_ast(text: str, function_name: str) -> tuple[str, tuple[str, ...]]:
    tree = ast.parse(text)
    matches = tuple(
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    )
    if len(matches) != 1:
        raise ValueError("Reviewed function missing or ambiguous: " + function_name)
    import_asts = tuple(
        ast.dump(node, include_attributes=False)
        for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
    )
    return ast.dump(matches[0], include_attributes=False), import_asts


def preserve_original_lines(original: bytes, old_text: str, updated_text: str) -> bytes:
    """Insert only new lines; never rewrite a pre-existing line or its ending."""
    had_bom = original.startswith(b"\xef\xbb\xbf")
    raw_text = original.decode("utf-8-sig")
    raw_lines = raw_text.splitlines(keepends=True)
    old_lines = old_text.splitlines(keepends=True)
    updated_lines = updated_text.splitlines(keepends=True)
    if len(raw_lines) != len(old_lines):
        raise ValueError("Raw and normalized line counts disagree; refusing rewrite")
    if any(normalize_text(line.encode("utf-8")) != normalized
           for line, normalized in zip(raw_lines, old_lines)):
        raise ValueError("Original bytes do not map to normalized source lines")
    opcodes = SequenceMatcher(
        a=old_lines, b=updated_lines, autojunk=False,
    ).get_opcodes()
    if not any(tag == "insert" for tag, _, _, _, _ in opcodes):
        raise ValueError("Expected at least one guarded insertion")
    if any(tag not in ("equal", "insert") for tag, _, _, _, _ in opcodes):
        raise ValueError("Installer attempted to replace or delete existing source")

    out: list[str] = []
    for tag, a, b, c, d in opcodes:
        if tag == "equal":
            out.extend(raw_lines[a:b])
        else:
            neighbor = raw_lines[a - 1] if a else raw_lines[0]
            ending = "\r\n" if neighbor.endswith("\r\n") else (
                "\r" if neighbor.endswith("\r") else "\n"
            )
            additions = updated_lines[c:d]
            for added in additions:
                if not added.endswith("\n"):
                    raise ValueError("Added line is missing a newline")
                out.append(added[:-1] + ending)
    modified = ("\ufeff" if had_bom else "") + "".join(out)
    result = modified.encode("utf-8")
    if normalize_text(result) != updated_text:
        raise ValueError("Applied code differs from the reviewed transformation")
    return result


def inspect_scoped_change(
    root: Path, path: str, function_name: str, transform,
    reviewed_blob_sha: str,
) -> ScopedChange:
    baseline = git_head_file(root, path)
    observed_head = git_blob_sha(baseline)
    if observed_head != reviewed_blob_sha:
        raise ValueError(
            f"Unreviewed Git HEAD blob for {path}: "
            f"expected {reviewed_blob_sha}, observed {observed_head}"
        )
    original = (root / path).read_bytes()
    baseline_text = normalize_text(baseline)
    local_text = normalize_text(original)
    baseline_function, baseline_imports = statement_ast(baseline_text, function_name)
    local_function, local_imports = statement_ast(local_text, function_name)
    if baseline_imports != local_imports:
        raise ValueError(
            f"Unreviewed import changes in {path}; source must be reviewed first"
        )
    if baseline_function != local_function:
        raise ValueError(
            f"Unreviewed changes inside {function_name} in {path}; "
            "source must be reviewed first"
        )
    expected_updated = transform(baseline_text)
    actual_updated = transform(local_text)
    if statement_ast(expected_updated, function_name)[0] != statement_ast(
        actual_updated, function_name
    )[0]:
        raise ValueError("Transformed function differs from reviewed target")
    updated = preserve_original_lines(original, local_text, actual_updated)
    return ScopedChange(
        path=path, original=original, updated=updated,
        original_normalized=local_text, updated_normalized=actual_updated,
        unrelated_worktree_difference=baseline_text != local_text,
    )


def reviewed_changes(root: Path = ROOT) -> tuple[ScopedChange, ...]:
    changes = []
    for path, function, transform in TARGETS:
        changes.append(inspect_scoped_change(
            root, path, function, transform, previous.REVIEWED_BLOBS[path],
        ))
    return tuple(changes)


def write_atomically(path: Path, data: bytes) -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="wb", dir=path.parent, prefix=path.name + ".",
        suffix=".tmp", delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_outputs(changes: tuple[ScopedChange, ...]) -> None:
    output = PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    previous.generate_full_outputs({
        change.path: (change.original, change.updated_normalized)
        for change in changes
    })
    names = (
        ("typed_sentence_FULL.py", "typed_sentence"),
        ("render_model_backed_narrative_markdown_FULL.py", "render_model_backed_narrative_markdown"),
    )
    text = ["# Phase 174 R3-R6-R3R1 置換可能な完全コード", "",
            "既存 import に変更はありません。新規クラス・関数は本 ZIP の `patch.py` に全文収録しています。", ""]
    for change, (filename, function) in zip(changes, names):
        function_source = previous.extract_full_function(change.updated_normalized, function)
        (output / filename).write_text(function_source.rstrip() + "\n", encoding="utf-8")
        text.extend(("## " + change.path + " — " + function, "", "```python",
                     function_source.rstrip(), "```", ""))
    (output / "CODE_FULL_JA.md").write_text("\n".join(text), encoding="utf-8")
    report = {
        "reviewed_head": REVIEWED_HEAD,
        "guard": "complete target-function and import AST match HEAD; unrelated bytes preserved",
        "changes": [{
            "path": change.path,
            "local_differs_from_HEAD": change.unrelated_worktree_difference,
            "before_sha256": hashlib.sha256(change.original).hexdigest(),
            "after_sha256": hashlib.sha256(change.updated).hexdigest(),
            "only_inserted_lines": True,
        } for change in changes],
        "full_pytest_performed": False,
    }
    (output / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    flags = parser.add_mutually_exclusive_group(required=True)
    flags.add_argument("--dry-run", action="store_true")
    flags.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    changes = reviewed_changes()
    write_outputs(changes)
    print("PHASE174_R3R6R3R1_SCOPED_SOURCE_GUARD=PASS")
    for change in changes:
        print("PHASE174_R3R6R3R1_LOCAL_DIFFERENCE_" +
              Path(change.path).stem + "=" + str(change.unrelated_worktree_difference))
    print("PHASE174_R3R6R3R1_TARGET_FILES=" + str(len(changes)))
    if args.dry_run:
        print("PHASE174_R3R6R3R1_DRY_RUN=PASS")
        return 0
    applied: list[ScopedChange] = []
    try:
        for change in changes:
            write_atomically(ROOT / change.path, change.updated)
            applied.append(change)
    except Exception:
        for change in reversed(applied):
            write_atomically(ROOT / change.path, change.original)
        raise
    print("PHASE174_R3R6R3R1_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
