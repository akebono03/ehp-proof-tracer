# GitHub baseline — Phase 155-R3-3A

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Current GitHub tests were inspected before R3-3A, including representative
Phase 143, Phase 150, Phase 153, and Phase 154 test files.

The repository shows that later tests often share production surfaces with
older tests but differ in:
- helper functions,
- imports,
- exact assertions,
- punctuation contracts,
- reference-selection contracts.

Therefore R3-3A does not infer deletability from file chronology alone.
It consumes only R3-2F-r1 `deletion_authorized=true` pair evidence.

The user's local R3-2F-r1 result is the authoritative current test-state input:
- 440 unique candidate base tests passed,
- 332 candidate pairs,
- 164 removable duplicate pairs,
- 125 retain-independent pairs,
- 43 historical-keep pairs,
- 0 needs-review pairs.

R3-3A converts those pair decisions into graph-level survivor/deletion
candidates without modifying repository tests.
