Phase 143-75AF implementation R2

Purpose:
Correct the new Phase 143-75AF test expectation only.

Observed actual renderer output:
\left.\left(Eβ + δ\right)\right|_{\pi_{11}^{5}} = E: \pi_{11}^{5} \to \pi_{12}^{6}

The failed test incorrectly expected:
\beta and \delta

R2 changes:
- phase143_75af_impl/test_phase143_75af_first_summand_rendering.py
  - expected Unicode β and δ, matching the existing expression renderer

R2 does NOT change:
- toda_proof_narrative_renderer.py
- toda_rules.py
- inference
- API
- docs

Focused tests only.
No full pytest.
