Phase 144-6-R5-30
upstream calculation attachment audit

Production changes: none.

Purpose:
Phase 29 showed that provider-anchored contribution chains are selective but
miss the two pi_6^3 Hopf calculation facts. Phase 30 tests the smallest
possible upstream extension.

Audited rule:
- start with the Phase-29 provider-anchored chain;
- remain inside the current NarrativeArgument local body;
- inspect only presentation edges whose parent is already in that chain;
- attach the premise only when its Narrative block role is CALCULATION;
- perform exactly one upstream hop; do not recurse.

Audit A:
Report whether H(nu')=eta_5 and H(nu' eta_6)=eta_5^2 are captured for each
pi_6^3 Argument.

Audit B:
Across the six representative groups, measure the number of added
CALCULATION occurrences relative to the Phase-29 base chain and all local
body occurrences.

Audit C:
Show the attachment distribution by Argument role.

Boundary:
- no production contribution-chain type;
- no ownership/renderer/frontier/dedup change;
- no ProofChain change;
- no expression-to-membership rule;
- no public route change;
- no dedicated pi_6^3 renderer removal.
