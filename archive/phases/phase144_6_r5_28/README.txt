Phase 144-6-R5-28
Narrative contribution ownership audit

Production changes: none.

Purpose:
Phase 27 showed that raw derivation-path membership is almost universal inside
Argument local bodies and therefore cannot serve as Narrative visibility.
Phase 28 changes the question from dependency relevance to ownership:
which NarrativeArgument should be responsible for explaining a shared fact?

Audit A:
For the six Phase-20 missing facts other than embedded membership, list every
pi_6^3 Argument whose local body contains the fact and classify whether it is:
- the Argument conclusion;
- a direct conclusion premise;
- a child-Argument conclusion;
- inside a direct SUPPORTING_BLOCK ProofChain provider;
- merely present in the local body.

Audit B:
Across all six representative groups, measure how often ProofSteps belong to
multiple Argument local bodies and how often direct supporting-provider steps
are shared by multiple ProofChains.

Audit C:
Apply a deliberately hypothetical structural ownership priority only for
diagnostic purposes:
argument conclusion > direct premise > child conclusion >
direct supporting provider > local body, then discourse order.

Boundary:
- no production ownership model;
- no renderer/frontier/dedup change;
- no expression-to-membership rule;
- no public route change;
- no dedicated pi_6^3 renderer removal.
