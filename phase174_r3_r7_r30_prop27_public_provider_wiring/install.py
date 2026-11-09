"""Guarded, idempotent R30 installation into exactly two shared functions.

The installer saves the COMPLETE resulting changed functions and import section
for inspection. No text outside those two function bodies is replaced.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
BASE = "94d4e655a76a90d33045b7143c6e6870e453be82"
PACKAGE = "phase174_r3_r7_r30_prop27_public_provider_wiring/"
ALLOWED_HISTORY = (
    "phase174_r3_r7_r29_prop27_canonical_provider/",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/",
)
CACHE = ".pytest_cache/v/cache/nodeids"
BRIDGE_ANCHOR = "        sources = sources + (build_isolated_toda59_annihilator_bridge(),)"
BRIDGE_ADDITION = (
    "        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (\n"
    "            register_positioned_prop27,\n"
    "        )\n"
    "        sources = sources + (register_positioned_prop27(Path(__file__).resolve().parent),)"
)
PROVIDER_ANCHOR = "        options = []\n        from phase174_r3_r7_r3_ehp_zero_rule.rule import ("
PROVIDER_ADDITION = (
    "        options = []\n"
    "        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (\n"
    "            expand_public_cited_prop27_goal,\n"
    "        )\n"
    "        cited_prop27_options = expand_public_cited_prop27_goal(goal, bridge)\n"
    "        if cited_prop27_options:\n"
    "            return cited_prop27_options\n"
    "        from phase174_r3_r7_r3_ehp_zero_rule.rule import ("
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT,
                          text=True, capture_output=True, check=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def normalized(text: str) -> str:
    return text.replace("\r\n", "\n")


def patch_source(text: str) -> str:
    """Return full module text, replacing only two function-local anchors."""
    clean = normalized(text)
    if BRIDGE_ADDITION not in clean:
        if clean.count(BRIDGE_ANCHOR) != 1:
            raise RuntimeError("source bridge installation anchor changed")
        clean = clean.replace(BRIDGE_ANCHOR, BRIDGE_ANCHOR + "\n" + BRIDGE_ADDITION)
    if PROVIDER_ADDITION not in clean:
        if clean.count(PROVIDER_ANCHOR) != 1:
            raise RuntimeError("shared provider installation anchor changed")
        clean = clean.replace(PROVIDER_ANCHOR, PROVIDER_ADDITION)
    tree = ast.parse(clean)
    relevant = {node.name for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in ("build_shared_typed_bridge", "shared_expansion_provider")}
    if relevant != {"build_shared_typed_bridge", "shared_expansion_provider"}:
        raise RuntimeError("shared function identity changed")
    return clean


def preflight() -> tuple[str, str, bool]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("unexpected repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/develop")
    if not remote or remote.split()[0] != head:
        raise RuntimeError("local/remote HEAD mismatch")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                              cwd=ROOT, capture_output=True)
    if ancestor.returncode:
        raise RuntimeError("reviewed R29 HEAD is not ancestor")
    changed = git("diff", "--name-only", BASE, head).splitlines()
    bad = tuple(x for x in changed if x != CACHE
                and not any(x.startswith(prefix) for prefix in ALLOWED_HISTORY))
    if bad:
        raise RuntimeError("unreviewed committed files: " + repr(bad))
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("staged changes require manual review: " + repr(staged))
    # The initial source is compared with the reviewed Git blob, NOT with a
    # presumed local branch tip. After R30, the unique expected patch is allowed.
    baseline = subprocess.run(("git", "show", BASE + ":phase165_r52_r9_shared_math.py"),
                              cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8-sig")
    original = TARGET.read_text(encoding="utf-8-sig")
    expected = patch_source(baseline)
    if normalized(original) not in (normalized(baseline), expected):
        raise RuntimeError("shared source differs from reviewed baseline/R30 patch")
    tracked = git("diff", "--name-only").splitlines()
    if any(x not in (CACHE, "phase165_r52_r9_shared_math.py") for x in tracked):
        raise RuntimeError("unreviewed working tracked changes")
    for filename in (
        "sources/toda/Toda_02_2.tex",
        "proof.py",
        "homotopy_groups.py",
        "phase165_r3_recursive_search.py",
        "phase174_r3_r7_r28_prop27_typed_literature_registration/registration.py",
        "phase174_r3_r7_r29_prop27_canonical_provider/provider.py",
    ):
        version = git("status", "--porcelain", "--", filename)
        if version:
            reviewed_r29 = (
                filename == "phase174_r3_r7_r29_prop27_canonical_provider/provider.py"
                and version.startswith("?? ")
                and hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
                == "99b8955b1089021ce9fb1bdd9c77dcd9998a7b6e735550b259ea186216923745"
            )
            if not reviewed_r29:
                raise RuntimeError("reviewed dependency has modifications: " + filename)
    return head, expected, normalized(original) == expected


def save_full_units(full_module: str) -> None:
    """Write full replaceable functions and COMPLETE original import section."""
    tree = ast.parse(full_module)
    lines = full_module.splitlines(keepends=True)
    output = ROOT / PACKAGE / "CHANGED_FUNCTIONS_FULL.py"
    parts = ['"""Complete reviewed R30 function replacements. Generated by install.py."""\n\n']
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
            "build_shared_typed_bridge", "shared_expansion_provider"
        ):
            parts.extend(lines[node.lineno - 1:node.end_lineno])
            parts.append("\n\n")
    output.write_text("".join(parts), encoding="utf-8")
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.extend(lines[node.lineno - 1:node.end_lineno])
    (ROOT / PACKAGE / "IMPORTS_FULL.txt").write_text("".join(imports), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, expected, installed = preflight()
    print("PHASE174_R3R7R30_HEAD=" + head)
    print("PHASE174_R3R7R30_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R30_ALREADY_INSTALLED=" + str(installed))
    if args.dry_run:
        print("PHASE174_R3R7R30_MODE=DRYRUN")
        print("PHASE174_R3R7R30_GATE=PASS_R30_PREFLIGHT")
        print("(END)")
        return 0
    if not installed:
        raw = TARGET.read_bytes()
        end = b"\r\n" if b"\r\n" in raw else b"\n"
        output = expected.replace("\n", end.decode("ascii"))
        TARGET.write_bytes(output.encode("utf-8"))
    save_full_units(expected)
    print("PHASE174_R3R7R30_SHARED_BRIDGE_WIRED=True")
    print("PHASE174_R3R7R30_SHARED_PROVIDER_WIRED=True")
    print("PHASE174_R3R7R30_NEW_SPECIALIZED_GIVEN=0")
    print("PHASE174_R3R7R30_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R30_FULL_PYTEST=False")
    print("PHASE174_R3R7R30_GATE=PASS_R30_INSTALLED_TESTS_PENDING")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
