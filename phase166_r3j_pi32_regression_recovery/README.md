# Phase 166 R3-J Web Regression Recovery

This package restores only `search_group_from_registered_goal()` to its pre-R3-J dispatcher implementation.
It retains the five Proposition 5.1 typed assertions and their agreed ordering.
It does not implement the final registry-only Web search design. The legacy on-demand earlier-proof route remains temporarily in use, pending a properly tested replacement.
Run `run.ps1` from the repository root. Backups are created before changes. Only focused pytest runs.
