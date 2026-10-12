Phase 164 R8-R1 UTF-8 test fixture correction.
Only test_audit.py read_text calls now explicitly use encoding="utf-8".
The read-only audit implementation is unchanged. Full pytest not run.
