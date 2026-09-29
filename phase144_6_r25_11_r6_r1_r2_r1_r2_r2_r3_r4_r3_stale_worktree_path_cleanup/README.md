# Phase 144-6 R4-R3 Stale Worktree Path Cleanup Repair

The previous run passed 41 focused historical-localization tests and then
stopped before measuring the first foundation-available commit because the
audit worktree path existed while `git worktree remove --force` returned 128.

This repair changes only the complete historical-audit
`Remove-TemporaryWorktree` function.

The function now distinguishes two states:

1. the audit path is registered by `git worktree list --porcelain`: remove it
   with normal `git worktree remove --force`;
2. the path exists but is not registered: only if its leaf name is exactly
   `.phase144_6_r25_11_r6_r1_worktree`, remove that stale audit directory with
   PowerShell filesystem cleanup.

This guard prevents arbitrary unregistered directories from being removed.

Unchanged:
- production code;
- existing project tests;
- `Measure-Commit`;
- restored `Read-PopulationCache`;
- collector;
- population cache contents;
- expected population 190.

A new audit-only test checks registration detection, registered Git removal,
the audit-path guard, and preservation of the R4/R4-R2 repairs.

Only the historical-localization audit directory is tested. No full project
pytest is run.
