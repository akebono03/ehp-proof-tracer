from __future__ import annotations

from types import SimpleNamespace

import phase155_closure_progress_plugin as plugin


def test_collection_finish_records_total_without_terminalreporter():
  session = SimpleNamespace(
    items=[
      object(),
      object(),
      object(),
    ]
  )

  plugin.pytest_collection_finish(
    session
  )

  assert plugin._total == 3


def test_logreport_does_not_require_report_config():
  plugin._total = 2
  plugin._completed = 0
  plugin._failed = 0

  report = SimpleNamespace(
    when="call",
    failed=False,
  )

  plugin.pytest_runtest_logreport(
    report
  )

  assert plugin._completed == 1
  assert plugin._failed == 0


def test_failed_logreport_counts_failure_without_report_config():
  plugin._total = 2
  plugin._completed = 0
  plugin._failed = 0

  report = SimpleNamespace(
    when="call",
    failed=True,
  )

  plugin.pytest_runtest_logreport(
    report
  )

  assert plugin._completed == 1
  assert plugin._failed == 1


def test_non_call_report_is_ignored():
  plugin._total = 2
  plugin._completed = 0
  plugin._failed = 0

  report = SimpleNamespace(
    when="setup",
    failed=False,
  )

  plugin.pytest_runtest_logreport(
    report
  )

  assert plugin._completed == 0
  assert plugin._failed == 0


def test_sessionfinish_does_not_require_terminalreporter():
  plugin._started = None
  plugin._total = 2
  plugin._completed = 2
  plugin._failed = 0

  plugin.pytest_sessionfinish(
    SimpleNamespace(),
    0,
  )
