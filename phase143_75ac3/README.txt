Phase 143-75AC-3 dedup audit

Audit only. No implementation changes.

Purpose:
Separate repeated renderer calls for
TodaLemma54HopfOddMultipleStatement into:

1. raw renderer calls
2. unique Python object identities
3. unique statement equality classes
4. unique first-class field-value signatures

The established Phase 143-75U inventory remains the authoritative count
for fallback occurrences and groups.

Expected inventory target:
20 occurrences / 18 groups.

No source files are changed.
No pytest is run.
