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
PACKAGE_PREFIX = "phase145_2_archive_implementation/"
ALLOWED_LOCAL_PREFIXES = (
    "phase145_2_stage1_archiving_audit/",
    "phase145_2_stage2_relative_path_risk_refinement/",
    "phase145_2_stage3_historical_executability_classification/",
    "phase145_2_stage4_dependency_chain_refinement/",
    "phase145_2_stage5_unresolved_token_final_classification/",
    PACKAGE_PREFIX,
)
ARCHIVE_ROOT = Path("archive/phases")
ROOT_FILES_DIR = ARCHIVE_ROOT / "_root_files"


def run(*args: str, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout


def tracked_paths() -> list[str]:
    return [
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    ]


def members_for(artifact: str, kind: str, tracked: list[str]) -> list[str]:
    if kind == "root_file":
        return [artifact] if artifact in tracked else []
    prefix = artifact.rstrip("/") + "/"
    return [p for p in tracked if p.startswith(prefix)]


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


def preflight_worktree() -> None:
    unexpected: list[str] = []
    for line in git("status", "--porcelain").splitlines():
        if not line.strip():
            continue
        path = line[3:].replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not any(path.startswith(prefix) for prefix in ALLOWED_LOCAL_PREFIXES):
            unexpected.append(line)
    if unexpected:
        details = "\n".join(unexpected[:80])
        raise RuntimeError(
            "Working tree contains changes outside Phase 145-2 packages:\n"
            + details
        )


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        raise RuntimeError("Run this script from the repository root.")

    head = git("rev-parse", "HEAD").strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        raise RuntimeError(
            "HEAD differs from the Phase 145-2 audited baseline. "
            "Do not archive against an unaudited commit."
        )

    preflight_worktree()
    rows = load_stage1_population()
    before = tracked_paths()

    total_members = 0
    plan: list[tuple[str, str, Path, list[str]]] = []
    seen_destinations: set[str] = set()

    for row in rows:
        artifact = row["artifact"]
        kind = row["kind"]
        members = members_for(artifact, kind, before)
        if not members:
            raise RuntimeError(
                f"Tracked source for Stage 1 artifact is missing: {artifact}"
            )
        total_members += len(members)

        destination = destination_for(artifact, kind)
        destination_key = destination.as_posix().lower()
        if destination_key in seen_destinations:
            raise RuntimeError(f"Duplicate archive destination: {destination}")
        seen_destinations.add(destination_key)

        if destination.exists():
            raise RuntimeError(
                f"Archive destination already exists before move: {destination}"
            )
        plan.append((artifact, kind, destination, members))

    if total_members != EXPECTED_TRACKED_FILES:
        raise RuntimeError(
            f"Expected {EXPECTED_TRACKED_FILES} tracked files in the Stage 1 "
            f"population, found {total_members}."
        )

    print(f"Audited artifacts: {len(plan)}")
    print(f"Audited tracked files: {total_members}")
    print("Preflight: PASS")
    print("")
    print("Creating archive/phases and moving audited artifacts with git mv...")

    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    ROOT_FILES_DIR.mkdir(parents=True, exist_ok=True)

    moved = 0
    for artifact, kind, destination, _members in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        run("git", "mv", "--", artifact, destination.as_posix())
        moved += 1

    print(f"git mv artifacts completed: {moved}")

    # The README is supplied by the implementation package and copied only
    # after all historical artifacts have been moved.
    readme_source = Path(PACKAGE_PREFIX) / "ARCHIVE_README.md"
    readme_destination = ARCHIVE_ROOT / "README.md"
    if not readme_source.is_file():
        raise RuntimeError(f"Archive README source missing: {readme_source}")
    if readme_destination.exists():
        raise RuntimeError(f"Archive README already exists: {readme_destination}")
    readme_destination.write_text(
        readme_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    run("git", "add", "--", readme_destination.as_posix())

    after = tracked_paths()

    # Verify every original member has left its root-level source and exists at
    # the deterministic archive destination.
    missing_destinations: list[str] = []
    lingering_sources: list[str] = []
    archived_historical_files = 0

    for artifact, kind, destination, members in plan:
        if kind == "root_file":
            expected = [destination.as_posix()]
        else:
            prefix = artifact.rstrip("/") + "/"
            expected = [
                (destination / member[len(prefix):]).as_posix()
                for member in members
            ]

        for member in members:
            if member in after:
                lingering_sources.append(member)

        for expected_path in expected:
            if expected_path not in after:
                missing_destinations.append(expected_path)
            else:
                archived_historical_files += 1

    if lingering_sources:
        raise RuntimeError(
            "Historical source paths remain after git mv:\n"
            + "\n".join(lingering_sources[:80])
        )
    if missing_destinations:
        raise RuntimeError(
            "Expected archive paths are missing:\n"
            + "\n".join(missing_destinations[:80])
        )
    if archived_historical_files != EXPECTED_TRACKED_FILES:
        raise RuntimeError(
            "Archived historical tracked-file count mismatch: "
            f"{archived_historical_files} != {EXPECTED_TRACKED_FILES}"
        )

    # Ensure no Stage 1 artifact is still represented at the repository root.
    lingering_artifacts = []
    for artifact, kind, _destination, _members in plan:
        if kind == "root_file":
            if (root / artifact).exists():
                lingering_artifacts.append(artifact)
        else:
            if (root / artifact).exists():
                lingering_artifacts.append(artifact)
    if lingering_artifacts:
        raise RuntimeError(
            "Stage 1 artifacts still exist at repository root:\n"
            + "\n".join(lingering_artifacts[:80])
        )

    print("")
    print("=" * 78)
    print("Phase 145-2 archive move verification: PASS")
    print(f"Artifacts moved: {len(plan)}")
    print(f"Historical tracked files moved: {archived_historical_files}")
    print("Archive policy README added: archive/phases/README.md")
    print("Production code changes: none")
    print("Canonical test changes: none")
    print("=" * 78)
    print("")
    print("Git diff summary:")
    print(git("diff", "--stat", "--cached"))
    print("Ready for repository-wide pytest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
