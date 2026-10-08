Phase 161-R4-R5 repair2 body-linkage audit

Purpose
=======
The R4-R5 repair1 now correctly renders Proposition 5.1 in general form in the
Reference section, while keeping the concrete pi_4^3 relation in the proof body.

The only remaining failure is that the concrete pi_4^3 paragraph does not carry
the Proposition 5.1 marker.

Before modifying generic consumer-linking behavior, this audit determines:

- every [Rk] marker currently present in the body
- whether [R2] is already attached somewhere else
- the Proposition 5.1 reference-entry proof steps
- their rendered statements
- consumer chains up to depth 3

No production or test files are modified.
