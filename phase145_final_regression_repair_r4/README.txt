Phase 145 Final Regression Repair R4

Purpose
-------
Repair the remaining Phase 145-2 archive regression without changing
production behavior or canonical test contents.

R3 still left the same 43 collection errors. The remaining missing modules
exist as archived files, but the R3 candidate search required the archived
path itself to be visible through `git ls-files`. That assumption is too
strict for the current partially staged/moved archive worktree.

R4 change
---------
R4 removes only that candidate-filter assumption.

For every missing direct import from a current canonical test:
1. Find the actual file under archive/phases by filename.
2. Resolve ambiguity conservatively.
3. Move it back to its canonical path.
4. Repeat until no new missing dependency is discovered.

If the archive path is tracked, R4 uses `git mv`.
If it physically exists but is not currently tracked at that path, R4 uses
a filesystem move so the canonical file is restored without modifying its
contents.

Scope boundary
--------------
- Production code changes: none.
- Canonical test body/import edits: none.
- No Phase 146 functionality.
- No repository-wide pytest test execution.

Verification
------------
R4 performs:
- canonical test syntax preflight;
- `pytest tests --collect-only -q`;
- the Phase 145 focused regression set.

After R4 passes, run the repository-wide Phase 145 pytest exactly once.
