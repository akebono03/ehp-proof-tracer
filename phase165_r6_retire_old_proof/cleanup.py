from __future__ import annotations
import argparse
import ast
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CATEGORIES = {"MISSING_SHARED_TEST_HELPER", "MISSING_HISTORICAL_TEST_HELPER", "RETIRED_PROBE_RULE", "RETIRED_RENDERER"}

def phase(path: str) -> int:
    match = re.search(r"test_phase(\d+)", Path(path).name)
    return int(match.group(1)) if match else 999

def eligible(record: dict) -> bool:
    name = record["file"]
    if not name.startswith("tests/test_phase") or record["category"] not in CATEGORIES:
        return False
    number = phase(name)
    if record["category"] == "RETIRED_PROBE_RULE":
        return 130 <= number <= 162
    if record["category"] == "RETIRED_RENDERER":
        return 130 <= number <= 162
    return 130 <= number <= 162

def test_references(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    except (SyntaxError, UnicodeDecodeError):
        return set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[-1] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[-1])
    return names

def removable_set(records: list[dict], files: dict[str, Path]) -> tuple[set[str], dict[str, list[str]]]:
    initial = {r["file"] for r in records if eligible(r) and r["file"] in files}
    by_name = {p.stem: name for name, p in files.items()}
    incoming = {name: set() for name in files}
    for owner, path in files.items():
        for imported in test_references(path):
            other = by_name.get(imported)
            if other and other != owner:
                incoming[other].add(owner)
    kept = set(files) - initial
    while True:
        blocked = {name for name in initial if incoming[name] & kept}
        if not blocked:
            break
        initial.difference_update(blocked)
        kept.update(blocked)
    dependencies = {name: sorted(incoming[name] & kept) for name in files if name not in initial}
    return initial, dependencies

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_records(root: Path) -> tuple[list[dict], Path]:
    reports = sorted((root / "phase165_r6_audit_results" / "triage_266").glob("report.json"))
    if not reports:
        raise RuntimeError("Missing phase165_r6_audit_results/triage_266/report.json; no files changed")
    report = json.loads(reports[-1].read_text(encoding="utf-8"))
    if report.get("error_count") != 266 or len(report.get("records", [])) != 266:
        raise RuntimeError("Baseline must contain exactly 266 records; no files changed")
    return report["records"], reports[-1]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    records, source = load_records(root)
    files = {p.relative_to(root).as_posix(): p for p in (root / "tests").glob("test_*.py")}
    to_remove, deps = removable_set(records, files)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = root / "phase165_r6_audit_results" / "old_proof_retirement" / timestamp
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name in sorted(to_remove):
        data = files[name].read_bytes()
        manifest.append({"path": name, "sha256": sha256(data), "size": len(data)})
    result = {"baseline": str(source), "baseline_errors": 266, "candidate_count": sum(eligible(r) for r in records), "removable_count": len(to_remove), "protected_count": 266-len(to_remove), "removed": [], "manifest": manifest, "mode": "APPLY" if args.apply else "DRY_RUN", "full_pytest_run": False}
    (output / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    if not args.apply:
        print(json.dumps({"status": "DRY_RUN", "removable": len(to_remove), "report": str(output / "report.json")}, ensure_ascii=False))
        return 0
    backup = output / "backup"
    for item in manifest:
        src = files[item["path"]]
        data = src.read_bytes()
        if sha256(data) != item["sha256"]:
            raise RuntimeError("File changed during audit: " + item["path"])
        target = backup / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if sha256(target.read_bytes()) != item["sha256"]:
            raise RuntimeError("Backup verification failed: " + item["path"])
    for item in manifest:
        files[item["path"]].unlink()
        result["removed"].append(item["path"])
    (output / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    collection = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "tests", *sorted(p.name for p in root.glob("test_*.py"))], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    (output / "collection.log").write_text(collection.stdout, encoding="utf-8")
    matches = re.findall(r"(?:^|\n)\s*(\d+) errors? in [\d.]+s", collection.stdout)
    result["collection_exit_code"] = collection.returncode
    result["collection_error_count"] = int(matches[-1]) if matches else (0 if collection.returncode == 0 else None)
    result["collection_summary_tail"] = collection.stdout[-1500:]
    (output / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "APPLIED", "removed": len(result["removed"]), "remaining_collection_errors": result["collection_error_count"], "report": str(output / "report.json"), "full_pytest_run": False}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
