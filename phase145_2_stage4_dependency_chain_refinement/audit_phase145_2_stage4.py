from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter
from pathlib import Path

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
STAGE3_CSV = Path(
    "phase145_2_stage3_historical_executability_classification/output/"
    "phase145_2_stage3_historical_executability.csv"
)
SELF_PREFIX = "phase145_2_stage4_dependency_chain_refinement/"
TEXT_EXTENSIONS = {
    ".py", ".ps1", ".txt", ".md", ".json", ".html", ".css", ".js",
    ".yml", ".yaml", ".toml", ".ini", ".cfg",
}

# Capture a Phase artifact token. The token stops before path separators,
# quotes, whitespace, or punctuation commonly used after a path component.
PHASE_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(phase\d[A-Za-z0-9_.-]*)"
    r"(?=[\\/\"'`\s),;:]|$)",
    re.I,
)


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


def tracked_members(artifact: str, tracked: list[str]) -> list[str]:
    if "/" not in artifact and "." in artifact:
        return [artifact] if artifact in tracked else []
    prefix = artifact.rstrip("/") + "/"
    return [p for p in tracked if p.startswith(prefix)]


def phase_tokens(text: str) -> set[str]:
    return {m.group(1) for m in PHASE_TOKEN_RE.finditer(text)}


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

    allowed = (
        "phase145_2_stage1_archiving_audit/",
        "phase145_2_stage2_relative_path_risk_refinement/",
        "phase145_2_stage3_historical_executability_classification/",
        SELF_PREFIX,
    )
    unexpected = []
    for line in git("status", "--porcelain").splitlines():
        if not line.strip():
            continue
        path = line[3:].replace("\\", "/")
        if not any(path.startswith(prefix) for prefix in allowed):
            unexpected.append(line)
    if unexpected:
        print("STOP: working tree contains changes outside Phase 145-2 audit packages:")
        for line in unexpected[:50]:
            print(line)
        return 2

    if not STAGE3_CSV.is_file():
        print(f"STOP: Stage 3 CSV not found: {STAGE3_CSV}")
        return 2

    with STAGE3_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        stage3 = list(csv.DictReader(f))

    population = [
        row for row in stage3
        if row["stage3_disposition"] == "DEPENDENCY_CHAIN_REVIEW"
    ]
    if len(population) != 41:
        print(f"STOP: expected 41 Stage 3 dependency-review artifacts, found {len(population)}.")
        return 2

    tracked = [
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    ]

    # Known Phase artifact names come from current root-level tracked paths.
    known_artifacts = set()
    for path in tracked:
        first = path.split("/", 1)[0]
        if re.match(r"^phase\d", first, re.I):
            known_artifacts.add(first)
        elif "/" not in path and re.match(r"^phase\d", path, re.I):
            known_artifacts.add(path)

    print(f"Stage 3 dependency-review population: {len(population)}")
    print(f"Known root Phase artifact names: {len(known_artifacts)}")
    print("Removing self references and resolving only real cross-artifact references...")

    results = []
    counts = Counter()

    for row in population:
        artifact = row["artifact"]
        members = tracked_members(artifact, tracked)
        token_files: dict[str, set[str]] = {}

        for member in members:
            fp = root / member
            if not fp.is_file() or fp.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            text = read_text(fp)
            for token in phase_tokens(text):
                token_files.setdefault(token, set()).add(member)

        self_refs = sorted(
            token for token in token_files
            if token.lower() == artifact.lower()
        )
        cross_refs = sorted(
            token for token in token_files
            if token.lower() != artifact.lower()
            and token in known_artifacts
        )
        unresolved_tokens = sorted(
            token for token in token_files
            if token.lower() != artifact.lower()
            and token not in known_artifacts
        )

        if cross_refs:
            disposition = "TRUE_CROSS_ARTIFACT_DEPENDENCY"
        elif unresolved_tokens:
            disposition = "UNRESOLVED_PHASE_TOKEN_REVIEW"
        else:
            disposition = "SELF_REFERENCE_ONLY_MOVE_CANDIDATE"

        counts[disposition] += 1

        evidence = []
        for token in cross_refs:
            files = ",".join(sorted(token_files[token]))
            evidence.append(f"{token} <- {files}")

        results.append({
            "artifact": artifact,
            "kind": row["kind"],
            "tracked_file_count": row["tracked_file_count"],
            "destination": row["destination"],
            "stage3_evidence_codes": row["evidence_codes"],
            "stage4_disposition": disposition,
            "self_reference_tokens": " | ".join(self_refs),
            "cross_artifact_dependencies": " | ".join(cross_refs),
            "unresolved_phase_tokens": " | ".join(unresolved_tokens),
            "cross_dependency_evidence": " | ".join(evidence),
        })

    out = root / SELF_PREFIX / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_2_stage4_dependency_chain_refinement.csv"
    txt_path = out / "phase145_2_stage4_dependency_chain_refinement_summary.txt"

    fields = list(results[0].keys()) if results else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-2 Stage 4 - Dependency Chain Refinement\n")
        f.write("=" * 78 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Stage 3 dependency-review population: {len(population)}\n\n")
        f.write("REFINED COUNTS\n")
        f.write("-" * 78 + "\n")
        for key in (
            "TRUE_CROSS_ARTIFACT_DEPENDENCY",
            "SELF_REFERENCE_ONLY_MOVE_CANDIDATE",
            "UNRESOLVED_PHASE_TOKEN_REVIEW",
        ):
            f.write(f"{key}: {counts[key]}\n")

        for disposition in (
            "TRUE_CROSS_ARTIFACT_DEPENDENCY",
            "UNRESOLVED_PHASE_TOKEN_REVIEW",
            "SELF_REFERENCE_ONLY_MOVE_CANDIDATE",
        ):
            f.write("\n" + disposition + "\n")
            f.write("-" * 78 + "\n")
            for result in results:
                if result["stage4_disposition"] != disposition:
                    continue
                f.write(
                    f'{result["artifact"]} :: files={result["tracked_file_count"]}'
                )
                if result["cross_artifact_dependencies"]:
                    f.write(
                        f' :: cross={result["cross_artifact_dependencies"]}'
                    )
                if result["unresolved_phase_tokens"]:
                    f.write(
                        f' :: unresolved={result["unresolved_phase_tokens"]}'
                    )
                if result["self_reference_tokens"]:
                    f.write(
                        f' :: self={result["self_reference_tokens"]}'
                    )
                f.write("\n")

    print("=" * 78)
    print("Stage 4 refinement complete - NO MOVE / NO DELETE / NO CODE CHANGE")
    for key in (
        "TRUE_CROSS_ARTIFACT_DEPENDENCY",
        "SELF_REFERENCE_ONLY_MOVE_CANDIDATE",
        "UNRESOLVED_PHASE_TOKEN_REVIEW",
    ):
        print(f"{key}: {counts[key]}")
    print("=" * 78)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository file was moved, deleted, or modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
