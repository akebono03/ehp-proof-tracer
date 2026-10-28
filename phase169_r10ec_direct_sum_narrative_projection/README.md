# Phase 169 R10EC — Verified Direct-Sum Narrative Projection

## Purpose

Compress excessively long, duplicated one-step generator-image prose in **completed, replay-verified direct-sum group proofs**. Preserve every `ProofStep`, premise, citation, group conclusion, and the existing proof search and Trust Boundary behavior.

A typical nineteenfold transport renders the three actually proved generator correspondences:

- `E^{19}(nu_11^3)=nu_30^3`
- `E^{19}(mu_11)=mu_30`
- `E^{19}(eta_11 epsilon_12)=eta_30 epsilon_31`

These are projections of an existing complete chain of independently verified `GeneratorImage` inference steps, **not new mathematical assertions or source axioms**.

## Scope of changes

- **Existing file:** `phase168_r3_5_model_renderer.py`, function `render_model_backed_narrative_markdown()` only. No module-level import changes. The full updated function and full file are written to `output/` by `patch.py`.
- **New file:** `phase169_r10ec_direct_sum_narrative_projection/projection.py`, containing `VerifiedDirectSumTransportDisplay` and `project_verified_direct_sum_transport()`.
- **New files:** `patch.py`, `audit.py`, `tests/test_r10ec_projection.py`, `tests/test_r10ec_patch.py`, and `run.ps1`.
- **Unmodified:** proof search, verified inference rules, typed expressions, underlying sources, data tables, registry, Trust Boundary, partial-proof rendering, and earlier cyclic-chain projections.

## Fail-closed display conditions

The projection requires an exact completed direct-sum transport root whose first premise is the original typed group structure, second premise a proved Toda (4.5) iterated isomorphism, and remaining premises the exhaustive, correctly ordered typed image obligations produced by the existing transport rule. Every image must have a citation-backed GIVEN ancestor. It hides only otherwise uncited image/suspension inference steps whose consumers belong exclusively to the compressed group-proof chain. Any ambiguity returns `None` and keeps the existing full prose.

The source and target generator LaTeX is read from the *existing typed generator printer*. It does not provide evidence for the generator image or substitute a candidate identity for a proof.

## Windows execution

From the `ehp_proof` repository root, after extracting the ZIP into the root:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10ec_direct_sum_narrative_projection\run.ps1"
```

The runner checks `develop`, the reviewed ancestor commit and unchanged Git blobs; rejects local or staged renderer changes; verifies the previously applied R10EB display prerequisite; preserves LF/CRLF; and restores the exact original renderer and known output files if any test or audit fails. It executes focused pytest only, then compares complete Proof Trees, citations, exact output equations, and Trust Boundary replay for four groups, including `pi_39^30`.

The **full pytest suite is deferred until the end of Phase 169**.
