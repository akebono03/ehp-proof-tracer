"""Safely install only the reviewed R4-R13 Source Guard lineage correction.

The existing R4-R13 audit remains read-only regarding application source.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import tempfile

OLD_SHA256 = "90e5cae1c55fef79220f430f560cbe4f754cedf26f919d514f7f8e9461180c37"
NEW_SHA256 = "4eb8cfb7885d42f6769906119ba19b3d29c52ba61403ce9497cbe0fa7663ade5"
OLD_HEAD = "a9b4617fbef603e4ced2252b7812d2dfa19fc606"
REVIEWED_HEAD = "33f73f1dfb853875589b8fb70bda9853c75a8dae"
AUDIT_PATH = "phase173_r4_r13_narrative_audit/audit.py"
WEB_ADAPTER_PATH = "phase165_r52_r3_web_adapter.py"
COMMITTED_WEB_BLOB = "57b079d51d6d5810ab0be6884feae1ed117a386c"


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Git state check failed: " + " ".join(arguments))
    return result.stdout.strip()


def replacement_audit(original: bytes, fixture: bytes) -> bytes:
    """Change only source_guard, with no new imports or audit semantics."""
    if sha256(original).hexdigest() != OLD_SHA256:
        raise RuntimeError("R4-R13 original audit is not the reviewed source")
    if sha256(fixture).hexdigest() != NEW_SHA256:
        raise RuntimeError("R4-R13 corrected audit fixture is not reviewed")
    before = ast.parse(original.decode("utf-8"))
    after = ast.parse(fixture.decode("utf-8"))
    def other_nodes(tree: ast.Module) -> list[str]:
        return [ast.dump(node, include_attributes=False) for node in tree.body
                if not (isinstance(node, ast.FunctionDef)
                        and node.name == "source_guard")]
    if other_nodes(before) != other_nodes(after):
        raise RuntimeError("Audit code outside source_guard differs")
    old_fn = [n for n in before.body if isinstance(n, ast.FunctionDef)
              and n.name == "source_guard"]
    new_fn = [n for n in after.body if isinstance(n, ast.FunctionDef)
              and n.name == "source_guard"]
    if len(old_fn) != 1 or len(new_fn) != 1:
        raise RuntimeError("Expected exactly one complete source_guard")
    compile(fixture.decode("utf-8"), AUDIT_PATH, "exec")
    return fixture


def preflight(root: Path, package: Path) -> tuple[Path, bytes, bytes, bool]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Run from the exact repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Develop branch required")
    if git(root, "rev-parse", "HEAD") != REVIEWED_HEAD:
        raise RuntimeError("Committed R4-R12 HEAD differs from reviewed lineage")
    remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop").split()[0]
    if remote != REVIEWED_HEAD:
        raise RuntimeError("GitHub develop HEAD differs from reviewed lineage")
    if git(root, "diff", "--cached", "--name-only") or git(root, "diff", "--name-only"):
        raise RuntimeError("All tracked files must be clean before the audit-only repair")
    if git(root, "rev-parse", "HEAD:" + WEB_ADAPTER_PATH) != COMMITTED_WEB_BLOB:
        raise RuntimeError("R4-R12 committed Web adapter differs from reviewed source")
    target = root / AUDIT_PATH
    if not target.is_file():
        raise RuntimeError("R4-R13 audit package not extracted")
    fixture_path = package / "replacement_audit.py.txt"
    current = target.read_bytes()
    fixture = fixture_path.read_bytes()
    if sha256(fixture).hexdigest() != NEW_SHA256:
        raise RuntimeError("R4-R13 correction fixture has changed")
    if sha256(current).hexdigest() == NEW_SHA256:
        return target, current, fixture, True
    new = replacement_audit(current, fixture)
    return target, current, new, False


def apply(root: Path, package: Path, *, dry_run: bool) -> str:
    target, original, replacement, already = preflight(root, package)
    print("PHASE173_R4_R13R1_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R13R1_HEAD=" + REVIEWED_HEAD, flush=True)
    if dry_run:
        print("PHASE173_R4_R13R1_DRY_RUN=PASS", flush=True)
        return "PASS_DRY_RUN"
    if already:
        print("PHASE173_R4_R13R1_ALREADY_INSTALLED=True", flush=True)
        return "ALREADY_INSTALLED"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=target.parent, prefix=".r4r13r1_",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if target.read_bytes() != original:
            raise RuntimeError("Audit source changed during repair")
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print("PHASE173_R4_R13R1_PATCHED=" + AUDIT_PATH, flush=True)
    return "PATCHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    package = Path(__file__).resolve().parent
    apply(root, package, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
