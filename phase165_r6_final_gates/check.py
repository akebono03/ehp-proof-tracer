from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "phase165_r6_audit_results" / "final_gates"
OUTPUT.mkdir(parents=True, exist_ok=True)
TESTS = {
    "architecture": "phase165_r3_architecture_guard/tests/test_phase165_r3_architecture_guard.py",
    "two_group_golden": "phase165_r4_golden_baseline/tests/test_phase165_r4_golden_baseline.py",
    "public_route": "phase165_r57_r1_single_entry/test_phase165_r57_r1_single_entry.py",
}
report = {"phase": "165 R6", "mode": "read_only_targeted", "timestamp":datetime.now(timezone.utc).isoformat(), "full_pytest_run":False, "whole_suite_collection_run":False, "tests":{}}

def run(label, arguments, timeout=90):
    print("[RUN]", label, flush=True)
    try:
        proc = subprocess.run(
            arguments, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
            env={**os.environ,"PYTHONPATH":str(ROOT)+os.pathsep+os.environ.get("PYTHONPATH","")},
        )
        output=(proc.stdout or "")+"\n"+(proc.stderr or "")
        (OUTPUT / (label+".log")).write_text(output,encoding="utf-8")
        status="PASS" if proc.returncode==0 else "FAIL"
        print("["+status+"]",label,"exit",proc.returncode,flush=True)
        for line in output.splitlines()[-18:]:
            print(line,flush=True)
        return {"status":status,"exit":proc.returncode}
    except subprocess.TimeoutExpired:
        print("[TIMEOUT]",label,flush=True)
        return {"status":"TIMEOUT"}

for label,path in TESTS.items():
    if not (ROOT/path).is_file():
        report["tests"][label]={"status":"MISSING","path":path}
        print("[MISSING]",path,flush=True)
    else:
        report["tests"][label]=run(label,[sys.executable,"-m","pytest","-q",path],90)

PROBE=r"""
import json
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view
rows={}
for n,k in [(2,1),(3,1)]:
    tag=f"pi{n+k}_{n}"
    try:
        view=build_standard_web_group_proof_view(n,k)
        text="\n".join(str(line) for line in view.rendered_lines)
        Path("phase165_r6_audit_results/final_gates/"+tag+".txt").write_text(text,encoding="utf-8")
        rows[tag]={"key":view.key,"partial_result":view.partial_result,"step_count":len(view.steps),"rendered_line_count":len(view.rendered_lines),"has_rendered_text":bool(text.strip()),"mode":view.mode}
    except Exception as error:
        rows[tag]={"error":type(error).__name__+": "+str(error)}
print(json.dumps(rows,ensure_ascii=False))
"""
probe=run("web_views",[sys.executable,"-c",PROBE],90)
report["web_views_execution"]=probe
if probe["status"]=="PASS":
    try:
        content=(OUTPUT/"web_views.log").read_text(encoding="utf-8").splitlines()
        report["web_views"]=json.loads(next(x for x in reversed(content) if x.strip().startswith("{")))
        for name,entry in report["web_views"].items():
            print("[VIEW]",name,entry,flush=True)
    except Exception as error:
        report["web_views_parse_error"]=repr(error)

report["git_status"]=run("git_status",["git","status","--short"],30)
previous=ROOT/"phase165_r6_audit_results"/"old_proof_retirement"/"20261019T015604Z"/"report.json"
if previous.is_file():
    try:
        old=json.loads(previous.read_text(encoding="utf-8-sig"))
        report["prior_retirement"]={"report_found":True,"removed":len(old.get("removed",[])),"note":"Historical report only; not a current collection count"}
    except Exception as error:
        report["prior_retirement"]={"report_found":True,"error":str(error)}
else:
    report["prior_retirement"]={"report_found":False}
report["status"]="TARGETED_PASS_PENDING_COLLECTION_AND_BROWSER" if all(x["status"]=="PASS" for x in report["tests"].values()) and probe["status"]=="PASS" else "TARGETED_CHECK_INCOMPLETE"
(OUTPUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("REPORT:",OUTPUT/"report.json",flush=True)
print("STATUS:",report["status"],flush=True)
