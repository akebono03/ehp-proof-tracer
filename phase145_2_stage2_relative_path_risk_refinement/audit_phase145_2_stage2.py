from __future__ import annotations
import csv
import re
import subprocess
from collections import Counter
from pathlib import Path

EXPECTED_HEAD = "4737d71e339b704b787668f493201e4aebeeb991"
STAGE1_CSV = Path("phase145_2_stage1_archiving_audit/output/phase145_2_stage1_archiving_audit.csv")
SELF_PREFIX = "phase145_2_stage2_relative_path_risk_refinement/"
TEXT_EXTENSIONS = {".py", ".ps1", ".txt", ".md", ".json", ".html", ".css", ".js", ".yml", ".yaml", ".toml", ".ini", ".cfg"}

PARENT_AS_REPO_PATTERNS = (
    re.compile(r"\$RepoRoot\s*=\s*Split-Path\s+-Parent\s+\$PackageDir", re.I),
    re.compile(r"Path\(__file__\)\.resolve\(\)\.parent\.parent(?!\.parent)", re.I),
    re.compile(r"Path\(__file__\)\.parent\.parent(?!\.parent)", re.I),
)
ROOT_PHASE_REFERENCE_PATTERNS = (
    re.compile(r"repo_root\s*/\s*[\"']phase\d", re.I),
    re.compile(r"repo_root\s*/\s*[A-Z_]*DIR_NAME", re.I),
    re.compile(r"Join-Path\s+\$RepoRoot\s+[\"']phase\d", re.I),
    re.compile(r"Path\.cwd\(\)\s*/\s*[\"']phase\d", re.I),
)
UPWARD_FROM_SCRIPT_PATTERNS = (
    re.compile(r"\$PSScriptRoot[^\r\n]*(?:\\|/)\.\.(?:\\|/|\b)", re.I),
    re.compile(r"\$PackageDir[^\r\n]*(?:\\|/)\.\.(?:\\|/|\b)", re.I),
    re.compile(r"__file__[^\r\n]*parents?\s*\[\s*[12]\s*\]", re.I),
)
BROAD_ONLY_PATTERNS = (
    re.compile(r"\bPYTHONPATH\b", re.I),
    re.compile(r"\bPath\.cwd\(\)", re.I),
    re.compile(r"\bgetcwd\(\)", re.I),
    re.compile(r"\bSet-Location\b", re.I),
    re.compile(r"(?m)^\s*cd\s+", re.I),
    re.compile(r"\brepo_root\b", re.I),
    re.compile(r"repository root", re.I),
)

def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, text=True, encoding="utf-8",
                          errors="replace", capture_output=True).stdout

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

def evidence_for_file(text: str) -> tuple[list[str], bool]:
    hard = []
    if any(p.search(text) for p in PARENT_AS_REPO_PATTERNS):
        hard.append("PACKAGE_PARENT_ASSUMED_REPO_ROOT")
    if any(p.search(text) for p in ROOT_PHASE_REFERENCE_PATTERNS):
        hard.append("ROOT_RELATIVE_PHASE_SIBLING_REFERENCE")
    if any(p.search(text) for p in UPWARD_FROM_SCRIPT_PATTERNS):
        hard.append("UPWARD_NAVIGATION_FROM_ARTIFACT")
    broad = any(p.search(text) for p in BROAD_ONLY_PATTERNS)
    return hard, broad

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

    allowed = ("phase145_2_stage1_archiving_audit/", SELF_PREFIX)
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

    if not STAGE1_CSV.is_file():
        print(f"STOP: Stage 1 CSV not found: {STAGE1_CSV}")
        return 2

    with STAGE1_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        stage1 = list(csv.DictReader(f))
    risks = [r for r in stage1 if r["disposition"] == "MOVE_REQUIRES_RELATIVE_PATH_REVIEW"]
    safe = [r for r in stage1 if r["disposition"] == "MOVE_SAFE_CANDIDATE"]
    if len(risks) != 408:
        print(f"STOP: expected 408 Stage 1 review artifacts, found {len(risks)}.")
        return 2

    tracked = [p.replace("\\", "/") for p in git("ls-files").splitlines() if p.strip()]
    print(f"Stage 1 relative-path review population: {len(risks)}")
    print(f"Stage 1 already-safe population: {len(safe)}")
    print("Refining actual archive-sensitive path assumptions...")

    results = []
    counts = Counter()
    for row in risks:
        artifact = row["artifact"]
        members = tracked_members(artifact, tracked)
        evidence = []
        broad_files = []
        for member in members:
            fp = root / member
            if not fp.is_file() or fp.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            hard, broad = evidence_for_file(read_text(fp))
            evidence.extend(f"{member}:{reason}" for reason in hard)
            if broad:
                broad_files.append(member)
        reasons = sorted({x.rsplit(":", 1)[1] for x in evidence})
        if reasons:
            disposition = "MOVE_REQUIRES_PATH_UPDATE"
        elif broad_files:
            disposition = "MOVE_SAFE_AFTER_REFINEMENT"
        else:
            disposition = "MOVE_SAFE_STAGE1_FALSE_POSITIVE"
        counts[disposition] += 1
        results.append({
            "artifact": artifact,
            "kind": row["kind"],
            "tracked_file_count": row["tracked_file_count"],
            "destination": row["destination"],
            "stage1_relative_path_risk_count": row["relative_path_risk_count"],
            "stage2_disposition": disposition,
            "hard_reason_codes": " | ".join(reasons),
            "hard_evidence": " | ".join(sorted(set(evidence))),
            "broad_only_files": " | ".join(sorted(set(broad_files))),
        })

    out = root / SELF_PREFIX / "output"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "phase145_2_stage2_relative_path_refinement.csv"
    txt_path = out / "phase145_2_stage2_relative_path_refinement_summary.txt"
    fields = list(results[0]) if results else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    refined_safe = sum(v for k, v in counts.items() if k.startswith("MOVE_SAFE_"))
    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Phase 145-2 Stage 2 - Relative Path Risk Refinement\n")
        f.write("=" * 78 + "\n")
        f.write(f"HEAD: {head}\n")
        f.write(f"Stage 1 relative-path population: {len(risks)}\n")
        f.write(f"Stage 1 already-safe population: {len(safe)}\n\n")
        f.write("REFINED DISPOSITION COUNTS\n" + "-" * 78 + "\n")
        for key, count in sorted(counts.items()):
            f.write(f"{key}: {count}\n")
        f.write(f"\nTOTAL SAFE IF COMBINED WITH STAGE 1: {len(safe) + refined_safe}\n")
        f.write(f"TOTAL REQUIRING PATH UPDATE: {counts['MOVE_REQUIRES_PATH_UPDATE']}\n")
        for disposition in ("MOVE_REQUIRES_PATH_UPDATE", "MOVE_SAFE_AFTER_REFINEMENT",
                            "MOVE_SAFE_STAGE1_FALSE_POSITIVE"):
            f.write("\n" + disposition + "\n" + "-" * 78 + "\n")
            for r in results:
                if r["stage2_disposition"] == disposition:
                    f.write(f'{r["artifact"]} :: {r["kind"]} :: files={r["tracked_file_count"]} :: '
                            f'destination={r["destination"]}')
                    if r["hard_reason_codes"]:
                        f.write(f' :: reasons={r["hard_reason_codes"]}')
                    f.write("\n")

    print("=" * 78)
    print("Stage 2 refinement complete - NO MOVE / NO DELETE / NO CODE CHANGE")
    for key, count in sorted(counts.items()):
        print(f"{key}: {count}")
    print("-" * 78)
    print(f"Total move-safe candidates including Stage 1: {len(safe) + refined_safe}")
    print(f"Artifacts requiring path update before archive: {counts['MOVE_REQUIRES_PATH_UPDATE']}")
    print("=" * 78)
    print(f"CSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print("No repository file was moved, deleted, or modified.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
