Phase157 R11-R17 repair2 — Reference attribution fix

repair1 result:
- 71 passed
- 4 failed
- remaining failures all belong to Reference attribution/pruning

repair2 pre-audit established the generic rule:

1. If a direct consumer is owned by another literature Reference,
   that consumer is ancestry and must not receive the source Reference marker.

2. Prefer a unique visible non-root consumer with no literature ownership.

3. If no such consumer exists, use a unique visible root consumer.

4. After fixed Reference restoration, run the existing body-usage filter once
   more so markerless ancestry-only References disappear.

Expected target effects:
- pi_6^3: Proposition 5.3 removed.
- pi_10^4: Proposition 5.11 root attribution; Lemma 5.4 non-root attribution.
- pi_12^5: Lemma 5.13 root attribution; (5.5) removed.
- pi_16^9: Proposition 5.15 / Lemma 5.14 attributed; Lemma 5.13 removed.

Production:
- toda_group_proof_narrative_contribution_renderer.py

Tests:
- existing R11-R17 focused tests only.

No imports changed.
No docs changed.
No full pytest.
