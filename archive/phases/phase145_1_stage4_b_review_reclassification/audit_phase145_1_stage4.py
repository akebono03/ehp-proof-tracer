from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_HEAD = "3bcb84fe687ace64f15859df1f9dcb5da7113266"

PHASE_DIR_RE = re.compile(r"^phase\d", re.IGNORECASE)
ROOT_ARTIFACT_RE = re.compile(
    r"^(?:PHASE\d.*(?:README|INSTRUCTIONS).*\.(?:txt|md)|"
    r"(?:apply|audit|diagnose|inspect|check|find)_phase\d.*\.(?:py|ps1|txt|md))$",
    re.IGNORECASE,
)
BACKUP_RE = re.compile(
    r"(?:^\.phase\d.*_backup/|\.before_phase|\.phase\d.*_backup|\.bak$)",
    re.IGNORECASE,
)
TEXT_EXTENSIONS = {
    ".py", ".ps1", ".txt", ".md", ".json", ".html", ".css", ".js",
    ".yml", ".yaml", ".toml", ".ini", ".cfg",
}
SELF_PREFIXES = (
    "phase145_1_repository_cleanup/",
    "phase145_1_stage2_artifact_classification/",
    "phase145_1_stage3_delete_safe_artifacts/",
    "phase145_1_stage4_b_review_reclassification/",
)
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
DELETED_A_SAFE = {
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
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    ).stdout


def tracked_files() -> list[str]:
    return [
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    ]


def exists_in_worktree(root: Path, path: str) -> bool:
    return (root / path).exists()


def is_backup(path: str) -> bool:
    return bool(BACKUP_RE.search(path))


def root_name(path: str) -> str:
    return path.split("/", 1)[0]


def is_phase_artifact_file(path: str) -> bool:
    first = root_name(path)
    if PHASE_DIR_RE.match(first):
        return True
    if "/" not in path and ROOT_ARTIFACT_RE.match(path):
        return True
    return False


def is_canonical(path: str) -> bool:
    if is_backup(path) or is_phase_artifact_file(path):
        return False
    if path in CANONICAL_DOCS:
        return True
    if path.startswith(CANONICAL_PREFIXES):
        return True
    if "/" not in path:
        return True
    if path.startswith(("templates/", "static/")):
        return True
    return False


def artifact_names(files: list[str]) -> list[str]:
    names = set()
    for p in files:
        if is_backup(p):
            continue
        first = root_name(p)
        if PHASE_DIR_RE.match(first):
            if first not in DELETED_A_SAFE:
                names.add(first)
        elif "/" not in p and ROOT_ARTIFACT_RE.match(p):
            names.add(p)
    return sorted(names, key=str.lower)


def artifact_members(files: list[str], name: str) -> list[str]:
    if "/" in name or "." in name:
        return [name] if name in files else []
    prefix = name + "/"
    return [p for p in files if p.startswith(prefix)]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_reason_flags(members: list[str]) -> dict[str, bool]:
    lower = [p.lower() for p in members]
    return {
        "has_apply": any(
            Path(p).name.lower().startswith("apply") or "/apply" in p
            for p in lower
        ),
        "has_run": any(
            Path(p).name.lower().startswith("run_") for p in lower
        ),
        "has_payload": any("/payload/" in p for p in lower),
        "has_test": any(
            "/tests/" in p or Path(p).name.lower().startswith("test_")
            for p in lower
        ),
        "has_readme": any(
            Path(p).name.lower().startswith("readme") for p in lower
        ),
        "has_audit_or_diagnose": any(
            Path(p).name.lower().startswith(("audit", "diagnose", "inspect", "check"))
            for p in lower
        ),
    }


def build_duplicate_index(
    root: Path,
    canonical_files: list[str],
) -> dict[tuple[str, str], list[str]]:
    index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for p in canonical_files:
        fp = root / p
        if not fp.is_file():
            continue
        try:
            key = (Path(p).name.lower(), sha256(fp))
        except OSError:
            continue
        index[key].append(p)
    return index


def canonical_duplicate_stats(
    root: Path,
    members: list[str],
    duplicate_index: dict[tuple[str, str], list[str]],
) -> tuple[int, int, list[str]]:
    relevant = []
    duplicates = []
    for p in members:
        fp = root / p
        if not fp.is_file():
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        name = Path(p).name.lower()
        if name.startswith(("readme", "run_", "apply")):
            continue
        relevant.append(p)
        key = (name, sha256(fp))
        if duplicate_index.get(key):
            duplicates.append(p)
    return len(relevant), len(duplicates), duplicates


def build_text_cache(root: Path, files: list[str]) -> dict[str, str]:
    return {
        p: read_text(root / p).lower()
        for p in files
        if (root / p).is_file() and Path(p).suffix.lower() in TEXT_EXTENSIONS
    }


def build_reference_index(
    names: list[str],
    cache: dict[str, str],
) -> dict[str, list[str]]:
    result = {name: [] for name in names}
    lowered = [(name, name.lower()) for name in names]
    for p, text in cache.items():
        for name, needle in lowered:
            if needle in text:
                result[name].append(p)
    return result


def main() -> int:
    root = Path.cwd()
    if not (root / ".git").exists():
        print("STOP: run from repository root.")
        return 2

    head = git("rev-parse", "HEAD").strip()
    print(f"HEAD: {head}")
    if head != EXPECTED_HEAD:
        print("STOP: HEAD differs from the audited baseline.")
        return 2

    files = tracked_files()
    present = [p for p in files if exists_in_worktree(root, p)]
    names = artifact_names(files)

    canonical = [p for p in present if is_canonical(p)]
    phase_text = [
        p for p in present
        if is_phase_artifact_file(p)
        and Path(p).suffix.lower() in TEXT_EXTENSIONS
        and not any(p.startswith(prefix) for prefix in SELF_PREFIXES)
    ]

    print(f"Tracked paths in index: {len(files)}")
    print(f"Present tracked paths: {len(present)}")
    print(f"Remaining Phase artifacts: {len(names)}")
    print("Building canonical duplicate index...")
    duplicate_index = build_duplicate_index(root, canonical)
    print("Building single-pass reference indexes...")
    canonical_refs = build_reference_index(names, build_text_cache(root, canonical))
    artifact_refs = build_reference_index(names, build_text_cache(root, phase_text))

    rows = []
    combo_counter = Counter()
    disposition_counter = Counter()

    for name in names:
        members = [
            p for p in artifact_members(present, name)
            if not any(p.startswith(prefix) for prefix in SELF_PREFIXES)
        ]
        if not members:
            continue

        flags = classify_reason_flags(members)
        canon_refs = canonical_refs.get(name, [])
        other_refs = [
            p for p in artifact_refs.get(name, [])
            if not (p == name or p.startswith(name + "/"))
        ]
        relevant_count, duplicate_count, duplicate_members = canonical_duplicate_stats(
            root, members, duplicate_index
        )

        all_relevant_duplicated = (
            relevant_count > 0 and relevant_count == duplicate_count
        )
        no_runtime_payload = not flags["has_apply"] and not flags["has_payload"]
        no_canonical_ref = not canon_refs

        reasons = []
        for key in (
            "has_apply", "has_payload", "has_test", "has_run",
            "has_readme", "has_audit_or_diagnose",
        ):
            if flags[key]:
                reasons.append(key)
        if other_refs:
            reasons.append("artifact_only_reference")
        if canon_refs:
            reasons.append("canonical_reference")
        if relevant_count > duplicate_count:
            reasons.append("unique_relevant_content")
        if all_relevant_duplicated:
            reasons.append("all_relevant_content_canonical_duplicate")

        combo = "+".join(reasons) if reasons else "no_detected_reason"
        combo_counter[combo] += 1

        if canon_refs:
            disposition = "C_SAVE_CANONICAL_REFERENCE"
        elif (
            all_relevant_duplicated
            and no_runtime_payload
        ):
            disposition = "A_CANDIDATE_CANONICAL_DUPLICATE"
        elif (
            flags["has_test"]
            and duplicate_count > 0
            and relevant_count == duplicate_count
            and no_runtime_payload
        ):
            disposition = "A_CANDIDATE_TEST_DUPLICATE"
        elif flags["has_apply"] or flags["has_payload"]:
            disposition = "B_APPLY_OR_PAYLOAD"
        elif flags["has_test"]:
            disposition = "B_UNIQUE_TEST_MATERIAL"
        elif other_refs:
            disposition = "B_ARTIFACT_REFERENCE_CHAIN"
        elif relevant_count > duplicate_count:
            disposition = "B_UNIQUE_AUDIT_OR_DOC_CONTENT"
        else:
            disposition = "B_CONSERVATIVE_OTHER"

        disposition_counter[disposition] += 1

        rows.append({
            "artifact": name,
            "disposition": disposition,
            "reason_combination": combo,
            "file_count": len(members),
            "canonical_reference_count": len(canon_refs),
            "artifact_reference_count": len(other_refs),
            "relevant_text_code_count": relevant_count,
            "canonical_duplicate_count": duplicate_count,
            "has_apply": flags["has_apply"],
            "has_payload": flags["has_payload"],
            "has_test": flags["has_test"],
            "has_run": flags["has_run"],
            "has_readme": flags["has_readme"],
            "has_audit_or_diagnose": flags["has_audit_or_diagnose"],
            "canonical_references": " | ".join(canon_refs),
            "artifact_references": " | ".join(other_refs),
            "canonical_duplicate_members": " | ".join(duplicate_members),
        })

    out = root / "phase145_1_stage4_b_review_reclassification" / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_1_stage4_reclassification.csv"
    txt_path = out / "phase145_1_stage4_summary.txt"

    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-1 Stage 4 B_REVIEW Reason Reclassification\n")
        f.write("=" * 76 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Artifacts analyzed: {len(rows)}\n\n")
        f.write("DISPOSITION COUNTS\n")
        f.write("-" * 76 + "\n")
        for key, count in sorted(disposition_counter.items()):
            f.write(f"{key}: {count}\n")
        f.write("\nREASON-COMBINATION COUNTS\n")
        f.write("-" * 76 + "\n")
        for key, count in combo_counter.most_common():
            f.write(f"{count:4d}  {key}\n")
        f.write("\nA-CANDIDATES FOR NEXT REVIEW\n")
        f.write("-" * 76 + "\n")
        for row in rows:
            if row["disposition"].startswith("A_CANDIDATE"):
                f.write(
                    f'{row["artifact"]} :: {row["disposition"]} :: '
                    f'relevant={row["relevant_text_code_count"]}, '
                    f'duplicates={row["canonical_duplicate_count"]}, '
                    f'artifact_refs={row["artifact_reference_count"]}\n'
                )
        f.write("\nC-SAVE CANONICAL REFERENCES\n")
        f.write("-" * 76 + "\n")
        for row in rows:
            if row["disposition"] == "C_SAVE_CANONICAL_REFERENCE":
                f.write(
                    f'{row["artifact"]} :: '
                    f'{row["canonical_reference_count"]} canonical refs\n'
                )

    print("=" * 76)
    print("Stage 4 reclassification complete - NO DELETION")
    for key, count in sorted(disposition_counter.items()):
        print(f"{key}: {count}")
    print("=" * 76)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository files were deleted or modified by this audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
