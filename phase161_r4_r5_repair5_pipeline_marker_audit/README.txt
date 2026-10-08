Phase 161-R4-R5 repair5 pipeline marker audit

Purpose
=======
Repair4 showed that the final public body still contains:

  [R2]より, pi_{n+1}^n = Z/2{eta_n}.

instead of:

  [R2]より, pi_4^3 = Z/2{eta_3}.

Earlier audit also showed that, before public filtering, Proposition 5.1 can
exist under different reference-entry numbers.

This audit traces the exact runtime order of:

- suppress_toda_group_proof_narrative_reference_body_duplicates
- link_toda_group_proof_narrative_reference_body_consumers
- link_toda_group_proof_narrative_unmarked_reference_consumers

in both the contribution renderer and the outer narrative renderer.

For every call it prints:
- reference-entry number and locator pairs
- marker lines
- the general Proposition 5.1 line
- the concrete pi_4^3 line
- before/after text

No production or test files are modified.

Goal
====
Determine exactly:
1. where the Proposition 5.1 marker is first attached,
2. what reference number it has at that stage,
3. where the general statement is suppressed,
4. where the marker is lost or reattached,
5. where final renumbering to R2 occurs.

Do not implement another repair until this trace is known.
