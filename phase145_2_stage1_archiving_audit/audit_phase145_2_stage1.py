from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
TEXT_EXTENSIONS = {
    ".py", ".ps1", ".txt", ".md", ".json", ".html", ".css", ".js",
    ".yml", ".yaml", ".toml", ".ini", ".cfg",
}
PHASE_DIR_RE = re.compile(r"^phase\d", re.IGNORECASE)
ROOT_PHASE_FILE_RE = re.compile(
    r"^(?:"
    r"PHASE\d.*(?:README|INSTRUCTIONS).*\.(?:txt|md)"
    r"|(?:apply|audit|diagnose|inspect|check|find)_phase\d.*\.(?:py|ps1|txt|md)"
    r"|phase\d.*\.(?:json|txt|md|csv)"
    r")$",
    re.IGNORECASE,
)
BACKUP_RE = re.compile(
    r"(?:^\.phase\d.*_backup/|\.before_phase|\.phase\d.*_backup|\.bak$)",
    re.IGNORECASE,
)
SELF_PREFIX = "phase145_2_stage1_archiving_audit/"
ARCHIVE_PREFIX = "archive/phases/"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    ).stdout


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def is_backup(path: str) -> bool:
    return bool(BACKUP_RE.search(path))


def collect_phase_artifacts(files: list[str]) -> dict[str, list[str]]:
    artifacts: dict[str, list[str]] = defaultdict(list)
    for path in files:
        if is_backup(path) or path.startswith(ARCHIVE_PREFIX) or path.startswith(SELF_PREFIX):
            continue
        parts = path.split("/", 1)
        if len(parts) == 2 and PHASE_DIR_RE.match(parts[0]):
            artifacts[parts[0]].append(path)
        elif len(parts) == 1 and ROOT_PHASE_FILE_RE.match(path):
            artifacts[path].append(path)
    return dict(sorted(artifacts.items(), key=lambda item: item[0].lower()))


def canonical_files(files: list[str], artifact_paths: set[str]) -> list[str]:
    result = []
    for path in files:
        if path in artifact_paths:
            continue
        if is_backup(path) or path.startswith(ARCHIVE_PREFIX) or path.startswith(SELF_PREFIX):
            continue
        result.append(path)
    return result


def relative_path_markers(artifact: str, members: list[str]) -> set[str]:
    markers = {artifact, artifact + "/"}
    for member in members:
        markers.add(member)
        markers.add("./" + member)
        if "/" in member:
            markers.add(member.split("/", 1)[1])
    return {m for m in markers if len(m) >= 4}


def text_cache(root: Path, files: list[str]) -> dict[str, str]:
    cache = {}
    for path in files:
        fp = root / path
        if fp.is_file() and fp.suffix.lower() in TEXT_EXTENSIONS:
            cache[path] = read_text(fp)
    return cache


def find_external_path_refs(
    artifact: str,
    members: list[str],
    canonical_cache: dict[str, str],
) -> list[str]:
    strong = {artifact + "/", "./" + artifact + "/"}
    if len(members) == 1 and members[0] == artifact:
        strong.add(artifact)
    refs = []
    for path, text in canonical_cache.items():
        if any(marker in text for marker in strong):
            refs.append(path)
    return refs


def find_internal_relative_risk(
    artifact: str,
    members: list[str],
    artifact_cache: dict[str, str],
) -> list[str]:
    risks = []
    member_set = set(members)
    for path in members:
        text = artifact_cache.get(path, "")
        if not text:
            continue
        own_dir = PurePosixPath(path).parent
        patterns = (
            "../", "..\\", "Path.cwd()", "getcwd()", "Set-Location",
            "cd ", "PYTHONPATH", "repo_root", "repository root",
        )
        if any(p.lower() in text.lower() for p in patterns):
            risks.append(path)
            continue
        for candidate in member_set:
            rel_name = PurePosixPath(candidate).name
            if rel_name != PurePosixPath(path).name and rel_name in text:
                # Internal filename references are preserved by moving the whole
                # directory, so they are not automatically risky.
                pass
    return sorted(set(risks))


def destination_for(artifact: str) -> str:
    if "/" not in artifact and "." in artifact:
        return ARCHIVE_PREFIX + "_root_files/" + artifact
    return ARCHIVE_PREFIX + artifact + "/"


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        print("STOP: run from repository root.")
        return 2

    head = git("rev-parse", "HEAD").strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        print("STOP: HEAD differs from Phase 145-2 audited baseline.")
        return 2

    status = git("status", "--porcelain")
    unexpected = []
    for line in status.splitlines():
        if not line.strip():
            continue
        path = line[3:].replace("\\", "/")
        if path.startswith(SELF_PREFIX):
            continue
        unexpected.append(line)
    if unexpected:
        print("STOP: working tree contains changes outside this audit package:")
        for line in unexpected[:40]:
            print(line)
        return 2

    files = [p.replace("\\", "/") for p in git("ls-files").splitlines() if p.strip()]
    artifacts = collect_phase_artifacts(files)
    artifact_paths = {p for members in artifacts.values() for p in members}
    canonical = canonical_files(files, artifact_paths)

    print(f"Tracked files: {len(files)}")
    print(f"Phase artifacts found: {len(artifacts)}")
    print(f"Phase artifact tracked files: {len(artifact_paths)}")
    print(f"Canonical/non-Phase tracked files scanned: {len(canonical)}")
    print("Building text caches...")
    canonical_cache = text_cache(root, canonical)
    artifact_cache = text_cache(root, sorted(artifact_paths))

    rows = []
    counts = Counter()
    for artifact, members in artifacts.items():
        external_refs = find_external_path_refs(artifact, members, canonical_cache)
        internal_risks = find_internal_relative_risk(
            artifact, members, artifact_cache
        )
        destination = destination_for(artifact)
        destination_exists = (root / destination.rstrip("/")).exists()

        if external_refs:
            disposition = "MOVE_REQUIRES_CANONICAL_REFERENCE_UPDATE"
        elif destination_exists:
            disposition = "MOVE_REQUIRES_DESTINATION_REVIEW"
        elif internal_risks:
            disposition = "MOVE_REQUIRES_RELATIVE_PATH_REVIEW"
        else:
            disposition = "MOVE_SAFE_CANDIDATE"

        counts[disposition] += 1
        rows.append({
            "artifact": artifact,
            "kind": "root_file" if len(members) == 1 and members[0] == artifact else "directory",
            "tracked_file_count": len(members),
            "destination": destination,
            "disposition": disposition,
            "canonical_path_reference_count": len(external_refs),
            "relative_path_risk_count": len(internal_risks),
            "canonical_path_references": " | ".join(external_refs),
            "relative_path_risk_files": " | ".join(internal_risks),
        })

    out = root / SELF_PREFIX / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_2_stage1_archiving_audit.csv"
    txt_path = out / "phase145_2_stage1_archiving_summary.txt"

    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-2 Stage 1 - Phase Artifact Archiving Audit\n")
        f.write("=" * 78 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Artifacts analyzed: {len(rows)}\n")
        f.write(f"Tracked files represented: {len(artifact_paths)}\n\n")
        f.write("DISPOSITION COUNTS\n")
        f.write("-" * 78 + "\n")
        for key, count in sorted(counts.items()):
            f.write(f"{key}: {count}\n")

        for disposition in (
            "MOVE_REQUIRES_CANONICAL_REFERENCE_UPDATE",
            "MOVE_REQUIRES_RELATIVE_PATH_REVIEW",
            "MOVE_REQUIRES_DESTINATION_REVIEW",
            "MOVE_SAFE_CANDIDATE",
        ):
            f.write("\n" + disposition + "\n")
            f.write("-" * 78 + "\n")
            for row in rows:
                if row["disposition"] != disposition:
                    continue
                f.write(
                    f'{row["artifact"]} :: {row["kind"]} :: '
                    f'files={row["tracked_file_count"]} :: '
                    f'destination={row["destination"]}'
                )
                if row["canonical_path_reference_count"]:
                    f.write(
                        f' :: canonical_refs={row["canonical_path_reference_count"]}'
                    )
                if row["relative_path_risk_count"]:
                    f.write(
                        f' :: relative_risks={row["relative_path_risk_count"]}'
                    )
                f.write("\n")

    print("=" * 78)
    print("Phase 145-2 Stage 1 archiving audit complete - NO MOVE / NO DELETE")
    for key, count in sorted(counts.items()):
        print(f"{key}: {count}")
    print("=" * 78)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository file was moved, deleted, or modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
