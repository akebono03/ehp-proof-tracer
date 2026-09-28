Phase 144-6-R5-29
Narrative contribution-chain ownership audit

Production changes: none.

Purpose:
Phase 27 showed that raw derivation-path membership is too broad.
Phase 28 showed that assigning isolated ProofSteps to an owner Argument is
also ambiguous. Phase 29 audits a larger unit: a provider-anchored Narrative
contribution chain.

Diagnostic chain:
1. Start from ProofSteps inside direct SUPPORTING_BLOCK ProofChain providers.
2. Stay inside the current NarrativeArgument local body.
3. Follow existing presentation parent edges toward the Argument conclusion.
4. Include only steps whose graph distance decreases toward that conclusion.

Audit A:
For the pi_6^3 Phase-20 missing six facts (membership excluded), report whether
each fact is inside the provider-anchored chain for each Argument, whether it
is itself a provider anchor, and its distance to the Argument conclusion.

Audit B:
Across all six representative groups, compare provider-anchored chain step
occurrences with all local-body step occurrences.

Audit C:
Summarize how many missing-six facts each pi_6^3 Argument's chain owns.

Boundary:
- no production contribution-chain type;
- no ownership/renderer/frontier/dedup change;
- no ProofChain change;
- no expression-to-membership rule;
- no public route change;
- no dedicated pi_6^3 renderer removal.
