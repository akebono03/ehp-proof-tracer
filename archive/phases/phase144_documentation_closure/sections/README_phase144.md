## Phase 144 closure

Phase 144 audited how semantic Narrative presentation scales from the representative
$\pi_6^3$ proof to other group-result proofs. It did not add new Toda theorem facts
or a second proof engine.

The phase established a generic contribution-aware Narrative route over the existing
`ProofStep` graph, semantic sidecar, Narrative blocks, arguments, and proof chains.
The audit also established a complete replay API for Narrative use when an explicit
positive depth requires the semantic dependency closure. Explicit depth 0 remains a
bounded replay and is not silently expanded to the complete replay.

The Phase 144-6 R25-30-R3 boundary audit is the technical investigation endpoint
for the phase. Across the six representative groups, the current ownership /
argument-boundary classification was consistent with the existing child-argument
model. The audit identified a separate remaining pressure: some owned group-structure
or definition entries can recursively re-expand a large proof subtree. This is a
result-reuse problem, not an ownership-boundary leak, and it is deliberately deferred
until a concrete proof requires a general repair.

Representative current boundary inventory:

```text
pi_6^3:  selected=6   participating=6/6   detached=0/0    transport=1
pi_8^5:  selected=10  participating=7/7   detached=3/3    transport=1
pi_10^4: selected=22  participating=0/0   detached=22/0   transport=2
pi_12^5: selected=46  participating=2/2   detached=44/0   transport=4
pi_15^8: selected=54  participating=10/10 detached=44/0   transport=4
pi_16^9: selected=54  participating=10/10 detached=44/0   transport=4

TOTAL selected=192
TOTAL participating=35
TOTAL detached=157
TOTAL detached_insertable=3
TOTAL missing=0
```

The final canonical repository-wide run after the Phase 144 regression repairs
collected 10,298 tests:

```text
10273 passed, 25 failed in 2321.20s (0:38:41)
```

All 25 failures were confined to historical R5-39 through R5-43 completion /
fixed-count snapshot assertions whose pre-R25 assumptions no longer represented
the current ownership/boundary semantics. They were maintained without changing
the production renderer and without replacing the old fixed totals with new fixed
totals. The affected focused regression then passed:

```text
66 passed in 1308.82s (0:21:48)
```

The whole repository suite was intentionally not rerun after that historical-test
maintenance. Therefore the closure record preserves both pieces of evidence rather
than reporting an unobserved all-green repository-wide run.

Phase 145 is intentionally narrow: change the default group-proof presentation to
Narrative with depth 2. It must not implement result reuse or other new
generalization machinery.

From Phase 146 onward, development follows one concrete proof pressure at a time:

```text
one Phase
→ one concrete issue
→ the minimum general rule needed for that issue
→ focused regression
→ preserve existing proofs
```

A future phase is complete when its one target issue is solved by a general rule
rather than target-specific special handling, without breaking existing proofs.
