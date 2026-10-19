import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
manifest = Path(__file__).with_name("phase103_manifest.csv")
rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
if len(rows) != 35 or sum(int(r["failed_tests"]) for r in rows) != 282:
    raise SystemExit("Manifest unexpected; no files moved")
source = repo / "standard_production_applicability_catalog.py"
if not source.is_file() or 'Legacy production applicability catalog is retired' not in source.read_text(encoding="utf-8"):
    raise SystemExit("Legacy catalog retirement guard not found; no files moved")
checks = []
for r in rows:
    name = r["file"]
    if not name.startswith("tests/test_phase103_") or not name.endswith(".py") or ".." in name:
        raise SystemExit("Unsafe path: " + name)
    path = repo / name
    if not path.is_file():
        raise SystemExit("Missing file; no files moved: " + name)
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != r["source_sha256"]:
        raise SystemExit("Hash mismatch; no files moved: " + name)
    content = data.decode("utf-8")
    if "standard_production_applicability_catalog" not in content:
        raise SystemExit("Catalog dependency not verified; no files moved: " + name)
    checks.append((r, path, data))
archive = repo / "phase165_r6_audit_results" / "retired_phase103_catalog" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
archive.mkdir(parents=True, exist_ok=False)
report = {"status": "PREPARED", "scope": "35 legacy catalog classification test modules", "initial_failed_tests": 282,
          "coverage_equivalence_verified": False, "whole_suite_run": False, "entries": [], "archive": str(archive)}
for r, path, data in checks:
    target = archive / r["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    report["entries"].append({"path":r["file"],"sha256":r["source_sha256"],"initial_failed_tests":int(r["failed_tests"]),"status":"backed_up"})
(archive / "report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
for r, path, data in checks:
    path.unlink()
    report["entries"][rows.index(r)]["status"]="archived"
report["status"]="APPLIED"
(archive / "report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"status":report["status"],"archived_test_files":len(checks),"initial_failed_nodes":282,"coverage_equivalence_verified":False,"report":str(archive / "report.json"),"full_pytest_run":False},ensure_ascii=False,indent=2))
