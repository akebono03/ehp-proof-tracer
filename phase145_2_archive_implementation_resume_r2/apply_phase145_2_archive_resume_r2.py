from __future__ import annotations

import csv
import subprocess
from pathlib import Path

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
EXPECTED_ARTIFACTS = 553
EXPECTED_TRACKED_FILES = 1811

STAGE1_CSV = Path(
    "phase145_2_stage1_archiving_audit/output/"
    "phase145_2_stage1_archiving_audit.csv"
)
PACKAGE_PREFIX = "phase145_2_archive_implementation_resume_r2/"
ALLOWED_LOCAL_PREFIXES = (
    "archive/phases/",
    "phase145_2_stage1_archiving_audit/",
    "phase145_2_stage2_relative_path_risk_refinement/",
    "phase145_2_stage3_historical_executability_classification/",
    "phase145_2_stage4_dependency_chain_refinement/",
    "phase145_2_stage5_unresolved_token_final_classification/",
    "phase145_2_archive_implementation/",
    PACKAGE_PREFIX,
)
ARCHIVE_ROOT = Path("archive/phases")
ROOT_FILES_DIR = ARCHIVE_ROOT / "_root_files"


def run(
    *args: str,
    capture: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(args),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
    )
    if check and result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.stderr:
            print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


def git(*args: str) -> str:
    return run("git", *args).stdout


def tracked_paths() -> list[str]:
    return [
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    ]


def load_stage1_population() -> list[dict[str, str]]:
    if not STAGE1_CSV.is_file():
        raise RuntimeError(f"Stage 1 CSV not found: {STAGE1_CSV}")
    with STAGE1_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != EXPECTED_ARTIFACTS:
        raise RuntimeError(
            f"Expected {EXPECTED_ARTIFACTS} Stage 1 artifacts, found {len(rows)}."
        )
    return rows


def destination_for(artifact: str, kind: str) -> Path:
    if kind == "root_file":
        return ROOT_FILES_DIR / artifact
    if kind == "directory":
        return ARCHIVE_ROOT / artifact
    raise RuntimeError(f"Unknown artifact kind for {artifact}: {kind}")


def original_members_from_head(artifact: str, kind: str) -> list[str]:
    if kind == "root_file":
        result = run(
            "git", "ls-tree", "-r", "--name-only", "HEAD", "--", artifact
        ).stdout.splitlines()
        return [p.replace("\\", "/") for p in result if p.strip()]

    prefix = artifact.rstrip("/") + "/"
    result = run(
        "git", "ls-tree", "-r", "--name-only", "HEAD", "--", artifact
    ).stdout.splitlines()
    return [
        p.replace("\\", "/")
        for p in result
        if p.replace("\\", "/").startswith(prefix)
    ]


def expected_destination_members(
    artifact: str,
    kind: str,
    destination: Path,
    original_members: list[str],
) -> list[str]:
    if kind == "root_file":
        return [destination.as_posix()]
    prefix = artifact.rstrip("/") + "/"
    return [
        (destination / member[len(prefix):]).as_posix()
        for member in original_members
    ]


def preflight_worktree() -> None:
    rows = load_stage1_population()
    audited_sources = {row["artifact"] for row in rows}

    def is_allowed_source(path: str) -> bool:
        for artifact in audited_sources:
            if path == artifact or path.startswith(artifact.rstrip("/") + "/"):
                return True
        return any(path.startswith(prefix) for prefix in ALLOWED_LOCAL_PREFIXES)

    def is_allowed_destination(path: str) -> bool:
        return any(path.startswith(prefix) for prefix in ALLOWED_LOCAL_PREFIXES)

    unexpected: list[str] = []
    for line in git("status", "--porcelain").splitlines():
        if not line.strip():
            continue

        status = line[:2]
        path = line[3:].replace("\\", "/")

        if " -> " in path:
            old, new = path.split(" -> ", 1)
            # A staged rename is valid when the source belongs to the exact
            # Stage 1 audited population and the destination is under the
            # Phase 145-2 archive/package boundary.
            if not (is_allowed_source(old) and is_allowed_destination(new)):
                unexpected.append(line)
            continue

        if not is_allowed_destination(path):
            unexpected.append(line)

    if unexpected:
        raise RuntimeError(
            "Working tree contains changes outside the audited Phase 145-2 "
            "archive operation:\n"
            + "\n".join(unexpected[:80])
        )


def classify_state(
    artifact: str,
    kind: str,
    destination: Path,
    original_members: list[str],
    current_tracked: set[str],
) -> str:
    expected_dest = expected_destination_members(
        artifact, kind, destination, original_members
    )

    source_tracked = [p for p in original_members if p in current_tracked]
    dest_tracked = [p for p in expected_dest if p in current_tracked]

    source_exists = Path(artifact).exists()
    dest_exists = destination.exists()

    if (
        len(source_tracked) == len(original_members)
        and not dest_tracked
        and source_exists
        and not dest_exists
    ):
        return "PENDING"

    if (
        not source_tracked
        and len(dest_tracked) == len(expected_dest)
        and not source_exists
        and dest_exists
    ):
        return "ALREADY_MOVED"

    raise RuntimeError(
        "Ambiguous partial state for artifact:\n"
        f"  artifact={artifact}\n"
        f"  source_exists={source_exists}\n"
        f"  destination_exists={dest_exists}\n"
        f"  source_tracked={len(source_tracked)}/{len(original_members)}\n"
        f"  destination_tracked={len(dest_tracked)}/{len(expected_dest)}"
    )


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        raise RuntimeError("Run this script from the repository root.")

    head = git("rev-parse", "HEAD").strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        raise RuntimeError(
            "HEAD differs from the Phase 145-2 audited baseline."
        )

    preflight_worktree()
    rows = load_stage1_population()

    plan = []
    original_total = 0
    current_tracked = set(tracked_paths())

    for row in rows:
        artifact = row["artifact"]
        kind = row["kind"]
        destination = destination_for(artifact, kind)
        original_members = original_members_from_head(artifact, kind)
        if not original_members:
            raise RuntimeError(
                f"Artifact is missing from baseline HEAD: {artifact}"
            )
        original_total += len(original_members)
        state = classify_state(
            artifact,
            kind,
            destination,
            original_members,
            current_tracked,
        )
        plan.append(
            (artifact, kind, destination, original_members, state)
        )

    if original_total != EXPECTED_TRACKED_FILES:
        raise RuntimeError(
            f"Expected {EXPECTED_TRACKED_FILES} baseline tracked files, "
            f"found {original_total}."
        )

    moved_count = sum(1 for item in plan if item[4] == "ALREADY_MOVED")
    pending_count = sum(1 for item in plan if item[4] == "PENDING")

    print(f"Audited artifacts: {len(plan)}")
    print(f"Baseline tracked files: {original_total}")
    print(f"Already moved artifacts: {moved_count}")
    print(f"Pending artifacts: {pending_count}")
    print("Resume preflight: PASS")
    print("")
    print("Continuing archive move...")

    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    ROOT_FILES_DIR.mkdir(parents=True, exist_ok=True)

    newly_moved = 0
    for artifact, _kind, destination, _members, state in plan:
        if state == "ALREADY_MOVED":
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        print(f"MOVE {artifact} -> {destination.as_posix()}")
        result = run(
            "git",
            "mv",
            "--",
            artifact,
            destination.as_posix(),
            check=False,
        )
        if result.returncode != 0:
            print("")
            print("git mv FAILED")
            print(f"artifact: {artifact}")
            print(f"destination: {destination.as_posix()}")
            print(f"return code: {result.returncode}")
            if result.stdout:
                print("--- git stdout ---")
                print(result.stdout)
            if result.stderr:
                print("--- git stderr ---")
                print(result.stderr)
            raise RuntimeError(
                f"git mv failed for {artifact}; partial progress is preserved."
            )
        newly_moved += 1

    readme_source = Path(PACKAGE_PREFIX) / "ARCHIVE_README.md"
    readme_destination = ARCHIVE_ROOT / "README.md"
    if not readme_source.is_file():
        raise RuntimeError(f"Archive README source missing: {readme_source}")

    if not readme_destination.exists():
        readme_destination.write_text(
            readme_source.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        run("git", "add", "--", readme_destination.as_posix())
    else:
        existing = readme_destination.read_text(
            encoding="utf-8", errors="replace"
        )
        desired = readme_source.read_text(encoding="utf-8")
        if existing != desired:
            raise RuntimeError(
                "archive/phases/README.md already exists with different content."
            )
        run("git", "add", "--", readme_destination.as_posix())

    final_tracked = set(tracked_paths())
    missing = []
    lingering = []
    verified_files = 0

    for artifact, kind, destination, original_members, _state in plan:
        expected = expected_destination_members(
            artifact, kind, destination, original_members
        )
        for source in original_members:
            if source in final_tracked:
                lingering.append(source)
        for dest in expected:
            if dest not in final_tracked:
                missing.append(dest)
            else:
                verified_files += 1

    if lingering:
        raise RuntimeError(
            "Original tracked paths remain:\n" + "\n".join(lingering[:80])
        )
    if missing:
        raise RuntimeError(
            "Archive tracked paths are missing:\n" + "\n".join(missing[:80])
        )
    if verified_files != EXPECTED_TRACKED_FILES:
        raise RuntimeError(
            f"Verified {verified_files} archived historical files; "
            f"expected {EXPECTED_TRACKED_FILES}."
        )

    print("")
    print("=" * 78)
    print("Phase 145-2 resumable archive move verification: PASS")
    print(f"Artifacts already moved before resume: {moved_count}")
    print(f"Artifacts newly moved: {newly_moved}")
    print(f"Artifacts verified in archive: {len(plan)}")
    print(f"Historical tracked files verified: {verified_files}")
    print("Archive README: archive/phases/README.md")
    print("Production code changes: none")
    print("Canonical test changes: none")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
