from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter
from pathlib import Path

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
STAGE4_CSV = Path(
    "phase145_2_stage4_dependency_chain_refinement/output/"
    "phase145_2_stage4_dependency_chain_refinement.csv"
)
SELF_PREFIX = "phase145_2_stage5_unresolved_token_final_classification/"

OUTPUT_SUFFIXES = (
    ".txt", ".zip", ".log", ".csv", ".json",
)
WORKTREE_RE = re.compile(r"(?:^|[_.-])worktree(?:$|[_.-])", re.I)
MODULE_PATH_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+$")
BROAD_PHASE_LABEL_RE = re.compile(r"^Phase\d+$", re.I)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    ).stdout


def git_history_contains(token: str) -> bool:
    # Search all reachable history for an exact token. This is intentionally
    # used only for the small Stage 5 unresolved population.
    result = subprocess.run(
        ["git", "log", "--all", "-S", token, "--format=%H", "--"],
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return bool(result.stdout.strip())


def classify_token(
    token: str,
    artifact: str,
    tracked_paths: set[str],
) -> tuple[str, str]:
    lower = token.lower()

    if lower == artifact.lower():
        return "SELF_REFERENCE", "token equals current artifact name"

    if any(lower.endswith(suffix) for suffix in OUTPUT_SUFFIXES):
        return "GENERATED_OR_PACKAGED_OUTPUT", "file-like output/archive suffix"

    if WORKTREE_RE.search(token):
        return "TEMPORARY_WORKTREE", "worktree/cache-style temporary path token"

    if MODULE_PATH_RE.match(token):
        first = token.split(".", 1)[0]
        if first.lower() == artifact.lower():
            return "INTRA_ARTIFACT_MODULE_PATH", "Python module path rooted in current artifact"

    if BROAD_PHASE_LABEL_RE.match(token):
        return "DOCUMENTATION_PHASE_LABEL", "broad Phase label, not an artifact path"

    # If a token names a current tracked path it should have been resolved in
    # Stage 4. Keep a defensive classification here.
    if token in tracked_paths or any(p.startswith(token + "/") for p in tracked_paths):
        return "CURRENT_TRACKED_PATH_REVIEW", "currently tracked path unexpectedly unresolved"

    if git_history_contains(token):
        return "MISSING_HISTORICAL_ARTIFACT_REFERENCE", "token occurs in reachable Git history"

    return "NON_ARTIFACT_LITERAL", "no current path or reachable historical artifact evidence"


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
        "phase145_2_stage4_dependency_chain_refinement/",
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

    if not STAGE4_CSV.is_file():
        print(f"STOP: Stage 4 CSV not found: {STAGE4_CSV}")
        return 2

    with STAGE4_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        stage4 = list(csv.DictReader(f))

    population = [
        row for row in stage4
        if row["stage4_disposition"] == "UNRESOLVED_PHASE_TOKEN_REVIEW"
    ]
    if len(population) != 16:
        print(f"STOP: expected 16 Stage 4 unresolved artifacts, found {len(population)}.")
        return 2

    tracked_paths = {
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    }

    print(f"Stage 4 unresolved artifact population: {len(population)}")
    print("Classifying every unresolved token by concrete role...")

    results = []
    artifact_counts = Counter()
    token_counts = Counter()

    blocking_token_classes = {
        "MISSING_HISTORICAL_ARTIFACT_REFERENCE",
        "CURRENT_TRACKED_PATH_REVIEW",
    }

    for row in population:
        artifact = row["artifact"]
        raw_tokens = [
            token.strip()
            for token in row["unresolved_phase_tokens"].split("|")
            if token.strip()
        ]

        token_details = []
        has_blocking = False
        for token in raw_tokens:
            token_class, reason = classify_token(token, artifact, tracked_paths)
            token_counts[token_class] += 1
            if token_class in blocking_token_classes:
                has_blocking = True
            token_details.append((token, token_class, reason))

        if has_blocking:
            disposition = "HISTORICAL_DEPENDENCY_SPECIAL_HANDLING"
        else:
            disposition = "NON_DEPENDENCY_MOVE_CANDIDATE"

        artifact_counts[disposition] += 1
        results.append({
            "artifact": artifact,
            "tracked_file_count": row["tracked_file_count"],
            "destination": row["destination"],
            "stage5_disposition": disposition,
            "token_classifications": " | ".join(
                f"{token} => {token_class}"
                for token, token_class, _ in token_details
            ),
            "token_reasons": " | ".join(
                f"{token} => {reason}"
                for token, _, reason in token_details
            ),
        })

    out = root / SELF_PREFIX / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_2_stage5_unresolved_token_final_classification.csv"
    txt_path = out / "phase145_2_stage5_unresolved_token_final_classification_summary.txt"

    fields = list(results[0].keys()) if results else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-2 Stage 5 - Unresolved Token Final Classification\n")
        f.write("=" * 78 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Stage 4 unresolved artifact population: {len(population)}\n\n")

        f.write("ARTIFACT DISPOSITION COUNTS\n")
        f.write("-" * 78 + "\n")
        for key in (
            "HISTORICAL_DEPENDENCY_SPECIAL_HANDLING",
            "NON_DEPENDENCY_MOVE_CANDIDATE",
        ):
            f.write(f"{key}: {artifact_counts[key]}\n")

        f.write("\nTOKEN CLASS COUNTS\n")
        f.write("-" * 78 + "\n")
        for key in sorted(token_counts):
            f.write(f"{key}: {token_counts[key]}\n")

        for disposition in (
            "HISTORICAL_DEPENDENCY_SPECIAL_HANDLING",
            "NON_DEPENDENCY_MOVE_CANDIDATE",
        ):
            f.write("\n" + disposition + "\n")
            f.write("-" * 78 + "\n")
            for result in results:
                if result["stage5_disposition"] != disposition:
                    continue
                f.write(
                    f'{result["artifact"]} :: files={result["tracked_file_count"]}\n'
                )
                f.write(
                    f'  tokens={result["token_classifications"]}\n'
                )

    print("=" * 78)
    print("Stage 5 final classification complete - NO MOVE / NO DELETE / NO CODE CHANGE")
    for key in (
        "HISTORICAL_DEPENDENCY_SPECIAL_HANDLING",
        "NON_DEPENDENCY_MOVE_CANDIDATE",
    ):
        print(f"{key}: {artifact_counts[key]}")
    print("-" * 78)
    for key in sorted(token_counts):
        print(f"{key}: {token_counts[key]}")
    print("=" * 78)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository file was moved, deleted, or modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
