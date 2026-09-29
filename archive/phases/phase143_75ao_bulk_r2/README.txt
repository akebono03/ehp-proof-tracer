Phase 143-75AO bulk R2

Problem:
The first bulk patcher inserted literal backslash-n text into the
toda_rules import block, causing SyntaxError before the semantic patch
could complete.

R2:
1. Repairs only that malformed import insertion.
2. Verifies syntax.
3. Re-runs the original 75AO bulk patcher.
4. Verifies syntax again.
5. Runs the same focused tests.

No additional semantic scope is introduced.
No docs changes.
No full pytest.
