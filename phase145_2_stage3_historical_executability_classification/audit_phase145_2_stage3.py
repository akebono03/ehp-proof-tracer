from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter
from pathlib import Path

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
STAGE2_CSV = Path(
    "phase145_2_stage2_relative_path_risk_refinement/output/"
    "phase145_2_stage2_relative_path_refinement.csv"
)
SELF_PREFIX = "phase145_2_stage3_historical_executability_classification/"
TEXT_EXTENSIONS = {
    ".py", ".ps1", ".txt", ".md", ".json", ".html", ".css", ".js",
    ".yml", ".yaml", ".toml", ".ini", ".cfg",
}

FINAL_GATE_RE = re.compile(
    r"(?:finalization|final_full_suite|repository_wide_pytest|"
    r"final_completion_audit_and_full_pytest)",
    re.I,
)
APPLY_FILE_RE = re.compile(r"(?:^|/)(?:apply|install|patch)[^/]*\.(?:py|ps1)$", re.I)
PAYLOAD_PATH_RE = re.compile(r"(?:^|/)payload(?:/|$)", re.I)
RUNNER_FILE_RE = re.compile(r"(?:^|/)run[^/]*\.ps1$", re.I)
AUDIT_ONLY_NAME_RE = re.compile(r"(?:audit|diagnos|inspection|measurement)", re.I)

CANONICAL_TEST_RE = re.compile(r"(?:^|[\"'`])(?:\.\\|\./)?tests[\\/]", re.I)
CANONICAL_CODE_RE = re.compile(
    r"(?:^|[\"'`])(?:\.\\|\./)?"
    r"(?:main\.py|web_[A-Za-z0-9_]+\.py|toda_[A-Za-z0-9_]+\.py|"
    r"proof_[A-Za-z0-9_]+\.py|ehp_[A-Za-z0-9_]+\.py)",
    re.I,
)
OTHER_PHASE_RE = re.compile(r"phase\d[\w.-]*(?:[\\/])", re.I)


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

    if not STAGE2_CSV.is_file():
        print(f"STOP: Stage 2 CSV not found: {STAGE2_CSV}")
        return 2

    with STAGE2_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        stage2 = list(csv.DictReader(f))

    population = [
        row for row in stage2
        if row["stage2_disposition"] == "MOVE_REQUIRES_PATH_UPDATE"
    ]
    if len(population) != 91:
        print(f"STOP: expected 91 Stage 2 path-update artifacts, found {len(population)}.")
        return 2

    tracked = [
        p.replace("\\", "/")
        for p in git("ls-files").splitlines()
        if p.strip()
    ]

    print(f"Stage 2 path-update population: {len(population)}")
    print("Classifying historical executability requirements...")

    results = []
    counts = Counter()

    for row in population:
        artifact = row["artifact"]
        members = tracked_members(artifact, tracked)
        texts = []
        for member in members:
            fp = root / member
            if fp.is_file() and fp.suffix.lower() in TEXT_EXTENSIONS:
                texts.append((member, read_text(fp)))

        combined = "\n".join(text for _, text in texts)
        member_names = "\n".join(members)

        has_apply = any(APPLY_FILE_RE.search(p) for p in members)
        has_payload = any(PAYLOAD_PATH_RE.search(p) for p in members)
        has_runner = any(RUNNER_FILE_RE.search(p) for p in members)
        final_gate = bool(FINAL_GATE_RE.search(artifact))
        canonical_test = bool(CANONICAL_TEST_RE.search(combined))
        canonical_code = bool(CANONICAL_CODE_RE.search(combined))

        other_phase_refs = sorted({
            m.group(0).replace("\\", "/").rstrip("/")
            for m in OTHER_PHASE_RE.finditer(combined)
            if not m.group(0).lower().startswith(artifact.lower() + "/")
        })
        dependency_chain = bool(other_phase_refs)

        audit_named = bool(AUDIT_ONLY_NAME_RE.search(artifact))
        root_file = row["kind"] == "root_file"

        reasons = []
        if final_gate:
            reasons.append("FINAL_OR_FULL_SUITE_GATE")
        if has_apply:
            reasons.append("HAS_APPLY_OR_INSTALLER")
        if has_payload:
            reasons.append("HAS_PAYLOAD")
        if canonical_test:
            reasons.append("RUNS_OR_REFERENCES_CANONICAL_TESTS")
        if canonical_code:
            reasons.append("RUNS_OR_REFERENCES_CANONICAL_CODE")
        if dependency_chain:
            reasons.append("REFERENCES_OTHER_PHASE_ARTIFACT")
        if root_file:
            reasons.append("ROOT_LEVEL_HISTORICAL_TOOL")
        if audit_named:
            reasons.append("AUDIT_OR_DIAGNOSTIC_NAME")

        # Priority:
        # 1. Cross-artifact dependencies need chain review before relocation.
        # 2. Final/full-suite gates and packages that can mutate production
        #    (apply/payload) retain executability unless explicitly retired.
        # 3. Root historical audit tools and audit-only packages are historical.
        # 4. Remaining packages that merely run/read canonical code/tests are
        #    treated as historical verification artifacts.
        if dependency_chain:
            disposition = "DEPENDENCY_CHAIN_REVIEW"
        elif final_gate or has_apply or has_payload:
            disposition = "EXECUTABILITY_REQUIRED"
        else:
            disposition = "HISTORICAL_ONLY"

        counts[disposition] += 1
        results.append({
            "artifact": artifact,
            "kind": row["kind"],
            "tracked_file_count": row["tracked_file_count"],
            "destination": row["destination"],
            "stage2_hard_reason_codes": row["hard_reason_codes"],
            "stage3_disposition": disposition,
            "evidence_codes": " | ".join(reasons),
            "other_phase_references": " | ".join(other_phase_refs),
            "has_runner": "yes" if has_runner else "no",
            "has_apply_or_installer": "yes" if has_apply else "no",
            "has_payload": "yes" if has_payload else "no",
            "references_canonical_tests": "yes" if canonical_test else "no",
            "references_canonical_code": "yes" if canonical_code else "no",
        })

    out = root / SELF_PREFIX / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_2_stage3_historical_executability.csv"
    txt_path = out / "phase145_2_stage3_historical_executability_summary.txt"

    fields = list(results[0].keys()) if results else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-2 Stage 3 - Historical Executability Classification\n")
        f.write("=" * 78 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Stage 2 path-update population: {len(population)}\n\n")
        f.write("CLASSIFICATION COUNTS\n")
        f.write("-" * 78 + "\n")
        for key in (
            "EXECUTABILITY_REQUIRED",
            "DEPENDENCY_CHAIN_REVIEW",
            "HISTORICAL_ONLY",
        ):
            f.write(f"{key}: {counts[key]}\n")

        for disposition in (
            "EXECUTABILITY_REQUIRED",
            "DEPENDENCY_CHAIN_REVIEW",
            "HISTORICAL_ONLY",
        ):
            f.write("\n" + disposition + "\n")
            f.write("-" * 78 + "\n")
            for result in results:
                if result["stage3_disposition"] != disposition:
                    continue
                f.write(
                    f'{result["artifact"]} :: {result["kind"]} :: '
                    f'files={result["tracked_file_count"]} :: '
                    f'reasons={result["evidence_codes"]}\n'
                )
                if result["other_phase_references"]:
                    f.write(
                        f'  other_phase_refs={result["other_phase_references"]}\n'
                    )

    print("=" * 78)
    print("Stage 3 classification complete - NO MOVE / NO DELETE / NO CODE CHANGE")
    for key in (
        "EXECUTABILITY_REQUIRED",
        "DEPENDENCY_CHAIN_REVIEW",
        "HISTORICAL_ONLY",
    ):
        print(f"{key}: {counts[key]}")
    print("=" * 78)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository file was moved, deleted, or modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
