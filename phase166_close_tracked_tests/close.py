"""Phase 166 closure: run tracked, current test modules; do not collect installer scripts."""
from __future__ import annotations
import argparse
import datetime
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

EXCLUDED_ROOTS = {"archive", "backups", "backup", ".pytest_cache"}
EXCLUDED_PART_MARKERS = ("backup", "removed", "retired", "archive", "audit_results", "old_proof_retirement")
def candidate_classification(path: str) -> str:
    parts = PurePosixPath(path).parts
    if not parts or path.startswith("."):
        return "hidden_or_backup"
    if parts[0] in EXCLUDED_ROOTS:
        return "archive"
    if any(any(marker in p.lower() for marker in EXCLUDED_PART_MARKERS) for p in parts[:-1]):
        return "historical_or_backup_directory"
    name = parts[-1]
    if not name.endswith(".py"):
        return "non_python"
    if name.startswith("test_"):
        return "test"
    if name.endswith("_test.py"):
        return "installer_or_nonstandard_suffix"
    return "other_python"

def tracked_inventory(repo: Path):
    command=["git","ls-files","-z","--","*.py"]
    proc=subprocess.run(command,cwd=repo,capture_output=True,check=True)
    paths=[p.decode("utf-8","surrogateescape") for p in proc.stdout.split(b"\0") if p]
    rows=[{"path":p,"classification":candidate_classification(p)} for p in paths]
    return rows

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    a=parser.parse_args()
    repo=a.repo.resolve()
    output=Path(__file__).resolve().parent/"results"/datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True,exist_ok=True)
    rows=tracked_inventory(repo)
    tests=[x["path"] for x in rows if x["classification"]=="test"]
    excluded=[x for x in rows if x["classification"]!="test" and ("test" in PurePosixPath(x["path"]).name)]
    report={"phase":"166 closure","mode":"tracked_current_test_files","tracked_test_files":len(tests),
        "excluded_test_named_files":len(excluded),"status":"NOT_RUN","pytest_exit_code":None,
        "full_default_discovery_not_run":True}
    (output/"manifest.json").write_text(json.dumps({"included":tests,"excluded":excluded},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if not tests:
        report["status"]="BLOCKED_EMPTY_TEST_MANIFEST"
        (output/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("No tracked active test files:",output)
        return 2
    cmd=[sys.executable,"-m","pytest","-q","-p","no:cacheprovider",*tests]
    (output/"pytest_command.json").write_text(json.dumps(cmd,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for stage in ("before","after"):
        if stage=="after":continue
        proc=subprocess.run(["git","status","--short"],cwd=repo,capture_output=True,text=True,errors="replace")
        (output/("git_"+stage+".txt")).write_text(proc.stdout+proc.stderr,encoding="utf-8")
    print("Tracked current test modules:",len(tests),flush=True)
    print("Manifest:",output/"manifest.json",flush=True)
    print("Log:",output/"pytest.log",flush=True)
    env={**os.environ,"PYTHONPATH":str(repo)+os.pathsep+os.environ.get("PYTHONPATH","")}
    try:
        with (output/"pytest.log").open("w",encoding="utf-8") as log:
            proc=subprocess.Popen(cmd,cwd=repo,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="utf-8",errors="replace",text=True)
            assert proc.stdout is not None
            for line in proc.stdout:
                log.write(line)
                print(line,end="",flush=True)
            code=proc.wait()
    except OSError as exc:
        code=127
        (output/"launch_error.txt").write_text(repr(exc),encoding="utf-8")
    proc=subprocess.run(["git","status","--short"],cwd=repo,capture_output=True,text=True,errors="replace")
    (output/"git_after.txt").write_text(proc.stdout+proc.stderr,encoding="utf-8")
    report.update({"pytest_exit_code":code,"status":"TESTS_PASS_PENDING_SCOPE_REVIEW" if code==0 else "BLOCKED_TESTS"})
    (output/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("CLOSURE_REPORT:",output/"summary.json",flush=True)
    return code

if __name__=="__main__":
    raise SystemExit(main())
