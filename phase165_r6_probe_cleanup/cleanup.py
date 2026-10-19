from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


NAME_PATTERN = re.compile(r"test_phase[0-9a-z_]+_probe\.py\Z")


def imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan_cleanup(root: Path, triage: dict) -> dict:
    tests = root / "tests"
    failed = {
        entry["test_path"]: entry
        for entry in triage.get("records", [])
    }
    sources = sorted(tests.glob("test_*.py"))
    imported_by: dict[str, list[str]] = {}
    parse_failures: dict[str, str] = {}
    parsed: dict[str, set[str]] = {}
    for source in sources:
        relative = source.relative_to(root).as_posix()
        try:
            parsed[relative] = imports_of(source)
        except (SyntaxError, UnicodeError) as exc:
            parse_failures[relative] = str(exc)
    # Conservative: parsing any current test unsuccessfully blocks deletion.
    global_blocked = bool(parse_failures)
    for relative, imports in parsed.items():
        for module in imports:
            imported_by.setdefault(module, []).append(relative)
    decisions = []
    for relative, entry in sorted(failed.items()):
        path = root / relative
        if not NAME_PATTERN.fullmatch(path.name):
            continue
        reasons = []
        if entry.get("detail", "").find("toda_pi4_3_delta_image_free_cyclic_inference_rule") == -1:
            reasons.append("NOT_TARGET_ERROR")
        if not path.is_file():
            reasons.append("MISSING_FILE")
            direct = False
        else:
            direct = any(name.startswith("probes.probe_phase") for name in parsed.get(relative, set()))
            if not direct:
                reasons.append("NOT_DIRECT_PROBE_IMPORT")
        if global_blocked:
            reasons.append("UNPARSEABLE_TEST_EXISTS")
        references = sorted(set(imported_by.get(path.stem, []) + imported_by.get("tests." + path.stem, [])) - {relative})
        if references:
            reasons.append("IMPORTED_BY_OTHER_TESTS")
        if relative not in parsed:
            reasons.append("SOURCE_NOT_PARSED")
        decisions.append({"path": relative, "decision": "QUARANTINE" if not reasons else "KEEP", "reasons": reasons, "imported_by": references, "sha256": digest(path) if path.is_file() else None})
    return {"phase": "165 R6", "operation": "probe_only_test_cleanup", "parse_failures": parse_failures, "decisions": decisions}


def perform(root: Path, report: dict, backup: Path) -> None:
    candidates = [d for d in report["decisions"] if d["decision"] == "QUARANTINE"]
    if not candidates:
        return
    backup.mkdir(parents=True, exist_ok=True)
    # Check all sources and backup collisions before touching any originals.
    for entry in candidates:
        source = root / entry["path"]
        target = backup / entry["path"]
        if not source.is_file() or digest(source) != entry["sha256"]:
            raise RuntimeError("Source changed: " + entry["path"])
        if target.exists() and digest(target) != entry["sha256"]:
            raise RuntimeError("Backup conflict: " + entry["path"])
    for entry in candidates:
        source = root / entry["path"]
        target = backup / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(source, target)
        if digest(target) != entry["sha256"]:
            raise RuntimeError("Backup verification failed: " + entry["path"])
    for entry in candidates:
        source = root / entry["path"]
        if digest(source) != entry["sha256"]:
            raise RuntimeError("Source changed during backup: " + entry["path"])
        source.unlink()
        entry["result"] = "BACKED_UP_AND_REMOVED"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python cleanup.py PROJECT_ROOT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    result_dir = root / "phase165_r6_audit_results"
    triage_path = result_dir / "collection_error_triage.json"
    if not triage_path.is_file():
        print("Missing prerequisite: " + str(triage_path), file=sys.stderr)
        return 2
    triage = json.loads(triage_path.read_text(encoding="utf-8"))
    if triage.get("total_collection_errors") != 497:
        print("Refusing unexpected triage data", file=sys.stderr)
        return 2
    report = plan_cleanup(root, triage)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    session = result_dir / "probe_cleanup" / stamp
    session.mkdir(parents=True, exist_ok=True)
    report["backup_directory"] = str(session / "backup")
    report["status"] = "PLANNED"
    (session / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    perform(root, report, session / "backup")
    report["status"] = "COMPLETED"
    (session / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    removed = sum(d.get("result") == "BACKED_UP_AND_REMOVED" for d in report["decisions"])
    kept = sum(d["decision"] == "KEEP" for d in report["decisions"])
    print("Probe-only candidates removed:", removed)
    print("Probe-only candidates retained:", kept)
    print("Report:", session / "report.json")
    print("Backup:", session / "backup")
    print("Other collection errors remain unresolved. No full pytest run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
