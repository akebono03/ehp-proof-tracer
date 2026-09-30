import os
import time

_TRACE_START_PERCENT = 30.0
_session_total = 0
_session_index = 0
_started = {}
_log_path = os.environ.get(
    "PHASE150_TRACE_LOG",
    "phase150_final_regression_r4_trace.log",
)


def _emit(message):
    print(message, flush=True)
    with open(_log_path, "a", encoding="utf-8") as handle:
        handle.write(message + "\n")
        handle.flush()


def pytest_collection_finish(session):
    global _session_total
    _session_total = len(session.items)
    _emit(f"COLLECTED {_session_total} tests")


def pytest_runtest_logstart(nodeid, location):
    global _session_index
    _session_index += 1
    progress = (
        100.0 * _session_index / _session_total
        if _session_total
        else 0.0
    )
    if progress >= _TRACE_START_PERCENT:
        _started[nodeid] = time.perf_counter()
        _emit(
            f"START index={_session_index:05d}/{_session_total:05d} "
            f"progress={progress:6.2f}% {nodeid}"
        )


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    started = _started.pop(report.nodeid, None)
    if started is None:
        return
    elapsed = time.perf_counter() - started
    outcome = report.outcome.upper()
    _emit(
        f"END   index={_session_index:05d}/{_session_total:05d} "
        f"elapsed={elapsed:8.2f}s outcome={outcome} {report.nodeid}"
    )
