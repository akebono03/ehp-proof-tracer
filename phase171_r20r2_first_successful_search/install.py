"""Safe R20R2 installation: narrow AST replacement, optional certified R20 undo."""
from __future__ import annotations

import argparse
import ast
import difflib
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SEARCH_PATH = Path("phase165_r3_recursive_search.py")
R20_PATH = Path("phase165_r52_r9_shared_math.py")
EXPECTED_BLOBS = {
    SEARCH_PATH: "9c424f61a2b4a2d7789777017ad4f91292b0ad30",
    R20_PATH: "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def normalize(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def node_span(source: str, name: str, kind: type) -> tuple[int, int]:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, kind) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one top-level {name}")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:node.lineno - 1])
    end = sum(len(line) for line in lines[:node.end_lineno])
    return start, end


def replace_node(source: str, new_text: str, name: str, kind: type) -> str:
    start, end = node_span(source, name, kind)
    return source[:start] + new_text.strip("\n") + "\n" + source[end:]


def r20_change_is_identifiable(base: str, current: str) -> tuple[bool, str]:
    before = base.splitlines()
    after = current.splitlines()
    start = next((i for i, line in enumerate(before)
                  if line.startswith("def shared_expansion_provider(")), None)
    if start is None:
        return False, "missing shared provider"
    opcodes = [op for op in difflib.SequenceMatcher(
        None, before, after, autojunk=False,
    ).get_opcodes() if op[0] != "equal"]
    if not opcodes:
        return True, "no R20 working-tree diff"
    added = sum(j2 - j1 for _, i1, i2, j1, j2 in opcodes)
    deleted = sum(i2 - i1 for _, i1, i2, j1, j2 in opcodes)
    if (not opcodes or len(opcodes) > 2 or max(added, deleted) > 8
            or added + deleted > 16 or any(i1 <= start for _, i1, _, _, _ in opcodes)):
        return False, f"non-isolated patch (hunks={len(opcodes)}, added={added}, deleted={deleted})"
    changed = "\n".join(
        before[i1:i2][0] if i2 - i1 == 1 else "\n".join(before[i1:i2])
        for _, i1, i2, _, _ in opcodes
    ) + "\n" + "\n".join(
        "\n".join(after[j1:j2]) for _, _, _, j1, j2 in opcodes
    )
    if "eta" not in changed.lower() and "η" not in changed:
        return False, "isolated changes are not identifiable as eta-specific"
    # Do not claim we can identify arbitrary 8-line patches without markers.
    if not any(marker in changed.lower() for marker in (
        "r20", "specializ", "eta_route", "eta_special", "higher_eta",
    )):
        return False, "R20 provenance marker not found in changed lines"
    return True, f"isolated R20 eta edit (hunks={len(opcodes)}, added={added}, deleted={deleted})"


def run(dry_run: bool, keep_r20: bool) -> None:
    if not (ROOT / ".git").exists():
        raise RuntimeError("Unpack this package directly under the Git repository root")
    branch = git("branch", "--show-current").stdout.decode().strip()
    if branch != "develop":
        raise RuntimeError(f"Expected develop branch, found {branch}")
    for path, expected in EXPECTED_BLOBS.items():
        blob = git("rev-parse", f"HEAD:{path.as_posix()}").stdout.decode().strip()
        if blob != expected:
            raise RuntimeError(f"Unexpected HEAD blob for {path}: {blob}; expected {expected}")
    old_bytes = (ROOT / SEARCH_PATH).read_bytes()
    old_source = normalize(old_bytes)
    base_source = normalize(git("show", f"HEAD:{SEARCH_PATH.as_posix()}").stdout)
    new_function = (PACKAGE / "reconstruct_registered_goal_FULL.py").read_text(encoding="utf-8")
    classes_source = (PACKAGE / "class_definitions_FULL.py").read_text(encoding="utf-8")
    classes_tree = ast.parse(classes_source)
    classes = {
        node.name: ast.get_source_segment(classes_source, node) + "\n"
        for node in classes_tree.body if isinstance(node, ast.ClassDef)
    }
    if old_source != base_source:
        # An already installed R20R2 version is handled as a no-op, but
        # any other preexisting edits to this file must not be overwritten.
        start, end = node_span(old_source, "reconstruct_registered_goal", ast.FunctionDef)
        current_fn = old_source[start:end].strip()
        if current_fn != new_function.strip():
            raise RuntimeError("Recursive search has local edits; refusing replacement")
        desired = old_source
        print("PHASE171_R20R2_SEARCH=ALREADY_INSTALLED")
    else:
        if ("expected one registered derivation" not in old_source
                or "append_unique_verified_derivation(options, step)" not in old_source):
            raise RuntimeError("Canonical original search contract not found")
        desired = replace_node(old_source, new_function, "reconstruct_registered_goal", ast.FunctionDef)
        for name in ("RegisteredGoalUnresolved", "SourceBoundGoal"):
            desired = replace_node(desired, classes[name], name, ast.ClassDef)
    ast.parse(desired)
    r20_bytes = (ROOT / R20_PATH).read_bytes()
    r20_current = normalize(r20_bytes)
    r20_baseline_bytes = git("show", f"HEAD:{R20_PATH.as_posix()}").stdout
    r20_base = normalize(r20_baseline_bytes)
    if r20_current == r20_base:
        r20_action = "ALREADY_CLEAN"
    elif keep_r20:
        r20_action = "PRESERVED_BY_EXPLICIT_OVERRIDE"
    else:
        ok, detail = r20_change_is_identifiable(r20_base, r20_current)
        print("PHASE171_R20R2_R20_PREFLIGHT=" + detail)
        if not ok:
            raise RuntimeError(
                "Uncommitted shared_math.py edits could not be positively isolated as R20. "
                "No files changed. Inspect git diff first; use -KeepR20 only if intentional."
            )
        r20_action = "RESTORE_EXACT_HEAD_AFTER_BACKUP"
    print("PHASE171_R20R2_BRANCH=" + branch)
    print("PHASE171_R20R2_R20_ACTION=" + r20_action)
    print("PHASE171_R20R2_SEARCH_ACTION=" + ("UNCHANGED" if desired == old_source else "PATCH"))
    if dry_run:
        print("PHASE171_R20R2_RESULT=PASS_DRY_RUN")
        return
    # Backups retain original *bytes* including any uncommitted R20 changes.
    out = PACKAGE / "output" / (datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    out.mkdir(parents=True, exist_ok=False)
    (out / "phase165_r3_recursive_search.py.before").write_bytes(old_bytes)
    (out / "phase165_r52_r9_shared_math.py.before").write_bytes(r20_bytes)
    print("PHASE171_R20R2_BACKUP=" + str(out))
    if desired != old_source:
        newline = "\r\n" if b"\r\n" in old_bytes else "\n"
        (ROOT / SEARCH_PATH).write_bytes(desired.replace("\n", newline).encode("utf-8"))
    if r20_action == "RESTORE_EXACT_HEAD_AFTER_BACKUP":
        (ROOT / R20_PATH).write_bytes(r20_baseline_bytes)
    print("PHASE171_R20R2_RESULT=PATCHED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-r20", action="store_true")
    args = parser.parse_args()
    run(args.dry_run, args.keep_r20)
