from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EXPECTED_HEAD = "3bcb84fe687ace64f15859df1f9dcb5da7113266"

TARGETS = [
    "phase112_1a_audit_output",
    "phase112_1b_audit_output",
    "phase112_1c_audit_output",
    "phase133_5_audit_output",
    "phase133_8_audit_output",
    "phase133_final_audit_output",
    "phase144_3_renderer_route_comparison_audit",
    "phase144_6_final_regression_diagnosis_r6",
    "phase144_6_final_regression_diagnosis_r7",
    "phase144_6_final_regression_repair_r9",
    "phase144_6_pi16_9_detached_definition_diagnosis_r8",
    "phase144_6_r12_compact_argument_diagnosis",
    "phase144_6_r12_compact_argument_diagnosis_r2",
    "phase144_6_r13_body_boundary_diagnosis",
    "phase144_6_r13_body_boundary_diagnosis_r2",
    "phase144_6_r13_body_boundary_diagnosis_r3",
    "phase144_6_r18_duplicate_owner_diagnosis",
    "phase144_6_r25_11_r3_two_contribution_diagnosis",
    "phase144_6_r25_18_definition_selection_diagnosis",
    "phase144_6_r25_9a_r1_r3_test_scope_fix",
    "phase144_6_r25_9b_r1_test_scope_fix",
    "phase144_6_r25_r2_rollback_owner_diagnosis",
    "phase144_6_r25_r3_rollback_owner_diagnosis",
    "phase144_6_r25_r4_git_restore_owner_diagnosis",
    "phase144_6_r25_r5_owner_diagnosis",
    "phase144_6_r25_rollback_owner_diagnosis",
    "phase144_6_r5_43_10_r2_phase_boundary_test_update",
    "phase144_6_r5_43_10_r3_direct_connector_regression_update",
]

ALLOWED_UNTRACKED_PREFIXES = (
    "?? phase145_1_repository_cleanup/",
    "?? phase145_1_stage2_artifact_classification/",
    "?? phase145_1_stage3_delete_safe_artifacts/",
)


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def status_lines() -> list[str]:
    return [
        line
        for line in run_git("status", "--short", "--untracked-files=all").stdout.splitlines()
        if line.strip()
    ]


def is_allowed_existing_change(line: str) -> bool:
    if any(line.startswith(prefix) for prefix in ALLOWED_UNTRACKED_PREFIXES):
        return True

    if not line.startswith(" D "):
        return False

    path = line[3:].replace("\\", "/")

    backup_markers = (
        ".before_phase",
        "_backup",
        ".bak",
    )
    if any(marker in path for marker in backup_markers):
        return True
    if path.startswith(".phase") and "_backup/" in path:
        return True

    return False


def tracked_files_under(target: str) -> list[str]:
    result = run_git("ls-files", "--", target)
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        print("STOP: run this from the repository root.")
        return 2

    head = run_git("rev-parse", "HEAD").stdout.strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        print("STOP: HEAD differs from the audited develop baseline.")
        print(f"Expected: {EXPECTED_HEAD}")
        return 2

    unexpected = [line for line in status_lines() if not is_allowed_existing_change(line)]
    if unexpected:
        print("STOP: unexpected working-tree changes exist:")
        for line in unexpected:
            print(line)
        return 2

    missing = []
    empty = []
    total_files = 0
    for target in TARGETS:
        if not (root / target).exists():
            missing.append(target)
            continue
        files = tracked_files_under(target)
        if not files:
            empty.append(target)
            continue
        total_files += len(files)

    if missing or empty:
        print("STOP: audited targets do not match the current working tree.")
        if missing:
            print("Missing targets:")
            for target in missing:
                print(f"  {target}")
        if empty:
            print("Targets with no tracked files:")
            for target in empty:
                print(f"  {target}")
        return 2

    print(f"Verified A_SAFE_DELETE artifacts: {len(TARGETS)}")
    print(f"Tracked files inside targets: {total_files}")
    print("")
    for target in TARGETS:
        print(target)

    if "--apply" not in sys.argv:
        print("")
        print("DRY RUN ONLY: no Phase artifacts were deleted.")
        print("Run again with --apply after reviewing the list.")
        return 0

    print("")
    print("Applying verified Phase-artifact cleanup...")
    for target in TARGETS:
        result = run_git("rm", "-r", "--", target, check=False)
        if result.returncode != 0:
            print(f"STOP: git rm failed for {target}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode

    print(f"Deleted {len(TARGETS)} audited A_SAFE_DELETE artifacts.")
    print("B_REVIEW and C_SAVE artifacts were not touched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
