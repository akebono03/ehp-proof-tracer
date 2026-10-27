"""Conservative, reversible installation of one provider-function update."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = PACKAGE / "output"

OLD_ONE = '''        options.extend(expand_prior_cited_toda45_composite_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        ))'''
NEW_ONE = '''        legacy_one_step_options = expand_prior_cited_toda45_composite_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_one_step_options)'''
OLD_TWO = '''        options.extend(expand_prior_two_step_eta_square_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        ))'''
NEW_TWO = '''        legacy_two_step_options = expand_prior_two_step_eta_square_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_two_step_options)
        # R7 integration boundary: enable on the active 2-stem only.
        # The mathematical inference rule itself has no stem-specific branch.
        # Preserve the already verified R5B/R6A routes without ambiguity.
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and isinstance(goal, Relation)
                and isinstance(goal.lhs, TodaPrimaryGroup)
                and type(goal.lhs.group_dimension) is int
                and type(goal.lhs.sphere_dimension) is int
                and goal.lhs.group_dimension - goal.lhs.sphere_dimension == 2):
            options.extend(expand_prior_general_stable_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))'''


def _function_bounds(text: str) -> tuple[int, int]:
    tree = ast.parse(text)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one shared_expansion_provider function")
    node = matches[0]
    return node.lineno, node.end_lineno


def replacement_content(data: bytes) -> tuple[bytes, str]:
    original = data.decode("utf-8-sig")
    normalized = original.replace("\r\n", "\n")
    if normalized.count(OLD_ONE) != 1 or normalized.count(OLD_TWO) != 1:
        raise RuntimeError("reviewed R5B/R6A provider anchors are missing or duplicated")
    if "phase169_r7_general_stable_transport" in normalized:
        raise RuntimeError("R7 provider is already connected")
    _function_bounds(normalized)
    updated = normalized.replace(OLD_ONE, NEW_ONE, 1).replace(OLD_TWO, NEW_TWO, 1)
    ast.parse(updated)
    after = _function_bounds(updated)
    lines = updated.splitlines(keepends=True)
    function = "".join(lines[after[0] - 1:after[1]])
    if normalized.endswith("\n") and not updated.endswith("\n"):
        raise RuntimeError("patch changed the file's trailing newline")
    if b"\r\n" in data:
        updated = updated.replace("\n", "\r\n")
    if data.startswith(b"\xef\xbb\xbf"):
        return b"\xef\xbb\xbf" + updated.encode("utf-8"), function
    return updated.encode("utf-8"), function


def _git(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT,
                               check=True, capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
    return completed.stdout.strip()


def install() -> None:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("R7 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    if not TARGET.is_file():
        raise RuntimeError("the existing shared provider is missing")
    source = TARGET.read_bytes()
    updated, function = replacement_content(source)
    OUTPUT.mkdir(exist_ok=True)
    previous = OUTPUT / "phase165_r52_r9_shared_math.py.before"
    if previous.exists():
        raise RuntimeError("backup already exists: use a clean R7 package to prevent overwrite")
    previous.write_bytes(source)
    try:
        TARGET.write_bytes(updated)
        (OUTPUT / "shared_expansion_provider_FULL.py").write_text(function, encoding="utf-8")
        (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(updated)
        (OUTPUT / "patch_manifest.json").write_text(json.dumps({
            "head_at_patch": head,
            "branch": "develop",
            "target": str(TARGET),
            "before_sha256": hashlib.sha256(source).hexdigest(),
            "after_sha256": hashlib.sha256(updated).hexdigest(),
            "changed_production_functions": ["shared_expansion_provider"],
            "changed_production_files": ["phase165_r52_r9_shared_math.py"],
            "top_level_imports_changed": False,
            "local_import_added_inside_function": True,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except BaseException:
        TARGET.write_bytes(source)
        raise
    print("R7_PATCHED=" + str(TARGET))
    print("R7_BACKUP=" + str(previous))
    print("R7_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"))
    print("R7_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    install()
