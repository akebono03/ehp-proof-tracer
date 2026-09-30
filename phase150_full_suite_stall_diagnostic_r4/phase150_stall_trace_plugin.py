from __future__ import annotations
import os,time
from pathlib import Path
START_FRACTION=0.30
LOG=Path("phase150_full_suite_stall_diagnostic_r4_trace.txt")
total=0; indices={}; starts={}
def rss():
    try:
        import psutil
        return f"{psutil.Process(os.getpid()).memory_info().rss/(1024*1024):.1f}MB"
    except Exception:
        return "unknown"
def write(s):
    with LOG.open("a",encoding="utf-8",buffering=1) as f:
        f.write(s+"\n"); f.flush()
def pytest_collection_finish(session):
    global total,indices
    total=len(session.items); indices={x.nodeid:i for i,x in enumerate(session.items)}
    LOG.write_text(f"Phase 150 Full-Suite Stall Diagnostic R4\npid={os.getpid()}\ncollected={total}\ntrace_start_index={int(total*START_FRACTION)}\n"+"="*100+"\n",encoding="utf-8")
def pytest_runtest_logstart(nodeid,location):
    i=indices.get(nodeid,-1)
    if total<=0 or i<int(total*START_FRACTION): return
    starts[nodeid]=time.perf_counter()
    write(f"START index={i:05d}/{total-1:05d} progress={100*i/total:6.2f}% rss={rss()} nodeid={nodeid}")
def pytest_runtest_logreport(report):
    if report.when!="call": return
    i=indices.get(report.nodeid,-1)
    if total<=0 or i<int(total*START_FRACTION): return
    elapsed=time.perf_counter()-starts.get(report.nodeid,time.perf_counter())
    write(f"END   index={i:05d}/{total-1:05d} progress={100*i/total:6.2f}% elapsed={elapsed:8.2f}s rss={rss()} outcome={report.outcome.upper()} nodeid={report.nodeid}")
def pytest_sessionfinish(session,exitstatus):
    write("="*100); write(f"SESSION_END exitstatus={exitstatus}")
