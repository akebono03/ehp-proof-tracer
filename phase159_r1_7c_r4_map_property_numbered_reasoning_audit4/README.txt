Phase 159 R1-7c R4 map-property numbered-reasoning audit4

Purpose
-------
Audit3 established:

- pi_9^3 Delta pair:
  injective + surjective visible;
  no semantic isomorphism step.
- pi_10^3 Delta pair:
  injective + surjective visible;
  no semantic isomorphism step.
- pi_11^6 H pair:
  injective + surjective + public isomorphism prose visible;
  no matching raw or semantic-closure step.

Therefore the pi_11^6 isomorphism prose is generated later in the narrative
pipeline.

Current GitHub inspection found no literal "は同型写像である." in the
contribution renderer, so audit4 traces calls to its imported generic step
renderer during pi_11^6 public rendering.

The trace records:
- conclusion type;
- inference rule name;
- rendered sentence;
- caller function chain.

Goal
----
Identify the exact runtime source route for:

  $H: \pi_7^3 \to \pi_7^5$ は同型写像である.

This determines where numbered injective/surjective reasoning should be
connected without inventing any new semantic conclusion.

Production code changes: none.
Test code changes: none.
No full pytest.
