Phase 143-75D

Purpose:
Re-run the unchanged Phase 143-75A whole-range inference-rule-name fallback audit
after Phase 143-75C.

Scope:
- n=2..15
- k=0..7
- max_depth=7
- production Narrative path
- no production changes
- no test changes
- no documentation changes
- no full pytest

Expected comparison:
- Phase 143-75A baseline: 1262 fallback occurrences, 47 statement types
- Phase 143-75C converted: 354 occurrences across 3 statement types
- Expected remaining fallback occurrences: 908
- Expected remaining statement types: 44

The actual audit output is authoritative.
