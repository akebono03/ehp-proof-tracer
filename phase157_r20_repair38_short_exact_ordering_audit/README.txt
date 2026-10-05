Phase157-R20 repair38 runtime audit

Purpose
-------
Determine why repair37's generic short-exact ordering function does not move
the short-exact reason and sequence.

The audit prints:
- every visible injective/surjective map-property candidate;
- statement type and `.map` availability;
- map source/target/name;
- every exactness step that generates a short exact sequence;
- exactness window terms and map names;
- visible reason/sequence paragraph indices;
- current visible support order;
- whether directly re-running
  `order_toda_group_proof_narrative_short_exact_support()` changes the body.

Production code changes: none.
pytest: not run.
