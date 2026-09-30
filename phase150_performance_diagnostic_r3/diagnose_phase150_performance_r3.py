from __future__ import annotations
import argparse, subprocess, sys, time
from pathlib import Path

def collect(repo):
    r=subprocess.run([sys.executable,"-m","pytest","tests","--collect-only","-q"],cwd=repo,capture_output=True,text=True,encoding="utf-8",errors="replace")
    if r.returncode: print(r.stdout); print(r.stderr,file=sys.stderr); raise SystemExit(r.returncode)
    ids=[x.strip() for x in r.stdout.splitlines() if "::" in x and not x.startswith("=")]
    if not ids: raise SystemExit("No node IDs collected")
    return ids

def run_one(repo,nodeid,timeout):
    t=time.perf_counter()
    try:
        r=subprocess.run([sys.executable,"-m","pytest",nodeid,"-q","--durations=1","--durations-min=0.0"],cwd=repo,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=timeout)
        return ("PASS" if r.returncode==0 else "FAIL",time.perf_counter()-t,r.stdout,r.stderr)
    except subprocess.TimeoutExpired as e:
        out=e.stdout or ""; err=e.stderr or ""
        if isinstance(out,bytes): out=out.decode("utf-8","replace")
        if isinstance(err,bytes): err=err.decode("utf-8","replace")
        return ("TIMEOUT",time.perf_counter()-t,out,err)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--percent",type=float,default=32); p.add_argument("--before",type=int,default=20); p.add_argument("--after",type=int,default=20); p.add_argument("--timeout",type=float,default=60); a=p.parse_args()
    repo=Path.cwd(); out=repo/"phase150_performance_diagnostic_r3_output"; out.mkdir(exist_ok=True)
    ids=collect(repo); total=len(ids); center=round(a.percent/100*(total-1)); start=max(0,center-a.before); stop=min(total,center+a.after+1); selected=ids[start:stop]
    (out/"collected_tests.txt").write_text("\n".join(f"{i:05d}\t{x}" for i,x in enumerate(ids))+"\n",encoding="utf-8")
    (out/"window_nodeids.txt").write_text("\n".join(f"{start+i:05d}\t{x}" for i,x in enumerate(selected))+"\n",encoding="utf-8")
    report=["Phase 150 Performance Diagnostic R3","="*78,"Production changes: none","Existing test changes: none","Documentation changes: none","Full regression: NOT run",f"Collected tests: {total}",f"Target progress: {a.percent:.1f}%",f"Center index: {center}",f"Window: [{start}, {stop})",f"Measured node IDs: {len(selected)}",f"Per-test timeout: {a.timeout:.1f}s","","Per-test results","-"*78]; detail=[]; failures=timeouts=0
    for off,nodeid in enumerate(selected):
        i=start+off; print(f"[{i:05d}/{total-1:05d}] START {nodeid}",flush=True)
        status,elapsed,stdout,stderr=run_one(repo,nodeid,a.timeout); print(f"[{i:05d}/{total-1:05d}] {status} {elapsed:.2f}s {nodeid}",flush=True)
        report.append(f"{i:05d}\t{status}\t{elapsed:.2f}s\t{nodeid}")
        detail += ["="*78,f"INDEX: {i}",f"STATUS: {status}",f"ELAPSED: {elapsed:.2f}s",f"NODEID: {nodeid}","--- stdout ---",stdout.rstrip(),"--- stderr ---",stderr.rstrip(),""]
        failures += status=="FAIL"; timeouts += status=="TIMEOUT"
    report += ["","Summary","-"*78,f"Failures: {failures}",f"Timeouts: {timeouts}","TIMEOUT is a concrete 32% stall candidate; slow PASS rows are remaining hotspots."]
    (out/"REPORT.txt").write_text("\n".join(report)+"\n",encoding="utf-8"); (out/"timing_detail.txt").write_text("\n".join(detail)+"\n",encoding="utf-8")
    print("\n".join(report[-6:])); return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
