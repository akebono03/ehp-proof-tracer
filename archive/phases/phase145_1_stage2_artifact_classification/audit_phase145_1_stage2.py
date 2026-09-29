from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

EXPECTED_HEAD = "3bcb84fe687ace64f15859df1f9dcb5da7113266"
SELF_DIRS = {
    "phase145_1_repository_cleanup",
    "phase145_1_stage2_artifact_classification",
}
CANONICAL_PREFIXES = (
    "tests/",
    "docs/development_log/",
    "docs/proof_records/",
)
CANONICAL_DOCS = {
    "README.md",
    "docs/code_reference.md",
    "docs/design.md",
    "docs/development_log.md",
    "docs/proof_records.md",
    "docs/roadmap.md",
}
BACKUP_RE = re.compile(
    r"(?:^|/)\.phase\d.*_backup/|"
    r"\.before_phase|"
    r"(?:^|[._])phase\d.*_backup(?:$|[._/])|"
    r"\.bak$",
    re.IGNORECASE,
)
PHASE_DIR_RE = re.compile(r"^phase\d", re.IGNORECASE)
PHASE_ROOT_FILE_RE = re.compile(
    r"^(?:PHASE\d.*(?:README|INSTRUCTIONS)|"
    r"(?:apply|audit|diagnose|inspect|check|find)_phase\d.*)\.(?:py|ps1|txt|md)$",
    re.IGNORECASE,
)
OUTPUT_LIKE_RE = re.compile(
    r"(?:audit_output|diagnosis|diagnostic|report|snapshot|comparison|"
    r"inventory|inspection|inspect|analysis_output)",
    re.IGNORECASE,
)
CODE_EXTENSIONS = {".py", ".ps1", ".sh", ".bat", ".cmd"}
TEXT_EXTENSIONS = CODE_EXTENSIONS | {".txt", ".md", ".json", ".csv", ".html", ".css", ".js"}


@dataclass
class Artifact:
    path: str
    kind: str
    files: list[str]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def git_lines(*args: str) -> list[str]:
    result = run_git(*args)
    return [line for line in result.stdout.splitlines() if line.strip()]


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def is_first_stage_backup(path: str) -> bool:
    return bool(BACKUP_RE.search(normalize(path)))


def is_canonical(path: str) -> bool:
    p = normalize(path)
    if p in CANONICAL_DOCS:
        return True
    if p.startswith(CANONICAL_PREFIXES):
        return True
    first = p.split("/", 1)[0]
    if "/" not in p and not PHASE_ROOT_FILE_RE.match(first):
        return True
    if p.startswith(("templates/", "static/")):
        return True
    return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_artifacts(tracked: list[str]) -> list[Artifact]:
    phase_dirs: dict[str, list[str]] = {}
    root_files: list[Artifact] = []

    for raw in tracked:
        p = normalize(raw)
        if is_first_stage_backup(p):
            continue
        first = p.split("/", 1)[0]
        if first in SELF_DIRS:
            continue
        if "/" in p and PHASE_DIR_RE.match(first):
            phase_dirs.setdefault(first, []).append(p)
        elif "/" not in p and PHASE_ROOT_FILE_RE.match(p):
            root_files.append(Artifact(path=p, kind="root_phase_file", files=[p]))

    result = [
        Artifact(path=name, kind="phase_directory", files=sorted(files))
        for name, files in sorted(phase_dirs.items())
    ]
    result.extend(sorted(root_files, key=lambda x: x.path.lower()))
    return result


def canonical_text_files(tracked: list[str]) -> list[str]:
    result = []
    for p in tracked:
        p = normalize(p)
        if is_first_stage_backup(p):
            continue
        if is_canonical(p) and Path(p).suffix.lower() in TEXT_EXTENSIONS:
            result.append(p)
    return sorted(result)


def artifact_text_files(artifacts: list[Artifact]) -> list[str]:
    result = []
    for artifact in artifacts:
        for p in artifact.files:
            if Path(p).suffix.lower() in TEXT_EXTENSIONS:
                result.append(p)
    return sorted(set(result))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def build_text_cache(files: list[str], root: Path) -> dict[str, str]:
    return {
        p: read_text(root / p).lower()
        for p in files
    }


def build_reference_index(
    artifact_names: list[str],
    text_cache: dict[str, str],
) -> dict[str, list[str]]:
    index = {name: [] for name in artifact_names}
    lowered_names = [(name, name.lower()) for name in artifact_names]
    for path, text in text_cache.items():
        for name, needle in lowered_names:
            if needle in text:
                index[name].append(path)
    return index


def canonical_hash_index(tracked: list[str], root: Path) -> dict[tuple[str, str], list[str]]:
    index: dict[tuple[str, str], list[str]] = {}
    for p in tracked:
        p = normalize(p)
        if not is_canonical(p):
            continue
        path = root / p
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in TEXT_EXTENSIONS:
            continue
        key = (path.name.lower(), sha256(path))
        index.setdefault(key, []).append(p)
    return index


def duplicate_status(artifact: Artifact, root: Path, index: dict[tuple[str, str], list[str]]) -> tuple[int, int, list[str]]:
    relevant = []
    matches = []
    for p in artifact.files:
        path = root / p
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in TEXT_EXTENSIONS:
            continue
        if path.name.lower() in {"readme.txt", "readme.md"}:
            continue
        if path.name.lower().startswith(("run_", "apply_")):
            continue
        relevant.append(p)
        key = (path.name.lower(), sha256(path))
        if key in index:
            matches.append(p)
    return len(relevant), len(matches), matches


def classify(
    artifact: Artifact,
    root: Path,
    canonical_reference_index: dict[str, list[str]],
    artifact_reference_index: dict[str, list[str]],
    index: dict[tuple[str, str], list[str]],
) -> dict[str, str]:
    name = artifact.path
    canonical_refs = canonical_reference_index.get(name, [])
    artifact_refs = [
        p
        for p in artifact_reference_index.get(name, [])
        if not (p == name or p.startswith(name + "/"))
    ]

    files = artifact.files
    has_apply = any(Path(p).name.lower().startswith("apply_") for p in files)
    has_run = any(Path(p).name.lower().startswith("run_") for p in files)
    has_payload = any("/payload/" in normalize(p).lower() for p in files)
    has_test = any(
        "/tests/" in ("/" + normalize(p).lower())
        or Path(p).name.lower().startswith("test_")
        for p in files
    )
    output_like = bool(OUTPUT_LIKE_RE.search(name))
    relevant_count, duplicate_count, duplicate_files = duplicate_status(artifact, root, index)
    all_relevant_duplicated = relevant_count > 0 and relevant_count == duplicate_count

    if canonical_refs:
        category = "C_SAVE"
        reason = "canonical production/test/docs directly reference this artifact name"
    elif output_like and not has_apply and not has_payload and not has_test:
        category = "A_SAFE_DELETE"
        reason = "output-like artifact; no canonical reference; no apply/payload/test content"
    elif all_relevant_duplicated and not has_apply:
        category = "A_SAFE_DELETE"
        reason = "all relevant text/code payload is byte-identical to canonical files; no canonical reference"
    else:
        category = "B_REVIEW"
        reasons = []
        if has_apply:
            reasons.append("contains apply script")
        if has_payload:
            reasons.append("contains payload")
        if has_test:
            reasons.append("contains test material")
        if artifact_refs:
            reasons.append("referenced by another phase artifact")
        if relevant_count and not all_relevant_duplicated:
            reasons.append("contains unique text/code content")
        if not reasons:
            reasons.append("not proven safe by conservative rules")
        reason = "; ".join(reasons)

    return {
        "category": category,
        "path": name,
        "kind": artifact.kind,
        "file_count": str(len(files)),
        "has_apply": str(has_apply),
        "has_run": str(has_run),
        "has_payload": str(has_payload),
        "has_test": str(has_test),
        "output_like": str(output_like),
        "canonical_reference_count": str(len(canonical_refs)),
        "canonical_references": " | ".join(canonical_refs),
        "artifact_reference_count": str(len(artifact_refs)),
        "artifact_references": " | ".join(artifact_refs[:20]),
        "relevant_text_code_count": str(relevant_count),
        "canonical_duplicate_count": str(duplicate_count),
        "canonical_duplicate_files": " | ".join(duplicate_files[:20]),
        "reason": reason,
    }


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        print("STOP: run this from the repository root.")
        return 2

    head = run_git("rev-parse", "HEAD").stdout.strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        print("NOTE: local HEAD differs from the GitHub develop SHA used to design this audit.")
        print("      Classification will still run against the current local tracked tree.")

    tracked = git_lines("ls-files")
    artifacts = collect_artifacts(tracked)
    canonical_files = canonical_text_files(tracked)
    phase_text_files = artifact_text_files(artifacts)
    index = canonical_hash_index(tracked, root)

    print(f"Tracked files visible locally: {len(tracked)}")
    print(f"Phase artifacts to classify: {len(artifacts)}")
    print(f"Canonical text/code files scanned for references: {len(canonical_files)}")

    artifact_names = [a.path for a in artifacts]

    print("Building canonical text cache (single read per file)...")
    canonical_cache = build_text_cache(canonical_files, root)
    print("Building Phase-artifact text cache (single read per file)...")
    artifact_cache = build_text_cache(phase_text_files, root)

    print("Indexing canonical references...")
    canonical_reference_index = build_reference_index(
        artifact_names,
        canonical_cache,
    )
    print("Indexing Phase-artifact references...")
    artifact_reference_index = build_reference_index(
        artifact_names,
        artifact_cache,
    )

    rows = [
        classify(
            a,
            root,
            canonical_reference_index,
            artifact_reference_index,
            index,
        )
        for a in artifacts
    ]
    rows.sort(key=lambda r: (r["category"], r["path"].lower()))

    out_dir = root / "phase145_1_stage2_artifact_classification" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys()) if rows else [
        "category", "path", "kind", "file_count", "reason"
    ]
    csv_path = out_dir / "phase145_1_stage2_classification.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    counts = {
        "A_SAFE_DELETE": sum(r["category"] == "A_SAFE_DELETE" for r in rows),
        "B_REVIEW": sum(r["category"] == "B_REVIEW" for r in rows),
        "C_SAVE": sum(r["category"] == "C_SAVE" for r in rows),
    }

    txt_path = out_dir / "phase145_1_stage2_summary.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-1 Stage 2 Phase Artifact Classification\n")
        f.write("=" * 72 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Artifacts: {len(rows)}\n")
        for key, value in counts.items():
            f.write(f"{key}: {value}\n")
        f.write("\nA_SAFE_DELETE\n")
        f.write("-" * 72 + "\n")
        for r in rows:
            if r["category"] == "A_SAFE_DELETE":
                f.write(f"{r['path']} :: {r['reason']}\n")
        f.write("\nC_SAVE\n")
        f.write("-" * 72 + "\n")
        for r in rows:
            if r["category"] == "C_SAVE":
                f.write(f"{r['path']} :: {r['reason']}\n")
        f.write("\nB_REVIEW\n")
        f.write("-" * 72 + "\n")
        for r in rows:
            if r["category"] == "B_REVIEW":
                f.write(f"{r['path']} :: {r['reason']}\n")

    print("=" * 72)
    print("Classification complete")
    print(f"A_SAFE_DELETE: {counts['A_SAFE_DELETE']}")
    print(f"B_REVIEW:      {counts['B_REVIEW']}")
    print(f"C_SAVE:        {counts['C_SAVE']}")
    print("=" * 72)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No files were deleted or modified by this audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
