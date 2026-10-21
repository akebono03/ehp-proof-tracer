# Phase 166 R3-AJ — DB-priority compatibility repair

## Modified files and functions

- `phase165_r55_nk_only_goal.py`: the **last** `registered_group_goal_candidates` function, replaced in full using AST line bounds. Its complete replacement is in `registered_group_goal_candidates.py.txt`.
- `phase166_r3aj_structured_generator.py`: newly installed module; complete file bundled.
- `tests/test_structured_generator.py`: original three tests, unchanged.

No import-section changes; required imports remain inside the replaced function. The previous patch failed because it matched an older "if not output" branch; the current selector returns a database candidate early. This version preserves that DB-first behavior, using structured IDs first for k>=2 when complete metadata are present, then the existing simple adapter, then registry/symbolic fallback. It never turns database data into evidence.

Run `run.ps1` from the repository root after extraction. Only focused pytest is run; full pytest remains for the end of Phase 166.

Completion: the new tests pass and the local π₃² proof continues to complete. Next work: audit all 112 rendered typed goals and their normalization, without extending proof derivations.
