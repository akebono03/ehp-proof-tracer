# EHP Proof Tracer

EHP Proof Tracer builds proof-backed narratives for homotopy groups using typed mathematical statements, a shared backward-search engine, and a common narrative renderer. The project distinguishes a mathematical proof from a displayed goal, an incomplete search, or an unverified assertion.

<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->

## Current status — Phase 169 closed (2026-10-28)

**Phase 169 is closed for its reviewed scope, not for all homotopy groups.** The completed work covers the 2-stem production path, theorem-based stable transport, direct-sum and composite-generator projection, shared generator-image Definition, root-reachable completed-proof references, and the relevant trust boundaries. The existing `HyoujiGen.csv` information continues to be used without adding generator-family-specific Definition implementations.

The independent R10ET R6D audit passed **19/19** scoped cases (16 required and 3 probes), with zero residual dependency on individual Definitions where the shared typed Definition was eligible. For $\pi_{10}^{8}$, the search retains nine `ProofStep` objects; the completed narrative and references include only the eight steps reachable from the selected root, citing the used `sphere.csv (n=4,k=2)` DB premise and Toda (4.5). Partial-proof visibility is unchanged.

The final end-of-phase test run on **2026-10-28** passed **67 focused Phase 169/168 regression tests** and **3,546 active `tests/` tests**, with zero failed tests, zero errors, exit code 0, and preserved Git index. The closeout helper itself passed eight tests. Full-suite command: `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`. The active suite retains the Phase 155 historical audit-only deselection boundary; archived tests are not silently counted as passes.

These results certify the stated implementation and test scope only. They do **not** establish complete proofs for arbitrary $\pi_{n+k}^{n}$, certify the mathematical truth of every registered Toda or database statement, remove legacy individual Definitions, or prove that every stem is supported. The next phase is to audit remaining mathematical proof gaps and data coverage before selecting any new implementation work.

## Current status — Phase 168 closed (2026-10-25)

Phase 168 has completed its agreed implementation and active-test closure. The final Windows PowerShell run reported:

- **3,546 passed**, zero failures and zero collection errors in the current `tests/` suite together with the Phase 168 regression modules.
- **86 passed** in the focused Phase 168 closure checks.
- Exact, unchanged proof text, references, and citation markers for $\pi_3^2$, $\pi_4^3$, and $\pi_5^4$ against the frozen Phase 168 baselines.
- All **14 GIVEN** steps across these three examples passed the publication-order audit.

This is an **active-suite** result, not a claim that every historical, archived, or superseded test passes. It is also not an independent mathematical formal verification of every assertion in Toda's source or a guarantee that all 112 registered homotopy groups have complete public proofs.

## Canonical proof narrative path

```text
Registered typed goal and eligible literature statements
    -> Backward Search
    -> Proof Tree (ProofStep / typed InferenceRule)
    -> Complete-proof trust boundary
    -> Proof Narrative Model (proof uses and citation links)
    -> Common Renderer (proof text and references)
    -> Web view
```

The canonical complete Web path is `web_group_proof.py::build_standard_web_group_proof_view`. It uses the searched and screened source context, resolves the citing assertion from the registered goal, and checks the complete proof tree before building the narrative model. `ProofSearchStatus.PARTIAL` and other incomplete states remain explicitly incomplete; they must not be promoted to complete proofs.

Reference citations are derived from used, fixed statements in the literature registry and their publication positions. They are not synthesized by looking up text labels in the renderer. Displaying a previously established group structure does not require expanding that group's entire proof tree into a later argument.

The `proof_origin_capture.py` and `phase168_r3_41p17_origin_handoff` facilities are **experimental observation tools**, not security or mathematical certificates. The R3-41P18 audit identified self-attestation and cross-context limitations. The standard Web path therefore retains the existing complete-tree checker, and the renderer retains compatibility guards for independently supplied models.

## Confirmed reference examples

- $\pi_3^2=\mathbb Z\{\eta_2\}$ — 18 proven steps (13 INFERENCE, 5 GIVEN).
- $\pi_4^3=\mathbb Z/2\{\eta_3\}$ — 25 proven steps (19 INFERENCE, 6 GIVEN).
- $\pi_5^4=\mathbb Z/2\{\eta_4\}$ — 10 proven steps (7 INFERENCE, 3 GIVEN); uses the registered $\pi_4^3$ group structure and Toda (4.5), not a replay of the completed $\pi_4^3$ proof.

These are representative regression fixtures, not an inventory of all certified groups. Work on the broader 2-stem and remaining incomplete targets should be tracked separately.

## Tests and documentation

Run the current active tests from the repository root:

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

Phase 168 closure additionally executed focused regression modules and frozen full-text/publication audits. The closure artifact is `phase168_r3_41p19_phase_closeout/output/review_bundle_20261025_092131_633.zip` in the local run that produced the reported results; its presence in another checkout is not assumed.

- [Design and trust boundaries](docs/design.md)
- [Development history](docs/development_log.md)
- [Roadmap](docs/roadmap.md)
- [Proof records](docs/proof_records.md)

Previous Phase 165–167 documentation remains historical. In particular, a Phase 166 partial result must not be mistaken for the status verified by later Phase 168 tests.
