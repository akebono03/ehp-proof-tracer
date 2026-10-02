from __future__ import annotations
import argparse,json
from pathlib import Path
SPLIT={3:3,4:3,5:1,8:1}
def part(files,n):
    n=min(n,len(files)); out=[]; i=0
    for j in range(n):
      rem=len(files)-i; left=n-j; take=(rem+left-1)//left
      out.append(files[i:i+take]); i+=take
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--original-plan",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); a=ap.parse_args()
    p=json.loads(a.original_plan.read_text(encoding="utf-8"))
    by={k:[] for k in SPLIT}
    for f,s in sorted(p["file_to_shard"].items()):
      s=int(s)
      if s in by: by[s].append(f.replace("\\\\","/"))
    m={}; jobs=[]; idx=1
    for s in (3,4,5,8):
      chunks=part(by[s],SPLIT[s])
      for pi,ch in enumerate(chunks,1):
        for f in ch:m[f]=idx
        jobs.append({"job":idx,"original_shard":s,"part":pi,"parts":len(chunks),"files":len(ch)})
        idx+=1
    out={"job_count":len(jobs),"file_to_job":m,"jobs":jobs}
    a.output.write_text(json.dumps(out,indent=2),encoding="utf-8")
    print("repair jobs:",len(jobs))
    for j in jobs: print(j)
if __name__=="__main__":main()
