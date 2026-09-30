Phase 148 RC2-5 Repair R4.2

Test-only repair.
Production changes: none.

The remaining Phase143_47 pi8_5 assertion expected the second raw exactness
window to remain visible. RC2 classifies the recursive exactness evidence as
UNOWNED_RECURSIVE, so raw exactness body contributions are suppressed.
The assertion is therefore updated from >= 1 to == 0.

Runs the same focused regression only.
Repository-wide pytest is NOT run.
