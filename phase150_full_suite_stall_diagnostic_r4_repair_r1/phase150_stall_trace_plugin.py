from __future__ import annotations
import os
import time
from pathlib import Path

START_FRACTION = 0.30
LOG = Path("phase150_full_suite_stall_diagnostic_r4_trace.txt")
total = 0
indices = {}
starts = {}


def rss():
    try:
        import psutil
        return f"{psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024):.1f}MB"
    except Exception:
        return "unknown"


def write(line):
    with LOG.open("a", encoding="utf-8", buffering=1) as handle:
        handle.write(line + "\n")
        handle.flush()


def pytest_collection_finish(session):
    global total, indices
    total = len(session.items)
    indices = {
        item.nodeid: index
        for index, item in enumerate(session.items)
    }
    LOG.write_text(
        "Phase 150 Full-Suite Stall Diagnostic R4 Repair R1\n"
        f"pid={os.getpid()}\n"
        f"collected={total}\n"
        f"trace_start_index={int(total * START_FRACTION)}\n"
        + "=" * 100
        + "\n",
        encoding="utf-8",
    )


def pytest_runtest_logstart(nodeid, location):
    index = indices.get(nodeid, -1)
    if total <= 0 or index < int(total * START_FRACTION):
        return
    starts[nodeid] = time.perf_counter()
    write(
        f"START index={index:05d}/{total - 1:05d} "
        f"progress={100 * index / total:6.2f}% "
        f"rss={rss()} nodeid={nodeid}"
    )


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    index = indices.get(report.nodeid, -1)
    if total <= 0 or index < int(total * START_FRACTION):
        return
    elapsed = time.perf_counter() - starts.get(
        report.nodeid,
        time.perf_counter(),
    )
    write(
        f"END   index={index:05d}/{total - 1:05d} "
        f"progress={100 * index / total:6.2f}% "
        f"elapsed={elapsed:8.2f}s "
        f"rss={rss()} outcome={report.outcome.upper()} "
        f"nodeid={report.nodeid}"
    )


def pytest_sessionfinish(session, exitstatus):
    write("=" * 100)
    write(f"SESSION_END exitstatus={exitstatus}")
