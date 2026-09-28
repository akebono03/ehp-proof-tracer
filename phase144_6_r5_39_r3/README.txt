Phase 144-6-R5-39 R3

Audit-only repair. Production changes: none.

Root cause of R1/R2:
Phase 38 provider_keys intentionally contain Python object identity values.
Phase 39 called build_visibility_occurrences() once and then called
build_explanatory_contribution_groups(), which internally rebuilt the
occurrences a second time. The second build created a different object identity
space, so contribution-group provider_keys could not be used to look up rows
from the first occurrence build. This produced empty row lists.

R3:
Build visibility occurrences exactly once inside Phase 39, then build the
194 contribution groups from that same occurrence tuple using the same Phase-38
grouping and ownership rules. Therefore provider identity is compared only
within one construction identity space.

No production semantic key is introduced in this repair. Replacing object-id
provider keys with stable production identities would be a separate design
decision and is outside this audit repair.

Boundary:
- no production visibility rule;
- no production ownership rule;
- no renderer change;
- no ProofChain change;
- no production deduplication change;
- no expression-to-membership rule;
- no parity matcher change;
- no public route change;
- no dedicated pi_6^3 renderer removal.
