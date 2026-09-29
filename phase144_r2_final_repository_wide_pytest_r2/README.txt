Phase 144 R2 Final Repository-Wide Pytest R2

This package repairs only the PowerShell final-test runner.

R1 runner problem
-----------------
With $ErrorActionPreference = "Stop", this command:

  git ls-files --error-unmatch "tests/__init__.py"

raises a PowerShell NativeCommandError when tests/__init__.py is intentionally
untracked. Therefore the runner stopped before collection and before pytest.

R2 runner repair
----------------
Tracked status is detected with:

  git ls-files -- "tests/__init__.py"

and the returned text is inspected instead of using a non-zero exit code as
control flow.

Repository changes
------------------
Production: none
Existing tests: none
Documentation: none

Canonical final suite
---------------------
python -m pytest tests -q

The runner performs:
1. repository/environment preflight,
2. safe tests/__init__.py handling,
3. dual import preflight,
4. collection-only preflight,
5. exactly one final repository-wide pytest run,
6. restoration of any pre-existing untracked tests/__init__.py.
