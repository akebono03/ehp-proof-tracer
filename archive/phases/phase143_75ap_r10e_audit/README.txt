Phase 143-75AP R10E read-only audit

Purpose:
Inspect the current-local generic narrative block renderer and the
existing provenance/semantic suppression vocabulary before the final
minimal implementation.

R10D established:
- local-body extraction does include dependency blocks;
- body rendering passes non-exact blocks to
  _render_generic_narrative_proof_block(...,
  suppress_provenance_only=True).

R10E determines the narrowest existing condition for preserving a
semantic aggregate derivation without globally re-enabling provenance
labels.

No production files are modified.
No tests are run.
