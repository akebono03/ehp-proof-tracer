# Phase 160-R9

Connect the two-stem public Narrative to the Phase 160-R7 generic stable Narrative.

Scope:

- Extend the existing R7 finite-cyclic stable public renderer from stems 1 and 7 to stem 2.
- Keep the internal semantic generator as `Composition(eta_n, eta_(n+1))`.
- Render the public generator canonically as `eta_n^2`, matching the existing unstable Narrative convention.
- Use `pi_6^4 = Z/2{eta_4^2}` as the canonical two-stem base.
- Use Toda (4.5) as the stable transport reference.
- Render concrete target-local specializations only.
- Preserve the existing stem-1 and stem-7 public contracts.
- Delegate the canonical base `pi_6^4` itself to the existing renderer.
- Do not change production semantics.
- Do not add free-cyclic, zero-group, or direct-sum stable Narrative support.
- Do not run the full test suite.
