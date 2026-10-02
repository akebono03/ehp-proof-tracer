Phase 155-R3-3C — verified duplicate removal

Purpose
-------
Apply only the duplicate-test removals already proven safe by:

- Phase 155-R3-2F-r1 verification closure,
- Phase 155-R3-3A duplicate graph audit,
- Phase 155-R3-3B file/dependency safety audit.

Expected scope
--------------
- 161 safe duplicate test functions removed.
- 5 test files deleted entirely where every top-level test is removable and
  the file has no external module/symbol import.
- Remaining candidate files keep helpers, constants, imports, classes, and
  retained tests unchanged.
- The one externally imported helper-provider test file is preserved; only
  its approved duplicate test function(s) are removed.
- Production code is unchanged.

No unrelated cleanup
--------------------
R3-3C does not remove newly unused imports/helpers/constants merely because
the duplicate test removal may make them unnecessary. That is outside this
subphase unless required for syntax/collection correctness.

Focused verification
--------------------
After removal the package verifies:

1. all 5 whole-file targets are absent,
2. all approved function targets are absent,
3. every remaining affected file parses/compiles,
4. all non-deletion survivor tests from the R3-3A graph pass,
5. all remaining affected test files pass,
6. test-file importers identified by R3-3B pass,
7. non-test Python importers compile.

Repository-wide pytest is NOT run here. Per project policy it remains for
Phase 155 closure only.

Rollback
--------
Before changing any test file, the runner creates a timestamped sibling
backup directory containing every affected file.

The backup path is printed during execution and recorded in:

`phase155_r3_3c_removal_output/phase155_r3_3c_removal_manifest.json`
