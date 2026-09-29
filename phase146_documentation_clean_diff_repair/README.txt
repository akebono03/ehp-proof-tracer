Phase 146 Documentation Clean-Diff Repair

Purpose
-------
Remove the large documentation diff caused by the earlier Phase 146
documentation closure write, while preserving the canonical Phase 146
closure already present in repository HEAD.

Files restored from canonical HEAD
----------------------------------
docs/design.md
docs/development_log.md
docs/roadmap.md
docs/proof_records.md

README.md
---------
Unchanged. Phase 146 does not introduce a new user-facing feature requiring
a README update.

Safety
------
Before modifying any file, the apply script reads each file from git HEAD
and verifies Phase 146 closure markers.

If any required marker is absent, the script aborts before modifying the
documentation. This prevents accidentally discarding Phase 146 content from
a local branch whose HEAD predates the closure documentation.

Why no new regression result is appended
----------------------------------------
The previously observed whole-suite result was obtained before Test
Performance Repairs 1-9 were complete. The final Phase 146 whole-suite run
should be executed once after the performance cleanup and its actual result
should then be recorded. This clean-diff repair therefore does not write a
stale timing/result into the documents.

Tests
-----
No pytest is run. This package changes documentation only.

Completion criteria
-------------------
- All four canonical HEAD files contain Phase 146 closure markers.
- The four files are restored byte-for-byte from HEAD.
- git diff for those four files is empty.
- UTF-8 strict decoding passes.
- Production code is unchanged.
- Test code is unchanged.
- README.md is unchanged.

Next boundary
-------------
After this repair:
1. Run the final Phase 146 repository-wide test suite once.
2. Record the actual post-Repair-1-9 regression result with a small
   newline-preserving documentation update.
3. Close Phase 146.
4. Begin Phase 147 RC1 Argument-method ownership.
