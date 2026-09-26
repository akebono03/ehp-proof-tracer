Phase 143-75J
=============

Purpose
-------
Re-run the unchanged Phase 143-75A full-range
inference-rule-name fallback audit after Phase 143-75I.

Scope
-----
n=2..15
k=0..7
max_depth=7

This phase is audit-only.
No production code, tests, or documentation are changed.

The existing audit is reused:
phase143_75a/audit_phase143_75a_rule_name_fallback.py

Expected values
---------------
Phase 143-75G:
  fallback occurrences: 746
  statement types: 40

Phase 143-75I removed semantic fallback for:
  TodaPi32WhiteheadSquareUpToSignStatement: 60
  TodaProp27HopfInvariantUpToSignStatement: 53
  Toda58WhiteheadSquareUpToSignStatement: 33

Expected after Phase 143-75I:
  fallback occurrences: 600
  statement types: 37

The actual audit result is authoritative.
