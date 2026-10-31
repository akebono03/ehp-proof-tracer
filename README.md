# EHP Proof Tracer

EHP Proof Tracer builds proof-backed narratives for homotopy groups using typed mathematical statements, a shared backward-search engine, and a common narrative renderer. The project distinguishes a mathematical proof from a displayed goal, an incomplete search, or an unverified assertion.

<!-- PHASE171_FINAL_CLOSEOUT_20261031 -->

## Current status — Phase 171 closed (2026-10-31)

Phase 171 is complete for the reviewed public proof of $\pi_6^3=\mathbb Z/4\{\nu'\}$. The verified search has `complete`, `open_goals=0`, eight source-linked references, and a `generic-complete-proof` Web narrative. The mathematical basis is the EHP short exact sequence and the independently certified relation $2\nu'=E(\eta_2^3)\ne0$, establishing that $\nu'$ has order four.

The single phase-end active `tests/` suite reported **3,546 passed** (pytest summary: `3546 passed in 125.50s (0:02:05)`, exit code 0). Phase 171 R1R1 and R2R4 focused gates had already passed, and this closeout kept production code and historical proof sources unchanged. The archived full five-document outputs and gate JSON preserve the reviewed result. Previous R2 text stating that the phase-end test was pending is a historical pre-closure record.

Phase 172 may separately review display duplication and `DB prior` wording; these are not mathematical proof prerequisites. The result does not certify arbitrary $n\ge3$ groups or unchecked literature.

<!-- PHASE171_CLOSEOUT_R2_REVIEWED_20261031 -->

## Current status — Phase 171 proof complete; phase-end gate pending (2026-10-31)

The public, trust-gated proof search for $\pi_6^3=\mathbb Z/4\{\nu'\}$ reached `complete` with `open_goals=0` and `generic-complete-proof`. Its EHP exactness argument proves injectivity of $E:\pi_5^2\to\pi_6^3$ and surjectivity of $H:\pi_6^3\to\pi_6^5$. Using $\pi_5^2\cong\mathbb Z/2$ and $\pi_6^5\cong\mathbb Z/2$, it derives the short exact sequence $0\to\pi_5^2\xrightarrow{E}\pi_6^3\xrightarrow{H}\pi_6^5\to0$ and therefore $|\pi_6^3|=4$. The verified double relation $2\nu'=E(\eta_2^3)\ne0$ proves that $\nu'$ has order four. The public narrative has eight source-linked Reference entries.

The Phase 171 R20R12/R20R13 presentation work exposes proof-backed order reasoning, groups three independently certified $\eta$ suspension identities under one citation, and splits sentences in the completed proof body without changing the mathematical Proof Tree. R20R13R4 repaired a test-only `list.count()` assertion. At Phase 171 closeout preflight, the R1R1 review replaced a brittle fixed 28-step test with proof-state and root-preservation checks. The Windows focused verification reported **88 passed** plus **5 installer tests passed** on 2026-10-31, without production-code changes.

**Closure status:** The Phase 171 active-suite full `pytest` has **not** yet been run. The proof and focused regression checks are confirmed; formal Phase 171 closure remains pending the single phase-end full-suite gate, final Git review, and recorded outcome. Historical Phase 170 results below remain unchanged. This evidence does not certify all $n\ge3$ or all homotopy groups. Presentation-only duplication of equivalent $E$ equations, some long $H$ derivations, repeated surjectivity explanations, and `DB prior` labeling remain deferred to Phase 172 unless a verified correctness defect is discovered.

<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## Current status — Phase 170 closed (2026-10-29)

Phase 170 completed its reviewed **explicit $n=2$ database domain**, covering all 33 stems $1\le k\le 33$ (groups $\pi_{k+2}^{2}$). A fresh, independent R3-R10R1 audit ran ordinary typed proof search and the public, trust-gated narrative Web route for each stem. The results were **33/33 `COMPLETE_AND_WEB_VERIFIED`**, with no unresolved goals in the audited outcomes and no domain gaps. The audit left tracked files unchanged.

The proof search uses the separately screened earlier group structure for $\pi_{k+2}^{3}$ and the typed Toda (5.2) composition isomorphism $\eta_2\circ -:\pi_m^3\cong\pi_m^2$ in its applicable domain. For $\pi_{14}^{2}$, the previously unfinished generator correspondence additionally uses the cited equation $\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6$ from the checked adopted Chapter VII transcription of Toda (7.12). It is a separate, replayable proof premise, not an equality inferred from generator names or database display text. Its source position is defined relative to the adopted transcription, **not independently certified against the original printed edition**.

Phase-end verification on Windows on 2026-10-29 reported **3,546 passed in 34.94s**, exit code 0, for `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`. The Phase 170 R3-R11 final report was `FULL_SUITE_PASS`, with the previously verified 33/33 domain report accepted and `tracked_unchanged=True`. The active `tests/` suite is not the full collection of archived or retired historical tests.

These results do **not** certify every homotopy group, every $n\ge3$ target, every original Toda statement, or arbitrary user-defined inference rules. The existing Proof Tree, citation-screening, Narrative Model, and Web trust boundaries remain in effect. Further work should select remaining registered goals based on actual incomplete searches and independently checkable sources.

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
