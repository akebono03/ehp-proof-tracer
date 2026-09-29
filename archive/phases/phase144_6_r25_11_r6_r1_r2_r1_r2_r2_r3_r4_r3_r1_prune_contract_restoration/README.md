# Phase 144-6 R4-R3-R1 Prune Contract Restoration

The R4-R3 focused run produced 43 passes and two failures. Both failures have
the same cause: R4-R3 preserved stale-path cleanup but omitted the existing
`git worktree prune --expire now` contract.

This repair changes only the complete historical-audit
`Remove-TemporaryWorktree` function.

It preserves R4-R3 behavior:

- query `git worktree list --porcelain`;
- registered audit worktree -> `git worktree remove --force`;
- unregistered path -> filesystem cleanup only when the leaf is exactly the
  audit-specific `.phase144_6_r25_11_r6_r1_worktree`.

It restores the earlier R3 contract after either cleanup branch:

- `git worktree prune --expire now`;
- native output redirected away from the success stream;
- `$LASTEXITCODE` copied immediately to scalar `$pruneExitCode`;
- retry failure only for non-zero scalar exit code.

Unchanged:
- production code;
- existing project tests;
- existing historical audit tests;
- `Measure-Commit`;
- `Read-PopulationCache`;
- collector;
- population cache contents;
- expected historical population 190.

The focused historical-localization directory is run before localization.
No full project pytest is run.
