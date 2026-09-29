# Phase 144-6 R4-R4 Collector Native Error Handling

The previous run passed all 48 focused historical-localization tests and
reached the Python collector for the first foundation-available historical
commit.

Windows PowerShell 5.1 then converted Python stderr (`Traceback`) into a
terminating `NativeCommandError` because the locator runs with
`$ErrorActionPreference = "Stop"`. This interrupted `Measure-Commit` before
its existing collector exit-code and `UNAVAILABLE:<last line>` handling could
run.

This repair changes only the native Python invocation block inside the
existing `Measure-Commit` function.

The block now:

- saves the current `$ErrorActionPreference`;
- temporarily uses `Continue`;
- captures combined stdout/stderr in `$collectorOutput`;
- immediately copies `$LASTEXITCODE` to scalar `$collectorExitCode`;
- restores the original error preference in `finally`.

The existing collector failure conversion is preserved so the next
localization run can expose the actual historical Python incompatibility
instead of stopping at PowerShell's native stderr wrapper.

Unchanged:
- production code;
- existing project tests;
- existing historical audit tests;
- collector Python;
- `Remove-TemporaryWorktree`;
- `Read-PopulationCache`;
- all other `Measure-Commit` behavior;
- population cache contents;
- expected historical population 190.

Only focused historical-localization tests are run. No full project pytest is
run.
