from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "phase165_r6_audit_results" / "targeted_verify"
OUT.mkdir(parents=True, exist_ok=True)

TEST_GROUPS = {
    "shared_backward": [
        ROOT / "test_phase165_r52_r9_shared_math.py",
        ROOT / "phase165_r52_r9_shared_math" / "test_phase165_r52_r9_shared_math.py",
    ],
    "public_renderer": [
        ROOT / "test_phase165_r57_r1_single_entry.py",
        ROOT / "phase165_r57_r1_single_entry" / "test_phase165_r57_r1_single_entry.py",
    ],
    "inverse_rules": [
        ROOT / "test_phase165_r6_2_r2_verified_inverse.py",
        ROOT / "phase165_r6_2_r2_verified_inverse" / "test_phase165_r6_2_r2_verified_inverse.py",
    ],
}

result = {"phase": "165 R6", "mode": "targeted_no_modification",
          "checked_at_utc": datetime.now(timezone.utc).isoformat(),
          "full_pytest_run": False, "groups": {}}
for label, candidates in TEST_GROUPS.items():
    found = next((path for path in candidates if path.is_file()), None)
    if found is None:
        print(f"[MISSING] {label} : " + ", ".join(str(p.relative_to(ROOT)) for p in candidates), flush=True)
        result["groups"][label] = {"status": "MISSING", "paths_checked": [str(p.relative_to(ROOT)) for p in candidates]}
        continue
    relative = str(found.relative_to(ROOT))
    print(f"[RUN] {label}: {relative} (timeout=90 seconds)", flush=True)
    try:
        run = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(found)],
            cwd=ROOT, text=True, encoding="utf-8", errors="replace",
            capture_output=True, timeout=90, env={**os.environ, "PYTHONPATH": str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", "")},
        )
        output = (run.stdout or "") + "\n" + (run.stderr or "")
        (OUT / f"{label}.log").write_text(output, encoding="utf-8")
        status = "PASS" if run.returncode == 0 else "FAIL"
        print(f"[{status}] {label}: exit={run.returncode}", flush=True)
        print("\n".join(output.splitlines()[-12:]), flush=True)
        result["groups"][label] = {"status": status, "path": relative, "exit_code": run.returncode}
    except subprocess.TimeoutExpired as exc:
        print(f"[TIMEOUT] {label}: over 90 seconds", flush=True)
        result["groups"][label] = {"status": "TIMEOUT", "path": relative}
overall = "PASS" if all(item["status"] == "PASS" for item in result["groups"].values()) else "INCOMPLETE"
result["status"] = overall
(OUT / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("REPORT:", OUT / "report.json", flush=True)
print("STATUS:", overall, flush=True)
sys.exit(0 if overall == "PASS" else 1)
