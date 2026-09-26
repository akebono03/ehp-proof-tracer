Phase 143-75AO bulk read-only semantic audit

Purpose:
Inspect all 15 remaining fallback statement types in one run.

Current baseline:
- fallback occurrences: 53
- statement types: 15
- fallback rule names: 15
- render errors: 0

The audit records:
- runtime dataclass field names
- field runtime types
- unique semantic values
- current semantic rendering

This is intentionally read-only.
No production changes.
No tests.
No docs.
No full pytest.

The next implementation step can then batch all statement renderers
whose stored semantic fields are sufficient and unambiguous.
