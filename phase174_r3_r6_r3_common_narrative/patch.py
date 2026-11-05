"""Guarded textual installation of minimal shared-renderer changes.

This file intentionally fetches no network resources and overwrites no source
whose normalized Git blob differs from the reviewed GitHub develop baseline.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
REVIEWED_BLOBS = {
    "phase168_r3_27_typed_statement_projection.py": "57d0fb8cb713e91b0743f746bc8d59cea648868e",
    "phase168_r3_5_model_renderer.py": "03aca2e461e7e6a10a834a650e66270c072baf57",
}


def git_blob(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(
        b"blob " + str(len(normalized)).encode("ascii") + b"\x00" + normalized
    ).hexdigest()


def replace_once(text: str, old: str, new: str, *, where: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{where}: expected exactly one verified insertion anchor, got {count}")
    return text.replace(old, new, 1)


def transform_typed(text: str) -> str:
    anchor = "def typed_sentence(statement, step):\n    map_sentence = map_property_sentence(statement, step)\n"
    replacement = (
        "def typed_sentence(statement, step):\n"
        "    from phase174_r3_r6_r3_common_narrative.projection import (\n"
        "        project_verified_index_two_statement,\n"
        "    )\n"
        "    index_two = project_verified_index_two_statement(statement, step)\n"
        "    if index_two is not None:\n"
        "        return index_two\n"
        "    map_sentence = map_property_sentence(statement, step)\n"
    )
    return replace_once(text, anchor, replacement, where="typed_sentence")


def transform_renderer(text: str) -> str:
    before_reference = (
        "        if not incomplete:\n"
        "            displayed = display_prior_reference_locator(citation, model)\n"
        "            if displayed is not None:\n"
        "                locator = displayed\n"
        "        lines.append(f\"**[R{citation.number}] {locator}.**\")\n"
    )
    after_reference = (
        "        if not incomplete:\n"
        "            displayed = display_prior_reference_locator(citation, model)\n"
        "            if displayed is not None:\n"
        "                locator = displayed\n"
        "            from phase174_r3_r6_r3_common_narrative.projection import (\n"
        "                display_cited_nu_family_locator,\n"
        "            )\n"
        "            family_locator = display_cited_nu_family_locator(citation, model)\n"
        "            if family_locator is not None:\n"
        "                locator = family_locator\n"
        "        lines.append(f\"**[R{citation.number}] {locator}.**\")\n"
    )
    text = replace_once(text, before_reference, after_reference, where="reference heading")
    before_body = (
        "        body_line = body_by_step.get(index)\n"
        "        sentence = typed_sentence(step.conclusion, step)\n"
        "        if sentence is not None:\n"
    )
    after_body = (
        "        body_line = body_by_step.get(index)\n"
        "        sentence = typed_sentence(step.conclusion, step)\n"
        "        if index != model.root_index:\n"
        "            from phase174_r3_r6_r3_common_narrative.projection import (\n"
        "                project_verified_cyclic_extension_reason,\n"
        "            )\n"
        "            extension_reason = project_verified_cyclic_extension_reason(\n"
        "                step.conclusion, step,\n"
        "            )\n"
        "            if extension_reason is not None:\n"
        "                sentence = extension_reason\n"
        "        if sentence is not None:\n"
    )
    return replace_once(text, before_body, after_body, where="verified cyclic extension body")


def extract_full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError(f"function {name} missing or ambiguous")
    lines = source.splitlines(keepends=True)
    node = matches[0]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def reviewed_changes() -> dict[str, tuple[bytes, str]]:
    transforms = {
        "phase168_r3_27_typed_statement_projection.py": transform_typed,
        "phase168_r3_5_model_renderer.py": transform_renderer,
    }
    staged: dict[str, tuple[bytes, str]] = {}
    for path, expected_sha in REVIEWED_BLOBS.items():
        target = ROOT / path
        if not target.is_file():
            raise FileNotFoundError(f"missing reviewed target: {target}")
        original = target.read_bytes()
        actual = git_blob(original)
        if actual != expected_sha:
            raise ValueError(
                f"unreviewed changes to {path}: expected {expected_sha}, observed {actual}. "
                "Refusing to overwrite the local working tree."
            )
        original_text = original.replace(b"\r\n", b"\n").decode("utf-8-sig")
        updated = transforms[path](original_text)
        ast.parse(updated, filename=path)
        staged[path] = (original, updated)
    return staged


def generate_full_outputs(changes: dict[str, tuple[bytes, str]]) -> None:
    directory = PACKAGE / "output"
    directory.mkdir(exist_ok=True)
    typed = changes["phase168_r3_27_typed_statement_projection.py"][1]
    rendered = changes["phase168_r3_5_model_renderer.py"][1]
    names = (
        ("typed_sentence_FULL.py", extract_full_function(typed, "typed_sentence")),
        ("render_model_backed_narrative_markdown_FULL.py", extract_full_function(
            rendered, "render_model_backed_narrative_markdown"
        )),
    )
    for name, code in names:
        (directory / name).write_text(code.rstrip() + "\n", encoding="utf-8", newline="\n")
    specification = [
        "# Phase 174 R3-R6-R3 変更後の完全コード", "",
        "変更対象：`phase168_r3_27_typed_statement_projection.py` の `typed_sentence()`、",
        "`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()`。",
        "両者とも import 部分は変更しない。新規関数は `projection.py` 内に全文収録。", "",
    ]
    for filename, source in names:
        specification.extend((f"## {filename}", "", "```python", source.rstrip(), "```", ""))
    specification.extend(("## 新規 projection.py（全文）", "", "```python",
                          (PACKAGE / "projection.py").read_text(encoding="utf-8").rstrip(),
                          "```", ""))
    (directory / "CODE_FULL_JA.md").write_text(
        "\n".join(specification), encoding="utf-8", newline="\n"
    )


def write_atomically(target: Path, content: str) -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=target.parent,
        prefix=target.name + ".", suffix=".tmp", delete=False,
    )
    tmp = Path(handle.name)
    try:
        with handle:
            handle.write(content)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    changes = reviewed_changes()
    generate_full_outputs(changes)
    print("PHASE174_R3R6R3_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R3_TARGET_FILES=" + str(len(changes)))
    print("PHASE174_R3R6R3_FULL_FUNCTION_FILES=2")
    if arguments.dry_run:
        print("PHASE174_R3R6R3_DRY_RUN=PASS")
        return 0
    applied: list[tuple[Path, bytes]] = []
    try:
        for path, (original, updated) in changes.items():
            target = ROOT / path
            write_atomically(target, updated)
            applied.append((target, original))
    except Exception:
        for target, original in reversed(applied):
            target.write_bytes(original)
        raise
    print("PHASE174_R3R6R3_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
