# GitHub baseline — Phase 155 Closure-R4-R2

Repository: `akebono03/ehp-proof-tracer`

Inspected before implementation:
- Phase144 final completion audit and its audit helper
- Phase153 R3-10 public Reference audit
- Phase153 R3-11 Reference body ownership audit
- Phase97 representative top-level API audit
- current contribution/narrative renderers
- current calculation candidate/report provenance types
- Phase96 source-presentation contracts
- Phase98 facade provenance contracts

Key findings:
- current renderer intentionally reads structured `inference_rule` metadata;
- Phase144 fixed completion assumptions are historical;
- `TodaCalculationCandidate.goal_source` is explicitly optional;
- the 117 Reference/body duplicates belong to Phase156 relevance/minimal-display
  work, not Phase155 test consolidation.
