# Phase 159 pi3_2 Semantic Numbered Map-Property Reasoning Repair 24

This package removes prose-based semantic inference from the final numbered
map-property normalization step.

## Scope

The repair changes only the Phase 159 final public numbered map-property
reasoning path.

The semantic source of truth is now:

1. typed injective / surjective / isomorphism statements;
2. equality of the underlying `group_map` objects;
3. `EXACTNESS_TO_MAP_PROPERTY` typed reasons for exactness provenance.

Rendered strings are still used as output-location anchors, but they are no
longer used to decide whether two map-property statements have the same
mathematical meaning.

## Production change

`toda_group_proof_narrative_renderer.py`

- imports the existing typed reason sidecar builder and reason kind;
- changes
  `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()`;
- changes `render_toda_group_proof_narrative_markdown()` so the normalizer
  receives the `TodaGroupProofPresentation`.

When an injective or surjective step is backed by
`EXACTNESS_TO_MAP_PROPERTY`, the public numbered display is preceded by:

`完全性より,`

The connector is generated from typed provenance rather than preserved or
recovered from prose.

## Tests

A focused test file is added:

`tests/test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py`

It verifies:

- pi_3^2 injectivity and surjectivity retain exactness provenance;
- the numbered isomorphism conclusion still follows `(1), (2)`;
- the exactness provenance exists as typed reasons;
- calling the helper without semantic presentation does not infer meaning
  from arbitrary prose;
- the existing pi_11^6 semantic pairing remains available.

Repository-wide pytest is intentionally not run in this Phase step.
