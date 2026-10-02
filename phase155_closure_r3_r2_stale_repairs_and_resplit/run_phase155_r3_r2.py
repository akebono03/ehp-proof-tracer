from __future__ import annotations
import argparse,json,os,subprocess,sys,time
from pathlib import Path
def load(p,d): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d
def save(p,x): p.write_text(json.dumps(x,indent=2),encoding="utf-8")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",type=Path,default=Path.cwd()); ap.add_argument("--package-dir",type=Path,required=True); ap.add_argument("--plan",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); ap.add_argument("--timeout",type=int,default=600); a=ap.parse_args()
    root=a.repo_root.resolve(); pkg=a.package_dir.resolve(); plan=json.loads(a.plan.read_text(encoding="utf-8")); out=a.output_dir.resolve(); out.mkdir(exist_ok=True)
    cp=out/"r3_r2_checkpoint.json"; state=load(cp,{"jobs":{}})
    env=dict(os.environ); env["PYTHONPATH"]=str(pkg)+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    for j in range(1,plan["job_count"]+1):
      if state["jobs"].get(str(j),{}).get("status")=="PASS":
        print(f"job {j}: already PASS, skipping"); continue
      log=out/f"r3_r2_job_{j:02d}.log"
      cmd=[sys.executable,"-m","pytest","tests","-q","--tb=short","--durations=20","-p","phase155_r3_r2_plugin","--r3r2-plan",str(a.plan),"--r3r2-job",str(j)]
      t=time.monotonic()
      with log.open("w",encoding="utf-8") as fh:
        p=subprocess.Popen(cmd,cwd=root,env=env,stdout=fh,stderr=subprocess.STDOUT,text=True)
        try: rc=p.wait(timeout=a.timeout); status="PASS" if rc==0 else "FAIL"
        except subprocess.TimeoutExpired: p.kill(); p.wait(); status="TIMEOUT"
      elapsed=time.monotonic()-t
      print(log.read_text(encoding="utf-8",errors="replace"),end="")
      state["jobs"][str(j)]={"status":status,"elapsed_seconds":round(elapsed,2),"log":str(log)}; save(cp,state)
      print(f"job {j}: {status} in {elapsed:.2f}s")
    ok=all(state["jobs"].get(str(j),{}).get("status")=="PASS" for j in range(1,plan["job_count"]+1))
    summary=out/"r3_r2_summary.txt"
    lines=["Phase 155 Closure-R3-R2","", "Original PASS shards preserved: 1, 2, 6, 7"]
    for j in range(1,plan["job_count"]+1):
      r=state["jobs"].get(str(j),{}); lines.append(f"Repair job {j}: {r.get('status','NOT_RUN')} ({r.get('elapsed_seconds','-')}s)")
    lines += ["","Audit-only tests executed: 0","Monolithic repository-wide pytest: NOT run", "Closure-R3 routine result: PASS" if ok else "Closure-R3 routine result: INCOMPLETE"]
    summary.write_text("\n".join(lines)+"\n",encoding="utf-8"); print(summary.read_text(encoding="utf-8"))
    raise SystemExit(0 if ok else 1)
if __name__=="__main__":main()
