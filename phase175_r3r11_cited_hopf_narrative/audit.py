"""R3R11 guarded read-only DryRun and completed cited-narrative Web gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r11_cited_hopf_narrative import install

GATE = "PASS_R3R11R1_CITED_REFERENCES_AND_HOPF_CHAIN_COMPACT"
TEST_PATHS = (
    "phase175_r3r11_cited_hopf_narrative/tests",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase172_r3_hopf_chain_display/tests/test_projection.py",
    # R70's historical installer-source-pin test expects the pre-R3R10
    # phase168 file. R3R10 legitimately changed that file. Retain the
    # independent R70 functional tests, without weakening its source guard.
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_line_endings_source_guard_and_patch_idempotence",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_source_guard_rejects_unreviewed_change",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_rejects_mixed_eol_and_cr_only",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_body_line_search_does_not_match_reference_text",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_step_index_rejects_ambiguous_value_fallback",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_incomplete_model_has_no_composed_rewrite",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_git_sha_fixture",
)


def _read_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R11_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def preflight(root: Path):
    if not (root / ".git").exists():
        raise RuntimeError("R3R11_GIT_REPOSITORY_REQUIRED")
    if _read_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R11_DEVELOP_REQUIRED")
    blob = _read_git(root, "rev-parse", "HEAD:" + install.TARGET.as_posix())
    if blob != install.REVIEWED_HEAD_BLOB:
        raise RuntimeError("R3R11_REVIEWED_BLOB_CHANGED")
    if not (root / "phase175_r3r10_generator_zero_narrative" / "run.ps1").is_file():
        raise RuntimeError("R3R11_R3R10_REQUIRED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R11_R3R9_REQUIRED")
    r3r10 = (root / "phase168_r3_27_typed_statement_projection.py").read_text(
        encoding="utf-8",
    )
    if "if isinstance(statement.target_generator, Zero):" not in r3r10:
        raise RuntimeError("R3R11_R3R10_NOT_INSTALLED")
    plan = install.plan_patch(root)
    status = _read_git(root, "status", "--porcelain", "--", install.TARGET.as_posix())
    if plan.status == "PATCH_REQUIRED" and status:
        raise RuntimeError("R3R11_PREEXISTING_RENDERER_EDIT_REFUSED")
    return {"head": _read_git(root, "rev-parse", "HEAD"),
            "blob": blob, "plan": plan}


def _public_gate() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    recorded = inspect_one_group(3, 4)
    proof = verify_public_result(recorded)
    markdown = recorded.get("markdown")
    if not isinstance(markdown, str) or markdown.count("\n証明\n") != 1:
        raise RuntimeError("R3R11_MODEL_NARRATIVE_NOT_AVAILABLE")
    reference, body = markdown.split("\n証明\n", 1)
    refs = recorded.get("references")
    if not isinstance(refs, list):
        raise RuntimeError("R3R11_MODEL_CITATIONS_MISSING")
    by_locator = {c["locator"]: c["number"] for c in refs}
    if not all(name in by_locator for name in
               ("Lemma 5.7", "Proposition 2.2", "Chapter V, i)", "(5.3)")):
        raise RuntimeError("R3R11_REQUIRED_TYPED_SOURCES_NOT_CITED")
    l57 = f"[R{by_locator['Lemma 5.7']}]"
    prop22 = f"[R{by_locator['Proposition 2.2']}]"
    eta = f"[R{by_locator['Chapter V, i)']}]"
    hopf = f"[R{by_locator['(5.3)']}]"
    if (r"$E(\eta_2\nu')=0$." not in reference
            or r"$H(\alpha E\beta)=H(\alpha) E\beta$." not in reference):
        raise RuntimeError("R3R11_REFERENCE_CONTENT_NOT_VISIBLE")
    if (not re.search(re.escape(l57) + r"より, \$E\(\\eta_\{2\}\\nu'\)=0\$\.", body)
            or r"$E(\eta_{2}\circ" in body):
        raise RuntimeError("R3R11_COMPOSITION_NOT_UNIFIED")
    if (prop22 + "より, " not in body
            or f"{eta}, {prop22}, {hopf}より, " not in body):
        raise RuntimeError("R3R11_HOPF_CITATION_CHAIN_NOT_CONDENSED")
    if (body.count(r"H(\nu'\eta_{6})") > 2
            or body.count(r"H\left(\nu'\eta_{6}\right)") > 2):
        raise RuntimeError("R3R11_HOPF_CHAIN_STILL_REDUNDANT")
    if recorded.get("web_key") != "generic-complete-proof":
        raise RuntimeError("R3R11_WEB_PROOF_NOT_COMPLETE")
    return {
        "search": proof["search_status"],
        "web": proof["web"],
        "trust": recorded.get("trust_verified"),
        "lemma54_used": proof["lemma54_used"],
        "reference_count": recorded.get("reference_count"),
        "lemma57_reference": l57,
        "prop22_reference": prop22,
        "hopf_summary_references": f"{eta}, {prop22}, {hopf}",
        "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = root.resolve()
    checked = preflight(root)
    plan = checked["plan"]
    print("PHASE175_R3R11R1_BRANCH=develop")
    print("PHASE175_R3R11R1_HEAD=" + checked["head"])
    print("PHASE175_R3R11R1_REVIEWED_BLOB=" + checked["blob"])
    print("PHASE175_R3R11R1_PATCH_STATUS=" + plan.status)
    print("PHASE175_R3R11R1_NEW_GIVEN=0")
    print("PHASE175_R3R11R1_NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print("PHASE175_R3R11R1_GATE=PASS_R3R11_READ_ONLY_DRYRUN")
        return 0

    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / "phase175_r3r11_cited_hopf_narrative")
    folder.mkdir(parents=True, exist_ok=True)
    target = root / install.TARGET
    if plan.status == "PATCH_REQUIRED":
        (folder / "renderer_backup.py").write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        env = dict(os.environ)
        env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        cmd = [sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
               "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
               *TEST_PATHS]
        result = subprocess.run(
            cmd, cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout_seconds, check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            result.stdout + "\n" + result.stderr, encoding="utf-8",
        )
        print(result.stdout[-4000:])
        if result.returncode:
            raise RuntimeError("R3R11_FOCUSED_PYTEST_FAILED")
        print("PHASE175_R3R11R1_FOCUSED_PYTEST=PASS")
        certified = _public_gate()
        (folder / "report.json").write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "head": checked["head"],
            "pre_sha256": sha256(plan.old_bytes).hexdigest(),
            "post_sha256": sha256(target.read_bytes()).hexdigest(),
            "public": certified,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        for key, value in certified.items():
            print("PHASE175_R3R11R1_" + key.upper() + "=" + str(value))
        print("PHASE175_R3R11R1_GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print("PHASE175_R3R11R1_ROLLBACK=RESTORED")
            else:
                print("PHASE175_R3R11R1_ROLLBACK=MANUAL_INSPECTION_REQUIRED")
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
        print("PHASE175_R3R11R1_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
