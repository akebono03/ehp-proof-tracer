Phase 159-R1-4 repair2

This is a two-literal escaping fix only.

Diagnosis showed every exactness line returned normalized=None because the
generated matcher searched for two backslashes instead of one.

Fix:
- r"\\xrightarrow{" -> r"\xrightarrow{"
- r"\\Delta" -> r"\Delta"

No logic changes.
No imports changed.
No tests changed.
No full pytest.
