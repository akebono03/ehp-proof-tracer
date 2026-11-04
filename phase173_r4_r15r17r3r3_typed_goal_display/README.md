# Phase 173 R15R17-R3R3: Typed Pending Goal Display

This patch changes only the presentation of already pending typed group equations. No proof search, status, citation, completion certificate, or open-goal record is changed.

One new general helper projects the actual `CyclicStructureStatement` and equality `Relation` goals into a display group only when their typed target group and typed group structure are identical. A reversed equality may share a display group. Identical LaTeX is never an identity rule. The public line always reports the full number of pending typed goals grouped.

Run `run.ps1 -DryRun` first, and then `run.ps1`. This checks the reviewed GitHub `develop` HEAD `a4e01bca` (allowing local `aa25a993` or `a4e01bca`), the existing R1 and R2 installation records, the renderer Git blob, and the Git index. It creates `FULL_CHANGED_UNITS.md` containing the entire new function, entire replacement renderer, and the complete tests. The normal run executes only focused pytest and restores its renderer change on test failure.

`run.ps1 -Restore` restores only the R3R3 renderer modification and refuses to overwrite later edits. Other versions of this package should not be overlaid without review.

Historical test assertions that require the now-obsolete separate abstract-proof heading remain an explicitly separate follow-up contract migration. This patch intentionally does not modify their test files or legacy helper APIs.
