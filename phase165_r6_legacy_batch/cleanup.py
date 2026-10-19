from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LEGACY = re.compile(r"test_phase(8[0-9]|9[0-9]|10[0-9]|11[0-9]|12[0-9])(?:_|\b)")
MISSING = re.compile(r"No module named '([^']+)'", re.ASCII)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


def plan(root: Path, triage: dict) -> dict:
    tests = sorted((root / "tests").glob("test_*.py"))
    parsed = {}
    errors = {}
    for path in tests:
        rel = path.relative_to(root).as_posix()
        try:
            parsed[rel] = imports(path)
        except (SyntaxError, UnicodeError) as exc:
            errors[rel] = str(exc)
    reverse: dict[str, set[str]] = defaultdict(set)
    for rel, names in parsed.items():
        for name in names:
            reverse[name].add(rel)
    candidates = []
    for row in triage["records"]:
        rel = row["test_path"]
        path = root / rel
        if not LEGACY.match(path.stem):
            continue
        detail = row["detail"]
        match = MISSING.search(detail)
        if not match or not match.group(1).startswith("repository_"):
            continue
        module = match.group(1)
        reasons = []
        if not path.is_file():
            reasons.append("FILE_MISSING")
        if errors:
            reasons.append("PARSE_ERRORS_EXIST")
        if rel not in parsed or module not in parsed.get(rel, set()):
            reasons.append("NO_DIRECT_MISSING_IMPORT")
        if (root / (module.replace(".", "/") + ".py")).exists():
            reasons.append("MODULE_EXISTS_IN_ROOT")
        if (root / "probes" / (module + ".py")).exists():
            reasons.append("MODULE_EXISTS_IN_PROBES")
        if (root / "tests" / (module + ".py")).exists():
            reasons.append("MODULE_EXISTS_IN_TESTS")
        incoming = sorted((reverse.get(path.stem, set()) | reverse.get("tests." + path.stem, set())) - {rel})
        if incoming:
            reasons.append("IMPORTED_BY_OTHER_TESTS")
        candidates.append({"path": rel, "module": module, "sha256": sha(path) if path.is_file() else None, "incoming": incoming, "decision": "REMOVE" if not reasons else "KEEP", "reasons": reasons})
    return {"status": "PLANNED", "scope": "Phase80-129 direct missing repository module, no test consumers", "parse_errors": errors, "decisions": candidates}


def apply(root: Path, report: dict, backup: Path) -> None:
    chosen = [x for x in report["decisions"] if x["decision"] == "REMOVE"]
    for x in chosen:
        if sha(root / x["path"]) != x["sha256"]:
            raise RuntimeError("Changed source: " + x["path"])
        if (backup / x["path"]).exists():
            raise RuntimeError("Backup collision: " + x["path"])
    for x in chosen:
        out = backup / x["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / x["path"], out)
        if sha(out) != x["sha256"]:
            raise RuntimeError("Backup mismatch: " + x["path"])
    for x in chosen:
        src = root / x["path"]
        if sha(src) != x["sha256"]:
            raise RuntimeError("Changed during cleanup: " + x["path"])
        src.unlink()
        x["result"] = "REMOVED_AFTER_BACKUP"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: cleanup.py PROJECT_ROOT")
    root = Path(sys.argv[1]).resolve()
    triage_file = root / "phase165_r6_audit_results" / "collection_error_triage.json"
    triage = json.loads(triage_file.read_text(encoding="utf-8"))
    if triage.get("total_collection_errors") != 497:
        raise RuntimeError("Unexpected source audit")
    report = plan(root, triage)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = root / "phase165_r6_audit_results" / "legacy_batch" / stamp
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    apply(root, report, out / "backup")
    report["status"] = "COMPLETED"
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Removed:", sum(x.get("result") == "REMOVED_AFTER_BACKUP" for x in report["decisions"]))
    print("Retained:", sum(x["decision"] == "KEEP" for x in report["decisions"]))
    print("Report:", out / "report.json")
    print("No full pytest run; R6 closure PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
