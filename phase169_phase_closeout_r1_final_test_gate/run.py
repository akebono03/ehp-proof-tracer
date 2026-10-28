"""Phase 169 closeout: verify exact reviewed sources and run end-of-phase pytest.

This is the END-OF-PHASE test runner. It writes evidence outside the checkout,
never stages files and never updates production code or documentation.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any

sys.dont_write_bytecode = True

# Git object ids were read from the public develop commit 6e5d6bb (2026-10-28).
# These are file-level contracts, not a frozen HEAD: an audit-only follow-up
# commit can be accepted if the same reviewed bytes are still present.
REVIEWED_BLOBS = {
    "README.md": "c2c2c9236fdee03686518d05fa0ca7367b044a3b",
    "docs/design.md": "39f859dfe8a0ee208509efcb4dae7dc126812993",
    "docs/development_log.md": "9a68123a59d6acb2845ffc376aabc164a0102b45",
    "docs/roadmap.md": "0f5314a479a3549e99844ff8e0a94a4cf117023c",
    "docs/proof_records.md": "a993629e7ad2d4883f2c0d3e272eef47dcf29b9a",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": "daad1b7b246c4b005bd529637f82e64ce85a9cfe",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": "f0664c1e28793f5a3ab341b17eb5e7ded0724436",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": "9038d656aac21311a5272e4d62551cce435037c3",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": "65f65b5bacdbec9cc4257b2c96140720568097a3",
    "phase169_r10et_r6_residual_definition_dependency_audit/audit.py": "ae883ad6ec24382dfc4bac26790a4a2b7e8fa54e",
}

R6_EVIDENCE = "phase169_r10et_r6_residual_definition_dependency_audit/output/20261028_174644_215/audit.json"
R6_EVIDENCE_BLOB = "e00cb348d59679919189fab761025e0be9ca05dc"

REQUIRED = frozenset((
    "pi_69^43", "pi_56^30", "pi_41^30", "pi_44^30", "pi_46^30", "pi_39^30",
    "pi_3^2", "pi_4^3", "pi_5^4", "pi_4^2", "pi_5^3", "pi_6^4",
    "pi_28^22", "pi_32^22", "pi_23^15", "pi_33^24",
))
PROBES = frozenset(("pi_10^8", "pi_22^13", "pi_24^15"))

# Concrete regression tests checked in the public repository on 2026-10-28.
# This list is an additional, selected Phase 169 regression; it does not
# imply that every historical phase169_*/tests file is an active contract.
FOCUSED_TESTS = (
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py",
    "phase169_r10et_r6c_root_reachable_citations/tests/test_r6c_root_citations.py",
    "phase169_r10et_r6_residual_definition_dependency_audit/tests/test_r6_helpers.py",
    "phase169_r10et_r5d_staged_audit_guard/tests/test_r5_live.py",
    "phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py",
    "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_live.py",
    "phase168_r3_41p19_phase_closeout/tests/test_phase168_r3_41p19_phase_closeout.py",
)


def git(root: Path, *args: str) -> str:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    environment["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *args],
        capture_output=True, timeout=50, check=False, env=environment,
    )
    if result.returncode:
        raise RuntimeError(
            f"git {args!r} returned {result.returncode}: "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def snapshot(root: Path) -> tuple[str, str, str]:
    return (
        git(root, "rev-parse", "HEAD"),
        git(root, "diff", "--name-only"),
        git(root, "diff", "--cached", "--name-only"),
    )


def inspect_r6(data: dict[str, Any]) -> tuple[int, int]:
    """Check previous 19-case evidence, without treating it as a new proof."""
    if not isinstance(data, dict) or any(data.get(key) is not True for key in (
        "source_verified", "tracked_unchanged", "required_pass", "probes_pass",
    )) or data.get("full_pytest_run") is not False:
        raise ValueError("R6 certification flags do not match reviewed evidence")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 19:
        raise ValueError("R6 evidence must have exactly 19 cases")
    names = set()
    required = set()
    probes = set()
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("case"), str):
            raise ValueError("Malformed R6 case")
        name = case["case"]
        if name in names:
            raise ValueError("Duplicate R6 case: " + name)
        names.add(name)
        (required if case.get("required") is True else probes).add(name)
        if not (
            case.get("passed") is True and case.get("status") == "complete"
            and case.get("trust") == "PASS"
            and case.get("remaining_eligible_cited_steps") == 0
            and case.get("problems") == []
        ):
            raise ValueError("Unverified R6 case: " + name)
    if required != REQUIRED or probes != PROBES:
        raise ValueError("R6 case inventory differs from reviewed evidence")
    pi108 = next(x for x in cases if x["case"] == "pi_10^8")
    if not (pi108.get("eligible_image_steps") == 4
            and pi108.get("canonical_image_steps") == 4
            and pi108.get("reference_locators") == [
                "DB prior: sphere.csv (n=4, k=2) [参考: Proposition 5.3]", "(4.5)",
            ]):
        raise ValueError("Detached pi_10^8 citation or Definition regression")
    return len(required), len(probes)


def inspect_environment(root: Path) -> tuple[str, str, str]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Phase 169 closure requires the develop branch")
    original = snapshot(root)
    if original[1] or original[2]:
        raise RuntimeError("Tracked staged/unstaged changes must be reviewed first")
    head = original[0]
    if git(root, "rev-parse", "refs/remotes/origin/develop") != head:
        raise RuntimeError("Local develop and origin/develop differ")
    remote = git(root, "ls-remote", "origin", "refs/heads/develop")
    if remote != head + "\trefs/heads/develop":
        raise RuntimeError("Remote develop changed: synchronize and recheck first")
    for path, expected in {**REVIEWED_BLOBS, R6_EVIDENCE: R6_EVIDENCE_BLOB}.items():
        if not (root / path).is_file():
            raise RuntimeError("Missing reviewed file: " + path)
        committed = git(root, "rev-parse", "HEAD:" + path)
        observed = git(root, "hash-object", "--path=" + path, path)
        if committed != expected or observed != expected:
            raise RuntimeError("Unreviewed source/document/evidence: " + path)
    for path in FOCUSED_TESTS:
        if not (root / path).is_file():
            raise RuntimeError("Missing focused test: " + path)
    if not (root / "tests" / "conftest.py").is_file():
        raise RuntimeError("Missing active tests/conftest.py")
    return original


def passed_count(output: str, exit_code: int) -> int | None:
    if exit_code != 0:
        return None
    matched = re.findall(r"(?:^|\s)(\d+) passed(?:,| in )", output)
    return int(matched[-1]) if matched else None


def execute_pytest(root: Path, report_dir: Path, label: str,
                   paths: tuple[str, ...]) -> dict[str, Any]:
    command = [
        sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
        "--disable-warnings", "-p", "no:cacheprovider", *paths,
    ]
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    environment.pop("PYTEST_ADDOPTS", None)
    logfile = report_dir / (label + "_pytest.log")
    print("PHASE169_CLOSEOUT_R1_" + label.upper() + "_PYTEST_START", flush=True)
    print("PHASE169_CLOSEOUT_R1_" + label.upper() + "_COMMAND=" + " ".join(command), flush=True)
    with logfile.open("w", encoding="utf-8", newline="\n") as out:
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            cwd=root, env=environment,
        )
        assert proc.stdout is not None
        for raw in proc.stdout:
            line = raw.decode("utf-8", "replace")
            out.write(line)
            print(line, end="", flush=True)
        exit_code = proc.wait()
    output = logfile.read_text(encoding="utf-8")
    count = passed_count(output, exit_code)
    result = {
        "command": command, "exit_code": exit_code, "passed_count": count,
        "log": str(logfile),
    }
    print(f"PHASE169_CLOSEOUT_R1_{label.upper()}_PYTEST_EXIT={exit_code}", flush=True)
    print(f"PHASE169_CLOSEOUT_R1_{label.upper()}_PASSED={count if count is not None else 'UNVERIFIED'}", flush=True)
    return result


def write_report(report_dir: Path, report: dict[str, Any]) -> Path:
    report_path = report_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report_path


def execute(root: Path) -> int:
    original = inspect_environment(root)
    evidence = json.loads((root / R6_EVIDENCE).read_text(encoding="utf-8"))
    mandatory, optional = inspect_r6(evidence)
    if (mandatory, optional) != (16, 3):
        raise RuntimeError("R6 evidence coverage changed")
    localappdata = os.environ.get("LOCALAPPDATA")
    if not localappdata:
        raise RuntimeError("LOCALAPPDATA is required for safe external output")
    output_root = Path(localappdata) / "EHPProofTracerRecovery"
    if output_root.resolve() == root.resolve() or root.resolve() in output_root.resolve().parents:
        raise RuntimeError("Output must be outside the Git checkout")
    report_dir = output_root / ("phase169_closeout_r1_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    report_dir.mkdir(parents=True, exist_ok=False)
    report: dict[str, Any] = {
        "mode": "PHASE169_END_OF_PHASE_TEST", "head": original[0],
        "reviewed_files": len(REVIEWED_BLOBS), "r6_cases": mandatory + optional,
        "focused": None, "active_full": None,
        "git_index_preserved": False, "phase169_certified": False,
    }
    try:
        report["focused"] = execute_pytest(root, report_dir, "focused", FOCUSED_TESTS)
        if report["focused"]["passed_count"] is not None:
            report["active_full"] = execute_pytest(root, report_dir, "active_full", ("tests",))
        else:
            print("PHASE169_CLOSEOUT_R1_ACTIVE_FULL_SKIPPED=FOCUSED_FAILURE", flush=True)
        unchanged = snapshot(root) == original
        report["git_index_preserved"] = unchanged
        verified = bool(
            unchanged and report["focused"]["passed_count"] is not None
            and report["active_full"] is not None
            and report["active_full"]["passed_count"] is not None
        )
        report["phase169_test_gate_pass"] = verified
        # The phase itself is not closed until the test report is reviewed,
        # required documents are updated and its closure is explicitly recorded.
        report["phase169_certified"] = False
        report["decision"] = (
            "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION" if verified
            else "TEST_GATE_FAILED_REVIEW_REQUIRED"
        )
        print("PHASE169_CLOSEOUT_R1_GIT_INDEX_PRESERVED=" + str(unchanged), flush=True)
        print("PHASE169_CLOSEOUT_R1_TEST_GATE_PASS=" + str(verified), flush=True)
        print("PHASE169_CLOSEOUT_R1_DECISION=" + report["decision"], flush=True)
        print("PHASE169_CLOSEOUT_R1_REPORT=" + str(write_report(report_dir, report)), flush=True)
        print("PHASE169_CLOSEOUT_R1_EXIT=" + ("0" if verified else "1"), flush=True)
        return 0 if verified else 1
    except BaseException:
        report["error"] = traceback.format_exc()
        print("PHASE169_CLOSEOUT_R1_ERROR=" + report["error"], flush=True)
        print("PHASE169_CLOSEOUT_R1_REPORT=" + str(write_report(report_dir, report)), flush=True)
        print("PHASE169_CLOSEOUT_R1_EXIT=1", flush=True)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args(argv)
    print("PHASE169_CLOSEOUT_R1_MODE=PHASE_END_TEST_ONLY", flush=True)
    try:
        return execute(args.repo.resolve())
    except BaseException:
        print("PHASE169_CLOSEOUT_R1_ERROR=" + traceback.format_exc(), flush=True)
        print("PHASE169_CLOSEOUT_R1_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
