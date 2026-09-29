# Phase 144-6 Historical Audit Abort / Restore

This package stops and removes the temporary historical-localization audit
environment.

It does not use `git reset --hard` or `git clean -fd`.

It removes only:

- `.phase144_6_r25_11_r6_r1_worktree`, when present;
- its Git worktree registration, when present;
- `phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit`.

It then runs `git worktree prune --expire now` and prints `git status --short`.

Production code and existing project tests are not modified.
No full pytest is run.
