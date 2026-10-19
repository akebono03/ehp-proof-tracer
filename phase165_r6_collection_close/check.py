from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"phase165_r6_audit_results"/"collection_close"
OUT.mkdir(parents=True,exist_ok=True)
paths=[]
if (ROOT/"tests").is_dir():
    paths.append("tests")
paths.extend(x.name for x in sorted(ROOT.glob("test_*.py")) if x.is_file())
report={"phase":"165 R6","timestamp":datetime.now(timezone.utc).isoformat(),
        "scope":paths,"full_pytest_run":False,"test_bodies_executed":False,
        "status":"NOT_STARTED"}
if not paths:
    report["status"]="NO_TESTS_FOUND"
else:
    command=[sys.executable,"-m","pytest","--collect-only","-q",
             "--continue-on-collection-errors",*paths]
    environment={**os.environ,"PYTHONPATH":str(ROOT)+os.pathsep+os.environ.get("PYTHONPATH","")}
    log=OUT/"collection.log"
    print("START scoped collection: tests/ and root test_*.py only",flush=True)
    print("No tests executed; timeout 180 seconds; progress every 10 seconds",flush=True)
    timeout=False
    with log.open("w",encoding="utf-8") as file:
        with subprocess.Popen(command,cwd=ROOT,env=environment,stdout=file,stderr=subprocess.STDOUT) as proc:
            start=time.monotonic()
            try:
                while proc.poll() is None:
                    elapsed=int(time.monotonic()-start)
                    if elapsed>=180:
                        timeout=True
                        proc.kill()
                        proc.wait()
                        break
                    print(f"Collecting: {elapsed} seconds",flush=True)
                    time.sleep(10)
            except KeyboardInterrupt:
                proc.kill()
                proc.wait()
                timeout=True
            code=proc.returncode
    content=log.read_text(encoding="utf-8",errors="replace")
    errors=sorted(set(re.findall(r"^ERROR collecting (.+?)(?:\s+_+)?$",content,re.MULTILINE)))
    tail=content.splitlines()[-35:]
    report.update({"exit_code":code,"timeout_or_interrupted":timeout,
                   "error_file_count":len(errors),"error_files":errors,
                   "summary_tail":tail[-12:],
                   "status":"PASS" if code==0 and not timeout and not errors else "BLOCKED"})
    print("Exit:",code,"collection error files:",len(errors),"timeout:",timeout,flush=True)
    for line in tail[-12:]:
        print(line[:230],flush=True)
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Report:",OUT/"report.json",flush=True)
print("Status:",report["status"],flush=True)
