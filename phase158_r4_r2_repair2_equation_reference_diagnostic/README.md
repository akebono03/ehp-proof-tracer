# Phase 158-R4-R2 repair2 — equation-reference diagnostic

Diagnostic only.

It prints, for `pi_6^3` and `pi_8^5`:

- all visible `\tag{N}` values;
- every line containing a tag;
- every line/paragraph beginning with `(N)` and containing `より,`.

This is intended to identify exactly which public connector form is not being
recognized by the current equation-number normalizer.

No production code is changed.
No existing test is changed.
The full pytest suite is not run.
