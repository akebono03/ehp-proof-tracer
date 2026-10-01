Phase 153-R10 Route Boundary Repair R1
====================================

Confirmed causes
----------------
1. R9 integration test still expected pre-R10 Reference numbers.
2. R10 legacy wrapper rebuilt '## 証明' with only one newline before the body.
3. Generic narrative routes do not necessarily use [Rk] markers in the body.
   Filtering those routes by marker presence removed their entire Reference
   section.

Repair rule
-----------
Used Reference filtering applies only to narrative bodies that actually use
[Rk] markers.

If a body contains no [Rk] markers, preserve its existing structured
Reference section unchanged.

Production changes
------------------
toda_group_proof_narrative_references.py
- filtering helper returns unchanged entries/statement-lines/body when the
  body has no Reference markers.

toda_group_proof_narrative_renderer.py
- restore canonical '## 証明\n\n' spacing.

Test change
-----------
tests/test_phase153_r9_reference_reuse_derivation_suppression.py
- rendered pi6_2 expectations now use the R10-renumbered [R1] and [R2].
- the internal R9 reuse-boundary test remains unchanged.

Full pytest remains deferred until the end of Phase 153.
