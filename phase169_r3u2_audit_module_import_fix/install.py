"""Guarded R3U2 installation: one production function plus four existing test functions."""
from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
PRODUCTION = Path("phase165_r14_r5_ehp_connection.py")
TEST_FILES = (
    Path("phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py"),
    Path("phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py"),
    Path("phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py"),
)
R3I_FUNCTIONS = (
    "test_r3i_only_exact_screened_claims_propose_cited_rules",
    "test_r3i_derived_terminal_steps_have_exact_cited_ancestors",
    "test_r3i_historical_inference_only_rules_remain_intact",
    "test_r3i_real_recursive_proof_of_terminal_goals",
)
REPLACEMENTS = {
    PRODUCTION: {"expand_cited_ehp_terminal_goal": PACKAGE / "full_functions/expand_cited_ehp_terminal_goal_FULL.py"},
    **{
        path: {name: PACKAGE / "full_functions" / (name + "_FULL.py") for name in R3I_FUNCTIONS}
        for path in TEST_FILES
    },
}


def function_span(code: str, name: str) -> tuple[int, int, str]:
    tree = ast.parse(code)
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(nodes) != 1:
        raise ValueError("Expected one top-level function: " + name)
    node = nodes[0]
    lines = code.splitlines(keepends=True)
    return node.lineno, node.end_lineno, "".join(lines[node.lineno - 1:node.end_lineno])


def transform(path: Path, replacements: dict[str, Path]) -> tuple[str, str, bool]:
    original = path.read_text(encoding="utf-8-sig")
    altered = original
    target_spans = []
    for name, code_path in replacements.items():
        new_code = code_path.read_text(encoding="utf-8").rstrip() + "\n"
        tree = ast.parse(new_code)
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef) or tree.body[0].name != name:
            raise ValueError("Invalid full replacement function " + name)
        start, end, previous = function_span(original, name)
        if path.name == PRODUCTION.name and name == "expand_cited_ehp_terminal_goal":
            if ("historical EHP premise contract changed" not in previous
                    or "expand_registered_ehp_terminal_goal" not in previous):
                raise ValueError("R3U2 production function guard mismatch")
        if previous.rstrip() == new_code.rstrip():
            continue
        target_spans.append((start, end, new_code))
    if not target_spans:
        return original, original, False
    lines = altered.splitlines(keepends=True)
    for start, end, replacement in sorted(target_spans, reverse=True):
        lines[start - 1:end] = [replacement]
    altered = "".join(lines)
    ast.parse(altered)
    return original, altered, original != altered


def install() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True,
    ).strip()
    print("R3U2_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("R3U2 requires the develop branch")
    staged = {}
    for relative, functions in REPLACEMENTS.items():
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError("Missing required file: " + str(relative))
        previous, updated, changed = transform(path, functions)
        staged[relative] = (previous, updated, changed)
    metadata_path = OUTPUT / "installed.json"
    if metadata_path.exists():
        prior = json.loads(metadata_path.read_text(encoding="utf-8"))
        same_after = all(
            str(relative) in prior
            and hashlib.sha256(previous.encode()).hexdigest() == prior[str(relative)]["sha_after"]
            for relative, (previous, updated, changed) in staged.items()
        )
        if same_after:
            print("R3U2_ALREADY_APPLIED=True")
            print("R3U2_PATCH_COMPLETE=True")
            print("R3U2_FULL_CODE=" + str(OUTPUT))
            return
        same_before = all(
            str(relative) in prior
            and hashlib.sha256(previous.encode()).hexdigest() == prior[str(relative)]["sha_before"]
            for relative, (previous, updated, changed) in staged.items()
        )
        if not same_before:
            raise RuntimeError("R3U2 tracked files changed since prior installation; inspect backups")
    metadata = {}
    for relative, (previous, updated, changed) in staged.items():
        saved_name = str(relative).replace("/", "__").replace("\\", "__")
        before = OUTPUT / (saved_name + ".before")
        after = OUTPUT / (saved_name + ".FULL.py")
        before.write_text(previous, encoding="utf-8")
        after.write_text(updated, encoding="utf-8")
        metadata[str(relative)] = {
            "sha_before": hashlib.sha256(previous.encode()).hexdigest(),
            "sha_after": hashlib.sha256(updated.encode()).hexdigest(),
            "changed": changed,
        }
    for relative, (previous, updated, changed) in staged.items():
        if changed:
            (ROOT / relative).write_text(updated, encoding="utf-8")
            print("R3U2_PATCHED=" + str(relative))
        else:
            print("R3U2_ALREADY_APPLIED=" + str(relative))
    (OUTPUT / "installed.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print("R3U2_PATCH_COMPLETE=True")
    print("R3U2_FULL_CODE=" + str(OUTPUT))


def restore() -> None:
    meta_file = OUTPUT / "installed.json"
    if not meta_file.exists():
        raise RuntimeError("R3U2 restore metadata missing")
    metadata = json.loads(meta_file.read_text(encoding="utf-8"))
    for relative, data in metadata.items():
        if not data["changed"]:
            continue
        target = ROOT / relative
        current_hash = hashlib.sha256(target.read_text(encoding="utf-8").encode()).hexdigest()
        if current_hash != data["sha_after"]:
            raise RuntimeError("Refusing to overwrite subsequent edits: " + relative)
        saved_name = relative.replace("/", "__").replace("\\", "__")
        backup = OUTPUT / (saved_name + ".before")
        target.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
        print("R3U2_RESTORED=" + relative)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: python install.py install|restore")
    if sys.argv[1] == "install":
        install()
    else:
        restore()
