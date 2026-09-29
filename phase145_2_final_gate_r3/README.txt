Phase 145-2 Final Gate R3

Purpose
-------
The archive move itself has already completed and verified:

- 553 historical artifacts archived
- 1811 historical tracked files verified
- production code changes: none
- canonical test changes: none

Resume R2 then stopped in the canonical Python syntax preflight because Windows
rejected a single python -m py_compile command containing the entire canonical
Python file list as too long.

R3 changes only the final-gate runner.

Syntax preflight repair
-----------------------
Instead of passing every canonical Python path to one Python process, R3 invokes
python -m py_compile once per canonical Python file. This avoids the Windows
command-line length limit without changing the set of files checked.

R3 does not repeat or modify the archive move.

Final gate
----------
1. Verify archive/phases/README.md exists.
2. Verify no tracked Phase-like historical paths remain outside archive/phases/.
3. Compile canonical Python files one at a time.
4. Run the repository-wide canonical test suite:
   python -m pytest tests -q
5. Show final git status.

No production implementation or canonical test is modified by this package.
