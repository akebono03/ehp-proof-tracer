# Phase 144-6 R4-R5 Idempotent Post-Measure Cleanup

Historical localization has now established a real baseline:

- `39a1b8bfad` (`Phase 144-6-R5-43-R3`) -> `selected=190`.

The immediately earlier measurable candidate is unavailable because its
historical API does not accept `current_markdown`.

The remaining task is therefore to continue after the exact-190 baseline and
find the first later commit whose selected population is 192.

The previous run stopped after measuring 190 because post-measure worktree
cleanup returned Git exit code 128. R4-R5 makes only the historical audit
cleanup idempotent.

`Remove-TemporaryWorktree` now re-queries `git worktree list --porcelain`
after a failed `git worktree remove --force`. If the target is still
registered, the failure remains fatal. If Git has already unregistered it,
the function treats that transition as successful and removes only a
remaining audit-specific directory.

The audit-path guard remains exact:
`.phase144_6_r25_11_r6_r1_worktree`.

The existing `git worktree prune --expire now` scalar exit-code contract is
preserved.

Unchanged:
- production code;
- existing project tests;
- `Measure-Commit`;
- collector Python;
- restored `Read-PopulationCache`;
- population cache contents;
- expected historical population 190.

The runner reuses cached measurements, runs focused audit tests, and resumes
historical localization. No full project pytest is run.
