# Phase 169 R10A2 — Unified one-stem narrative projection

This package extends the successful R10A verified-suspension display contract to the previously separate one-stem eta-notation proof path. It does not change search, proof inference, typed statements, citations, or the generator database.

## Files and boundaries

- Existing production file: `phase168_r3_5_model_renderer.py` (complete function `render_model_backed_narrative_markdown` is exported after patching).
- New helper: `phase169_r10a2_unified_one_stem/one_stem_projection.py`, containing `project_verified_one_stem_notation_chain`.
- New patch, tests, and audit are contained in this package.

The existing R10A proof-image projection remains unchanged. R10A2 recognizes a complete one-stem proof whose root is an actual typed eta-notation inference and whose direct premises contain the proved iterated Toda transport and cited family definition. It reuses R10A's `VerifiedStableImageChainDisplay` and renders one aggregated equation, not a prose line per intermediate suspension.

The original ProofSteps and all citations remain in the Narrative Model. Partial proofs are excluded. The renderer is restored to the successful R10A1 version on any failed focused test or audit.

## Windows PowerShell

Extract `phase169_r10a2_unified_one_stem.zip` into the repository root and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10a2_unified_one_stem\run.ps1"
```

Full pytest is intentionally deferred until the end of Phase 169.
