## Phase 161 — Concrete Backward-Driven Proof Reconstruction

Phase 161 adds a focused backward-goal path for the unstable EHP suspension isomorphism

$$
E:\pi_4^2\xrightarrow{\cong}\pi_5^3.
$$

The implemented path starts from this concrete goal, decomposes it into injectivity and surjectivity, propagates four separate EHP exactness obligations, and identifies the independently supplied literature-derived premises. The seven existing Toda production rules are then applied **forward** to construct a new inference-backed proof step. The completed Phase 59 isomorphism step is not an input to this reconstruction.

The new modules are:

- `phase161_backward_goal_schema.py` (R2: suspension isomorphism goal decomposition).
- `phase161_r3_backward_goal_schema.py` (R3: four exactness-based backward expansions).
- `phase161_r4_literature_premise_matching.py` (R4: structural matching of the two terminal goals to existing inferred evidence).
- `phase161_r5_backward_proof_reconstruction.py` (R5: backward-directed construction using existing production-rule application).
- `phase161_r7_premise_provenance_validation.py` (R7: opt-in validated reconstruction and recursive inference ancestry checks).

R1 audited the seven production-rule instances. R6 audited the reconstructed proof and recorded a limitation in the legacy R5 entry point: structurally matching inferred premises alone do not validate the entire ancestry. R7 supplies a separate validated entry point. It recalculates inferred conclusions, rejects unsupported inference steps, unapproved given leaves, altered conclusions, and ancestry cycles. Approval of a given leaf is an explicit trust boundary, **not** an automatic mathematical proof of the underlying literature fact.

The R2–R7 implementation remains specific to the named isomorphism; it is not an arbitrary-group backward proof search. It does not automatically discover literature statements, does not replace established narrative renderers, and is not yet connected to the public proof display. Phase 162 is the proposed point to audit connection of validated reconstructed steps to the existing shared proof renderer before broader unstable generalization.

Focused local verification reported by the user:

```text
R2:  3 passed
R2–R3:  7 passed
R2–R4: 11 passed
R2–R5: 17 passed
R6 audit: 4 passed
R7 + R6 regression: 10 passed
```

**At the user's explicit request, no repository-wide pytest is run for Phase 161 closure.** The focused results are not a claim of repository-wide all-pass.

