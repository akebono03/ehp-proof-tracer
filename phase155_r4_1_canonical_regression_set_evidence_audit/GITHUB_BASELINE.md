# GitHub baseline — Phase 155-R4-1

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R4-1:
- `docs/roadmap.md`,
- `phase153_closure_audit/run_phase153_closure_audit.ps1`,
- `phase154_closure_audit/run_phase154_closure_audit.ps1`,
- `phase150_finalization/run_phase150_finalization.ps1`,
- current test collection guidance.

The public roadmap explicitly lists the following deferred test-suite
maintenance items:
- stale expectation inventory,
- duplicate coverage audit,
- historical snapshot classification,
- canonical regression set,
- pytest collection boundary,
- performance baseline.

R3 has addressed the duplicate/superseded and historical-precedence part.
R4-1 therefore starts the canonical-regression boundary as an evidence audit,
not as a bulk marker or file-layout change.

The Phase 153 and Phase 154 closure scripts provide direct evidence of tests
already used as focused current-contract regression boundaries.

Repository-wide pytest remains deferred to the end of Phase 155.
