Phase 155 Closure R1 — progress plugin repair

Cause
-----
The first Closure attempt aborted after 1/10421 tests because the custom
progress plugin accessed `report.config` inside `pytest_runtest_logreport`.

`pytest.TestReport` does not provide a `config` attribute.

Repair
------
Only the Closure package progress plugin is replaced.

The repaired plugin:
- uses plain `print(..., flush=True)` for progress;
- does not access `report.config`;
- reports collection size;
- reports every 100 completed call-phase tests;
- reports failures immediately;
- reports the final completed/failure counts.

The repair follows the style of the repository's earlier Phase150 trace plugins,
which emit progress directly rather than retrieving terminalreporter from a
TestReport.

Before the heavy full-suite retry, five lightweight plugin tests execute the
hooks directly with simple fake report/session objects.

Repository impact
-----------------
- production changes: none
- existing repository-test changes: none
- documentation changes before full-suite PASS: none

The previous full-suite attempt completed only one test before the plugin
INTERNALERROR, so the phase-final full run must restart from the beginning.
