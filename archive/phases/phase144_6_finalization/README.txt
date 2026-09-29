# Phase 144-6 Finalization

This package performs the measurement pass for closing Phase 144-6.

## Scope

- No production-code changes.
- No existing-test changes.
- No Phase 145 implementation.
- No new R25-31+ investigation.
- Runs every `tests/test_phase144_6*.py` test currently present in the repository.
- Runs the repository-wide Phase-final regression exactly once with:
  `python -m pytest tests -q`
- Captures the Git branch, HEAD, working-tree status, Python version, pytest version,
  focused-test inventory, test results, and final Git status.

The technical investigation stop point is R25-30-R3.

The remaining giant Narrative issue is treated as a result-reuse / proof-subtree
reuse problem, not as an unresolved Argument-boundary ownership leak. The design
and implementation of the result-reuse boundary are deferred to Phase 145.

## Run

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_finalization.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_finalization\run_phase144_6_finalization.ps1"
```

After the run, return:

```text
phase144_6_finalization\phase144_6_finalization_output.txt
```

The measured focused and repository-wide pytest counts from that output will be
used in the documentation-close pass. Documentation is deliberately not updated
before the actual final regression result is known.
