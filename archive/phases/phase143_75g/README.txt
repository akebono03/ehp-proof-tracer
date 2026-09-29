Phase 143-75G

Audit only. No production/test/document changes.

Purpose:
Re-run the unchanged Phase 143-75A whole-range inference-rule-name fallback audit after Phase 143-75F.

Range:
- n=2..15
- k=0..7
- max_depth=7

Baseline:
- Phase 143-75A: 1262 fallback occurrences, 47 statement types, 57 rule names
- Phase 143-75C removed: 354 occurrences, 3 statement types
- Phase 143-75F removed: 162 occurrences, 4 statement types

Expected remaining fallback occurrences: 746
Expected remaining statement types: 40
Expected remaining distinct rule names: determine from actual audit output.

The actual audit output is authoritative.
