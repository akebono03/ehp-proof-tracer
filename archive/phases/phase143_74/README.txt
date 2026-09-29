Phase 143-74

Purpose:
Audit actual group-proof Narrative output through the implemented 0-7 stems
for raw internal statement-class-name fallback exposure.

This package changes no implementation, tests, or documentation.

Audit range:
- n = 2..15
- k = 0..7
- proof replay max_depth = 7

A statement is counted only when:
1. its per-fact rendering is exactly `ClassName`;
2. that exact raw fallback is present in the final Narrative.

This avoids treating a statement type as exposed merely because it exists
in the proof presentation.

Run from repository root with PYTHONPATH set to the repository root.
