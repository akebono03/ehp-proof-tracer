"""Guarded Phase 172 R5 public Reference heading patch, focused tests and rollback.

The internal database locator and all proof/citation records are unchanged.
Only the complete-proof Renderer selects a validated Japanese display heading.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from phase172_r3_hopf_chain_display import install as r3_installer
from phase172_r4_hopf_surjectivity_display import install as r4_installer

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path("phase168_r3_5_model_renderer.py")
PROJECTION = Path("phase172_r5_prior_reference_display/projection.py")
TESTS = Path("phase172_r5_prior_reference_display/tests/test_projection.py")
R4_PROJECTION_SHA256 = "68983b5382eb82a66d0a0286b5cd5fbb2844b05694bbad910754b5cef4ba295c"
R4_TEST_SHA256 = "90e5b8629543d0f1bea280a855c360c400f66d4d8180db1be705322a11734bb7"
R4_INSTALL_SHA256 = "b7d13450d71de5417aa9f51c882320c6c98a7405839e27a157b727be38143722"
OLD = (
    "    for citation in model.citations:\n"
    "        locator = citation.reference.locator or citation.reference.label\n"
    "        # Display the cited locator verbatim; no series-specific alias.\n"
    '        lines.append(f"**[R{citation.number}] {locator}.**")\n'
)
NEW = (
    "    from phase172_r5_prior_reference_display.projection import (\n"
    "        display_prior_reference_locator,\n"
    "    )\n"
    "    for citation in model.citations:\n"
    "        locator = citation.reference.locator or citation.reference.label\n"
    "        if not incomplete:\n"
    "            displayed = display_prior_reference_locator(citation, model)\n"
    "            if displayed is not None:\n"
    "                locator = displayed\n"
    '        lines.append(f"**[R{citation.number}] {locator}.**")\n'
)
TEST_GROUPS = (
    ("phase172_r5_prior_reference_display/tests/test_projection.py",),
    ("phase172_r4_hopf_surjectivity_display/tests/test_projection.py",),
    ("phase172_r3_hopf_chain_display/tests/test_projection.py",),
    ("phase172_r2_suspension_relation_display/tests/test_projection.py",),
    ("phase171_r20r13_eta_sentence_layout/tests/test_projection.py",),
    ("phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py",),
)


def command(args: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False, timeout=timeout,
    )


def git(*args: str) -> str:
    if not args or args[0] not in {"branch", "rev-parse", "ls-remote"}:
        raise ValueError("read-only Git information only")
    process = command(["git", *args])
    if process.returncode:
        raise RuntimeError("Git command failed: " + repr(args) + process.stderr[-800:])
    return process.stdout.strip()


def normalize(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise ValueError("mixed line endings in reviewed source")
    return text.replace("\r\n", "\n")


def updated_renderer(source: bytes) -> bytes:
    original = normalize(source)
    if original.count(OLD) != 1 or NEW in original:
        raise RuntimeError("Renderer citation loop does not match reviewed R4 anchor")
    modified = original.replace(OLD, NEW, 1)
    tree = ast.parse(modified)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise RuntimeError("Renderer function identity changed")
    newline = "\r\n" if b"\r\n" in source else "\n"
    return modified.replace("\n", newline).encode("utf-8")


def full_function(source: bytes) -> str:
    text = normalize(source)
    tree = ast.parse(text)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "render_model_backed_narrative_markdown"]
    if len(nodes) != 1:
        raise RuntimeError("Renderer function missing or duplicated")
    node = nodes[0]
    return "\n".join(text.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def preflight() -> dict[str, object]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R5 requires develop branch")
    for path, sha in (
        (Path("phase172_r4_hopf_surjectivity_display/projection.py"), R4_PROJECTION_SHA256),
        (Path("phase172_r4_hopf_surjectivity_display/tests/test_projection.py"), R4_TEST_SHA256),
        (Path("phase172_r4_hopf_surjectivity_display/install.py"), R4_INSTALL_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("R4 prerequisite missing: " + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
            raise RuntimeError("R4 prerequisite differs from reviewed content: " + str(path))
    if (r3_installer.REVIEWED_GIT_BLOB != r4_installer.BASE_R2_BLOB):
        raise RuntimeError("R3/R4 committed baseline mismatch")
    blob = subprocess.run(
        ["git", "cat-file", "blob", r4_installer.BASE_R2_BLOB],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    r3_expected = r3_installer.transformed(blob)
    r4_expected = r4_installer.updated_renderer(r3_expected)
    current = (ROOT / TARGET).read_bytes()
    if normalize(current) != normalize(r4_expected):
        raise RuntimeError("working Renderer is not reviewed R4 content")
    committed = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    if normalize(committed) == normalize(r4_expected):
        state = "R4_COMMITTED"
    elif normalize(committed) == normalize(r3_expected):
        state = "R4_UNCOMMITTED"
    else:
        raise RuntimeError("committed Renderer is not reviewed R3/R4")
    for path in (PROJECTION, TESTS):
        if not (ROOT / path).is_file():
            raise RuntimeError("R5 payload is missing: " + str(path))
        ast.parse((ROOT / path).read_text(encoding="utf-8-sig"))
    updated_renderer(current)
    remote_result = command(["git", "ls-remote", "origin", "refs/heads/develop"], timeout=25)
    remote = (remote_result.stdout.split()[0]
              if remote_result.returncode == 0 and remote_result.stdout.strip() else None)
    if remote is not None and remote != head:
        raise RuntimeError("local HEAD differs from origin/develop")
    return {"branch": branch, "head": head, "remote": remote, "r4_state": state}


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "EHPProofTracerRecovery"
    output = base / ("phase172_r5_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ"))
    output.mkdir(parents=True, exist_ok=False)
    return output


def run_focused(output: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    summary = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        run = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
             "-p", "no:cacheprovider", *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=240,
        )
        log = run.stdout + "\n" + run.stderr
        (output / f"focused_{number}.log").write_text(log, encoding="utf-8")
        summary.append({"group": number, "paths": list(paths), "exit_code": run.returncode})
        print(f"PHASE172_R5_FOCUSED_{number}=" + ("PASS" if run.returncode == 0 else "FAIL"), flush=True)
        if run.returncode:
            raise RuntimeError(f"focused pytest group {number} failed:\n" + log[-3000:])
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.run_focused_tests:
        raise RuntimeError("R5 requires --run-focused-tests for write mode")
    state = preflight()
    print("PHASE172_R5_BRANCH=" + str(state["branch"]), flush=True)
    print("PHASE172_R5_HEAD=" + str(state["head"]), flush=True)
    print("PHASE172_R5_R4_RENDERER_STATE=" + str(state["r4_state"]), flush=True)
    print("PHASE172_R5_REVIEWED_CONTENT=PASS", flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = updated_renderer(before)
    output = output_directory()
    (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
        full_function(after), encoding="utf-8",
    )
    (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(after)
    if args.dry_run:
        print("PHASE172_R5_DRY_RUN=PASS", flush=True)
        print("PHASE172_R5_FULL_FUNCTION=" + str(output), flush=True)
        print("PHASE172_R5_SOURCE_CHANGES=0", flush=True)
        return 0
    (output / "renderer_before.py").write_bytes(before)
    report = {"phase": "172-R5", "mode": "PRESENTATION_ONLY", "state": state,
              "full_pytest_executed": False, "proof_tree_modified": False,
              "mathematical_rules_modified": False, "focused_tests": []}
    try:
        (ROOT / TARGET).write_bytes(after)
        report["focused_tests"] = run_focused(output)
        report["result"] = "PASS_R5_PRIOR_REFERENCE_DISPLAY_ONLY"
    except BaseException as exc:
        (ROOT / TARGET).write_bytes(before)
        report["result"] = "FAIL_RESTORED_SOURCE"
        report["exception"] = repr(exc)
        (output / "result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        print("PHASE172_R5_RESTORED=PASS", flush=True)
        print("PHASE172_R5_REPORT=" + str(output), flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE172_R5_REPORT=" + str(output), flush=True)
    print("PHASE172_R5_SOURCE_CHANGES=1", flush=True)
    print("PHASE172_R5_RESULT=PASS_R5_PRIOR_REFERENCE_DISPLAY_ONLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
