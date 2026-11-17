"""R3R12 read-only preflight, focused tests and public source-bound gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r12_hopf_conclusion import install

GATE = "PASS_R3R12R4_VERIFIED_HOPF_ISOMORPHISM_SINGLE_CONCLUSION"
TEST_PATHS = (
    "phase175_r3r12_hopf_conclusion/tests",
    "phase175_r3r11_cited_hopf_narrative/tests",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase172_r3_hopf_chain_display/tests/test_projection.py",
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
        raise RuntimeError("R3R12_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if not (root / ".git").exists():
        raise RuntimeError("R3R12_GIT_REPOSITORY_REQUIRED")
    if _read_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R12_DEVELOP_REQUIRED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R12_R3R9_REQUIRED")
    if not (root / "phase175_r3r11_cited_hopf_narrative" / "run.ps1").is_file():
        raise RuntimeError("R3R12_R3R11_REQUIRED")
    prior_projection = (root / "phase175_r3r11_cited_hopf_narrative" / "projection.py")
    normalized, _ = install._canonical(prior_projection.read_bytes())
    current_blob = install.git_blob_sha(normalized)
    plan = install.plan_patch(root)
    return {
        "head": _read_git(root, "rev-parse", "HEAD"),
        "reviewed_blob": current_blob,
        "plan": plan,
    }


def _public_gate() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    recorded = inspect_one_group(3, 4)
    previous = verify_public_result(recorded)
    markdown = recorded.get("markdown")
    if not isinstance(markdown, str) or markdown.count("\n証明\n") != 1:
        raise RuntimeError("R3R12_PUBLIC_MARKDOWN_MISSING")
    references, body = markdown.split("\n証明\n", 1)
    if (recorded.get("web_key") != "generic-complete-proof"
            or recorded.get("trust_verified") is not True
            or recorded.get("reference_count") != 7
            or previous["search_status"] != "complete"
            or previous["lemma54_used"] is not False):
        raise RuntimeError("R3R12_PROOF_OR_TRUST_CHANGED")
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    surjective = "よって, $H$ は全射."
    isomorphism = "よって, $H$ は同型."
    if (body.count(summary) != 1 or body.count(conclusion) != 1
            or body.count("以上より, " + conclusion) != 1
            or body.count(surjective) != 1 or body.count(isomorphism) != 1
            or "の生成元であり" in body or "すでに $H$ は単射なので" in body
            or not (body.index(summary) < body.index(surjective)
                    < body.index(isomorphism)
                    < body.index("以上より, " + conclusion))):
        raise RuntimeError("R3R12_SINGLE_CONCLUSION_OR_HOPF_EXPLANATION_FAILED")
    if (r"$E(\eta_2\nu')=0$." not in references
            or r"$H(\alpha E\beta)=H(\alpha) E\beta$." not in references
            or "特に, " in references or "右合成公式: " in references):
        raise RuntimeError("R3R12_OLDER_REFERENCE_BODIES_CHANGED")
    return {
        "search": previous["search_status"],
        "web": recorded["web_key"],
        "trust": recorded["trust_verified"],
        "reference_count": recorded["reference_count"],
        "lemma54_used": previous["lemma54_used"],
        "hopf_summary": summary,
        "hopf_surjective": surjective,
        "hopf_isomorphism": isomorphism,
        "final_conclusion": "以上より, " + conclusion,
        "final_conclusion_count": body.count(conclusion),
        "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = root.resolve()
    checked = preflight(root)
    plan = checked["plan"]
    label = "PHASE175_R3R12R4_"
    print(label + "BRANCH=develop")
    print(label + "HEAD=" + checked["head"])
    print(label + "REVIEWED_BLOB=" + checked["reviewed_blob"])
    print(label + "PATCH_STATUS=" + plan.status)
    print(label + "NEW_GIVEN=0")
    print(label + "NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print(label + "GATE=PASS_R3R12R4_READ_ONLY_DRYRUN")
        return 0

    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / "phase175_r3r12r4_hopf_conclusion")
    folder.mkdir(parents=True, exist_ok=True)
    target = root / install.TARGET
    if plan.status == "PATCH_REQUIRED":
        (folder / "r3r11_projection_backup.py").write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        environment = dict(os.environ)
        environment.update(
            PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
        )
        command = [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
            *TEST_PATHS,
        ]
        result = subprocess.run(
            command, cwd=root, env=environment, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=timeout_seconds, check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            result.stdout + "\n" + result.stderr, encoding="utf-8",
        )
        print(result.stdout[-6000:])
        if result.returncode:
            raise RuntimeError("R3R12_FOCUSED_PYTEST_FAILED")
        print(label + "FOCUSED_PYTEST=PASS")
        public = _public_gate()
        (folder / "report.json").write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "head": checked["head"],
            "before_sha256": sha256(plan.old_bytes).hexdigest(),
            "after_sha256": sha256(target.read_bytes()).hexdigest(),
            "public": public,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        for key, value in public.items():
            print(label + key.upper() + "=" + str(value))
        print(label + "GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print(label + "ROLLBACK=RESTORED")
            else:
                print(label + "ROLLBACK=MANUAL_INSPECTION_REQUIRED")
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
        print("PHASE175_R3R12R4_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
