# Phase 178 R19 — Isolated finite cyclic suspension transport

## Scope

Reuse `finite_cyclic_suspension_transport_inference_rule()` without changing its implementation. The new provider constructs only backward proof obligations for a one-fold suspension from an eligible earlier cyclic presentation of the same order. It does not restrict the stem or require a composition generator. It is deliberately isolated from public search.

For $A=\mathbb{Z}/m\{a\}$, a proved suspension isomorphism $E:A\to B$, and a proved generator image $E(a)=b$, the existing rule derives $B=\mathbb{Z}/m\{b\}$. The actual n=6 target is $\pi_{12}^{6}=\mathbb{Z}/2\{\nu_6^2\}$; the earlier group is $\pi_{11}^{5}=\mathbb{Z}/2\{\nu_5^2\}$.

## Boundaries

- Source-first discovery: screened, positioned linked fixed statements precede the verified prior-database candidate.
- Only exact adjacent dimensions, matching cyclic orders, and typed generators are accepted.
- No new mathematical rule, source registration, GIVEN, saved proof, public wiring, or renderer change.
- Synthetic ProofSteps in tests are conditional matcher hypotheses only.
- Root-scoped discovery is intentional. The legacy 2-stem candidate generator is left untouched.
- The real n=6 test checks candidate availability and absence from public search; it does not claim that any of the three subgoals has been proved.

## Run

Extract the ZIP in the repository root. The reviewed develop HEAD is `4d982fcdb8f5d2e2e749c1bae8656a7bb2029c0c`. The preflight checks the tracked worktree, reviewed blobs, and local/remote HEAD equality.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r19_finite_cyclic_suspension_transport_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r19_finite_cyclic_suspension_transport_isolated\run.ps1
```

Expected gate: `PHASE178_R19_GATE=PASS_R19_ISOLATED_FINITE_CYCLIC_TRANSPORT`.

The runner executes only the new provider tests and five historical transport unit tests. The historical live-frontier assertion is not included: R19 is an isolated provider test and does not reassert a Phase 169 public search outcome. No full pytest run is performed.

## Next boundary

After R19 passes, connect the unchanged candidate provider to public search with regression checks and inspect the actual frontier. A generic Toda suspension-isomorphism bridge and a cited Delta-zero route are separate tasks, not implemented here.
