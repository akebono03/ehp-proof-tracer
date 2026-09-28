# Phase 144-6 R25-22-R3 Focused-Test Assertion Repair

R25-22-R2 production behavior passed the first four focused tests.

The remaining failure was caused by the R25-22-R2 HTML assertion expecting two
backslash bytes before `tag`. Existing Web tests correctly inspect LaTeX in the
rendered HTML with raw byte literals such as `rb"\pi_{6}^{3}"`.

R25-22-R3 therefore changes no production code. It repairs only the temporary
R25-22-R2 focused assertions:

- `rb"\tag{1}"`
- `rb"\tag{2}"`
- `rb"\tag{3}"`

After that repair, the runner continues through the regression checks that
R25-22-R2 did not reach because it stopped at the focused-test failure.

Repository-wide pytest is intentionally not run.
