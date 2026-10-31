"""Guarded Phase 172 R2 single-function insertion and focused verification.

Only phase168_r3_5_model_renderer.py is an existing production modification.
No mathematical proof or inference registration changes. Outputs and backup
are placed outside the Git worktree. On failure, source bytes are restored.
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

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path("phase168_r3_5_model_renderer.py")
PROJECTION = Path("phase172_r2_suspension_relation_display/projection.py")
REVIEWED_BLOB = "94996b403f1c01f81319824565db422463714f02"
ORIGINAL_ANCHOR = (
    "    if direct_sum_display is not None:\n"
    "        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n"
    "    for index in order:\n"
)
UPDATED_ANCHOR = (
    "    if direct_sum_display is not None:\n"
    "        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n"
    "    if not incomplete:\n"
    "        from phase172_r2_suspension_relation_display.projection import (\n"
    "            redundant_suspension_relation_indices,\n"
    "        )\n"
    "        suppressed_body_indices.update(\n"
    "            redundant_suspension_relation_indices(\n"
    "                model, order, suppressed_body_indices,\n"
    "            )\n"
    "        )\n"
    "    for index in order:\n"
)
TEST_GROUPS = (
    ("phase172_r2_suspension_relation_display/tests/test_projection.py",),
    ("phase171_r20r13_eta_sentence_layout/tests/test_projection.py",),
    ("phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",),
    ("phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",),
    ("phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py",),
)


def command(*args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )


def checked(*args: str) -> str:
    result = command(*args)
    if result.returncode:
        raise RuntimeError("command failed: " + repr(args) + " " + result.stderr)
    return result.stdout.strip()


def lf(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("unreviewed/mixed newline convention")
    return text.replace("\r\n", "\n")


def transformed(source: bytes) -> bytes:
    current = lf(source)
    if current.count(ORIGINAL_ANCHOR) != 1 or UPDATED_ANCHOR in current:
        raise RuntimeError("reviewed renderer anchor not found exactly once")
    updated = current.replace(ORIGINAL_ANCHOR, UPDATED_ANCHOR, 1)
    tree = ast.parse(updated)
    targets = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(targets) != 1:
        raise RuntimeError("renderer function identity changed")
    newline = "\r\n" if b"\r\n" in source else "\n"
    return updated.replace("\n", newline).encode("utf-8")


def function_text(source: bytes) -> str:
    updated = lf(source)
    tree = ast.parse(updated)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "render_model_backed_narrative_markdown"]
    if len(functions) != 1:
        raise RuntimeError("exactly one renderer function is required")
    node = functions[0]
    lines = updated.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def report_dir() -> Path:
    home = os.environ.get("LOCALAPPDATA")
    base = Path(home) if home else Path.home()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    target = base / "EHPProofTracerRecovery" / ("phase172_r2_" + stamp)
    target.mkdir(parents=True, exist_ok=False)
    return target


def preflight() -> dict[str, str]:
    branch = checked("git", "branch", "--show-current")
    head = checked("git", "rev-parse", "HEAD")
    blob = checked("git", "rev-parse", "HEAD:" + TARGET.as_posix())
    if branch != "develop":
        raise RuntimeError("R2 requires the develop branch")
    if blob != REVIEWED_BLOB:
        raise RuntimeError("reviewed source Git blob differs; do not patch")
    if not (ROOT / PROJECTION).is_file():
        raise RuntimeError("R2 projection module is absent")
    result = command("git", "status", "--porcelain", "--", TARGET.as_posix())
    if result.returncode:
        raise RuntimeError("unable to inspect tracked renderer status")
    if result.stdout.strip():
        raise RuntimeError("existing renderer has local changes; do not overwrite")
    tracked_result = subprocess.run(
        ("git", "show", "HEAD:" + TARGET.as_posix()),
        cwd=ROOT, check=True, capture_output=True,
    )
    tracked = tracked_result.stdout
    # Binary worktree comparison below is intentionally newline-tolerant;
    # HEAD blob identity remains the immutable reviewed-source guard.
    source = (ROOT / TARGET).read_bytes()
    if lf(source) != lf(tracked):
        raise RuntimeError("local renderer differs from reviewed HEAD content")
    if source.decode("utf-8-sig").startswith("\ufeff"):
        raise RuntimeError("unexpected source encoding")
    updated = transformed(source)
    return {
        "branch": branch,
        "head": head,
        "reviewed_git_blob": blob,
        "before_sha256": hashlib.sha256(source).hexdigest(),
        "after_sha256": hashlib.sha256(updated).hexdigest(),
    }


def run_focused(output: Path) -> list[dict[str, object]]:
    results = []
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    for i, paths in enumerate(TEST_GROUPS, 1):
        process = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
             "-p", "no:cacheprovider", *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
        log = process.stdout + "\n" + process.stderr
        (output / f"focused_{i}.log").write_text(log, encoding="utf-8")
        results.append({"group": i, "paths": paths, "returncode": process.returncode,
                        "last_lines": log.splitlines()[-8:]})
        print(f"PHASE172_R2_FOCUSED_{i}=" +
              ("PASS" if process.returncode == 0 else "FAIL"), flush=True)
        if process.returncode:
            raise RuntimeError(f"focused pytest group {i} failed: " + log[-2000:])
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    state = preflight()
    print("PHASE172_R2_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R2_HEAD=" + state["head"], flush=True)
    print("PHASE172_R2_REVIEWED_BLOB=PASS", flush=True)
    original = (ROOT / TARGET).read_bytes()
    updated = transformed(original)
    if args.dry_run:
        output = report_dir()
        (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
            function_text(updated) + "\n", encoding="utf-8",
        )
        (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(updated)
        print("PHASE172_R2_DRY_RUN=PASS", flush=True)
        print("PHASE172_R2_FULL_FUNCTION=" + str(output), flush=True)
        print("PHASE172_R2_SOURCE_CHANGES=0", flush=True)
        return 0

    output = report_dir()
    (output / "renderer_before.py").write_bytes(original)
    report: dict[str, object] = {
        "phase": "172-R2", "mode": "GUARDED_PRESENTATION_ONLY",
        "source": str(TARGET), "state": state,
        "focused": [], "full_pytest_executed": False,
        "proof_tree_changed": False, "math_inference_changed": False,
    }
    try:
        (ROOT / TARGET).write_bytes(updated)
        (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
            function_text(updated) + "\n", encoding="utf-8",
        )
        (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(updated)
        if args.run_focused_tests:
            report["focused"] = run_focused(output)
        report["result"] = "PASS_R2_PRESENTATION_ONLY"
    except BaseException:
        (ROOT / TARGET).write_bytes(original)
        report["result"] = "FAILED_RESTORED_ORIGINAL_SOURCE"
        (output / "result.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("PHASE172_R2_RESTORED=PASS", flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("PHASE172_R2_REPORT=" + str(output), flush=True)
    print("PHASE172_R2_SOURCE_CHANGES=1", flush=True)
    print("PHASE172_R2_RESULT=PASS_R2_PRESENTATION_ONLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
