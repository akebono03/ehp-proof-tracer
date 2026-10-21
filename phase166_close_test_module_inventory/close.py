"""Phase 166 closure: select pytest modules by test definitions, never installer filename heuristics."""
from __future__ import annotations
import argparse
import ast
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

def identify_test_modules(repo: Path):
    included, omitted, unreadable = [], [], []
    for p in sorted(repo.rglob("*.py")):
        relative = p.relative_to(repo)
        if any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in relative.parts):
            continue
        if not (p.name.startswith("test_") or p.name.endswith("_test.py")):
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, SyntaxError) as exc:
            unreadable.append({"path":relative.as_posix(),"error":repr(exc)})
            continue
        tests = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                tests.append(node.name)
            if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                tests.append(node.name)
        if tests:
            included.append({"path":relative.as_posix(),"tests":tests})
        else:
            omitted.append({"path":relative.as_posix(),"reason":"no module-level test_ functions or Test classes"})
    return included, omitted, unreadable

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = Path(__file__).resolve().parent / "results" / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out.mkdir(parents=True, exist_ok=True)
    included, omitted, unreadable = identify_test_modules(repo)
    inventory={"included":included,"omitted":omitted,"unreadable":unreadable}
    (out/"test_inventory.json").write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    report={"phase":"166 closure","mode":"explicit_test_module_inventory","included_files":len(included),"omitted_files":len(omitted),"unreadable_files":len(unreadable),"full_pytest_run":False}
    if unreadable or not included:
        report["status"]="BLOCKED_INVENTORY"
        (out/"summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("BLOCKED_INVENTORY",out,flush=True)
        return 2
    command=[sys.executable,"-m","pytest","-q","-p","no:cacheprovider",*[item["path"] for item in included]]
    report["command_file"]=str(out/"pytest_command.json")
    (out/"pytest_command.json").write_text(json.dumps(command,indent=2)+"\n",encoding="utf-8")
    for label in ("before","after"):
        if label=="after":
            continue
        status=subprocess.run(["git","status","--short"],cwd=repo,capture_output=True,text=True,errors="replace")
        (out/("git_"+label+".txt")).write_text(status.stdout+status.stderr,encoding="utf-8")
    print("Explicit test modules:",len(included),"omitted non-test scripts:",len(omitted),flush=True)
    print("Full file list:",out/"test_inventory.json",flush=True)
    print("Pytest log:",out/"pytest.log",flush=True)
    with (out/"pytest.log").open("w",encoding="utf-8") as f:
        proc=subprocess.Popen(command,cwd=repo,env={**os.environ,"PYTHONPATH":str(repo)+os.pathsep+os.environ.get("PYTHONPATH","")},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace")
        assert proc.stdout is not None
        for line in proc.stdout:
            f.write(line)
            print(line,end="",flush=True)
        code=proc.wait()
    status=subprocess.run(["git","status","--short"],cwd=repo,capture_output=True,text=True,errors="replace")
    (out/"git_after.txt").write_text(status.stdout+status.stderr,encoding="utf-8")
    report.update({"full_pytest_run":True,"pytest_exit_code":code,"status":"PASS" if code==0 else "BLOCKED"})
    (out/"summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("CLOSURE_REPORT:",out/"summary.json",flush=True)
    return code

if __name__=="__main__":
    raise SystemExit(main())
