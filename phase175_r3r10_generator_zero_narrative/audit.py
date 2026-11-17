"""R3R10 read-only preflight and guarded, display-only integration gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r10_generator_zero_narrative import install

GATE = "PASS_R3R10_LEMMA57_ZERO_GENERATOR_NARRATIVE_VISIBLE"
TEST_PATHS = (
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_install.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_rule.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_route.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py",
)


def _command(root: Path, *argv: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, check=False,
    )


def _check_git(root: Path) -> dict[str, str]:
    if not (root / ".git").exists():
        raise RuntimeError("R3R10_REPOSITORY_ROOT_REQUIRED")
    commands = {
        "branch": ("git", "branch", "--show-current"),
        "head": ("git", "rev-parse", "HEAD"),
        "blob": ("git", "rev-parse", "HEAD:" + install.TARGET_RELATIVE.as_posix()),
        "target_status": ("git", "status", "--porcelain", "--", install.TARGET_RELATIVE.as_posix()),
    }
    values = {}
    for key, command in commands.items():
        result = _command(root, *command)
        if result.returncode:
            raise RuntimeError("R3R10_GIT_PREFLIGHT_FAILED: " + key)
        values[key] = result.stdout.strip()
    if values["branch"] != "develop":
        raise RuntimeError("R3R10_DEVELOP_BRANCH_REQUIRED")
    if values["blob"] != install.PINNED_HEAD_BLOB:
        raise RuntimeError("R3R10_REVIEWED_SOURCE_BLOB_CHANGED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R10_R3R9_SOURCE_REQUIRED")
    return values


def _audit_public_result() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    data = inspect_one_group(3, 4)
    certificate = verify_public_result(data)
    source_numbers = {
        ref["number"] for ref in data["references"]
        if ref.get("locator") == "Lemma 5.7"
    }
    if len(source_numbers) != 1:
        raise RuntimeError("R3R10_LEMMA57_CITATION_NOT_UNIQUE")
    source_number = next(iter(source_numbers))
    markdown = data.get("markdown")
    if not isinstance(markdown, str):
        raise RuntimeError("R3R10_MODEL_NARRATIVE_MISSING")
    body = markdown.split("\n証明\n", 1)[-1]
    formula = re.compile(
        r"\[R" + str(source_number) + r"\]より,\s*"
        r"\$E\(\\eta_\{?2\}?[^$]*\\nu[^$]*\)=0\$\."
    )
    match = formula.search(body)
    if match is None:
        raise RuntimeError("R3R10_EXPLICIT_LEMMA57_SENTENCE_MISSING")
    zero_map = re.search(r"\$E:\\pi_\{6\}\^\{2\}\\to\s*\\pi_\{7\}\^\{3\}\$ は零写像", body)
    if zero_map is None:
        raise RuntimeError("R3R10_ZERO_MAP_NARRATIVE_MISSING")
    if match.end() >= zero_map.start():
        raise RuntimeError("R3R10_LEMMA57_SENTENCE_NOT_BEFORE_ZERO_MAP")
    web_lines = data.get("web_lines")
    if not isinstance(web_lines, list) or not any(
        "E(" in str(line.get("math")) and "=0" in str(line.get("math"))
        for line in web_lines
    ):
        raise RuntimeError("R3R10_WEB_GENERATOR_ZERO_LINE_MISSING")
    return {
        "search_status": certificate["search_status"],
        "web": certificate["web"],
        "trust": data.get("trust_verified"),
        "lemma57_reference": f"[R{source_number}]",
        "display_line": match.group(0),
        "reference_count": data.get("reference_count"),
        "lemma54_used": certificate["lemma54_used"],
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = Path(root).resolve()
    values = _check_git(root)
    plan = install.plan_patch(root)
    target = root / install.TARGET_RELATIVE
    if plan.status == "PATCH_REQUIRED" and values["target_status"]:
        raise RuntimeError("R3R10_PREEXISTING_TARGET_MODIFICATION_REFUSED")
    print("PHASE175_R3R10_BRANCH=" + values["branch"])
    print("PHASE175_R3R10_HEAD=" + values["head"])
    print("PHASE175_R3R10_REVIEWED_BLOB=" + values["blob"])
    print("PHASE175_R3R10_PATCH_STATUS=" + plan.status)
    print("PHASE175_R3R10_NEW_GIVEN=0")
    print("PHASE175_R3R10_NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print("PHASE175_R3R10_GATE=PASS_R3R10_READ_ONLY_DRYRUN")
        return 0

    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / "phase175_r3r10_generator_zero_narrative"
    folder.mkdir(parents=True, exist_ok=True)
    backup = folder / "phase168_r3_27_before_r3r10.py"
    if plan.status == "PATCH_REQUIRED":
        backup.write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = (
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
            *TEST_PATHS,
        )
        test_result = subprocess.run(
            command, cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=env, timeout=timeout_seconds,
            check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            test_result.stdout + "\n" + test_result.stderr, encoding="utf-8",
        )
        print(test_result.stdout[-3000:])
        if test_result.returncode:
            raise RuntimeError("R3R10_FOCUSED_PYTEST_FAILED")
        print("PHASE175_R3R10_FOCUSED_PYTEST=PASS")
        public = _audit_public_result()
        report = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "git_head": values["head"],
            "original_sha256": hashlib.sha256(plan.old_bytes).hexdigest(),
            "installed_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "public": public,
        }
        (folder / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8",
        )
        for key, value in public.items():
            print(f"PHASE175_R3R10_{key.upper()}={value}")
        print("PHASE175_R3R10_GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print("PHASE175_R3R10_ROLLBACK=RESTORED")
            else:
                print("PHASE175_R3R10_ROLLBACK=MANUAL_INSPECTION_REQUIRED")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        return run(args.root, args.dry_run, args.timeout_seconds)
    except Exception:
        traceback.print_exc()
        print("PHASE175_R3R10_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
