from __future__ import annotations
import json
from pathlib import Path
import pytest
def pytest_addoption(parser):
    g=parser.getgroup("r3r2"); g.addoption("--r3r2-plan",required=True); g.addoption("--r3r2-job",type=int,required=True)
def pytest_collection_modifyitems(config,items):
    root=Path(str(config.rootpath)).resolve()
    audits={x.strip() for x in (root/"tests"/"phase155_audit_only_nodeids.txt").read_text(encoding="utf-8").splitlines() if x.strip()}
    plan=json.loads(Path(config.getoption("--r3r2-plan")).read_text(encoding="utf-8")); job=config.getoption("--r3r2-job")
    m={k.replace("\\\\","/"):int(v) for k,v in plan["file_to_job"].items()}
    keep=[]; drop=[]
    for item in items:
      f=item.nodeid.split("::",1)[0].replace("\\\\","/")
      if item.nodeid not in audits and m.get(f)==job: keep.append(item)
      else: drop.append(item)
    if drop: config.hook.pytest_deselected(items=drop)
    items[:]=keep
