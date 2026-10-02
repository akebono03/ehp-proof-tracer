from __future__ import annotations

import time


_started = None
_total = 0
_completed = 0
_failed = 0


def _emit(message: str) -> None:
    print(
        message,
        flush=True,
    )


def pytest_collection_finish(session):
    global _total

    _total = len(
        session.items
    )

    _emit(
        f"[Phase155 Closure] collected {_total} tests"
    )
    _emit(
        "[Phase155 Closure] progress will be reported every 100 tests"
    )


def pytest_sessionstart(session):
    global _started
    global _completed
    global _failed

    _started = time.perf_counter()
    _completed = 0
    _failed = 0


def pytest_runtest_logreport(report):
    global _completed
    global _failed

    if report.when != "call":
        return

    _completed += 1

    if report.failed:
        _failed += 1

    if (
        _completed == 1
        or _completed % 100 == 0
        or _completed == _total
        or report.failed
    ):
        _emit(
            "[Phase155 Closure] "
            f"{_completed}/{_total} completed, "
            f"failures={_failed}"
        )


def pytest_sessionfinish(session, exitstatus):
    elapsed = (
        time.perf_counter()
        - _started
        if _started is not None
        else 0.0
    )

    _emit(
        "[Phase155 Closure] "
        f"session finished: exit={exitstatus}, "
        f"completed={_completed}/{_total}, "
        f"failures={_failed}, "
        f"elapsed={elapsed:.2f}s"
    )
