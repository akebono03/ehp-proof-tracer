Phase 148 RC2-4 — Cross-group Audit

Purpose
-------
Audit the RC2 exposure rule across:

- pi_6^3
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

Production changes
------------------
None.

Existing repository test changes
--------------------------------
None.

Audit-only test added
---------------------
tests/test_phase148_rc2_4_cross_group_audit.py

Checks
------
1. Exactness component evidence remains retrievable from method-evidence
   traversal after Narrative suppression.
2. UNOWNED_RECURSIVE contributions are absent from the final Narrative.
3. pi_6^3 keeps its owned derived short exact sequence.
4. pi_12^5 still has an OWNED_PRIMARY exactness component.
5. pi_15^8 remains a no-exactness case.
6. No sampled group unexpectedly enters AMBIGUOUS_RELEVANT.

The diagnostic audit prints, for every Argument:
- role
- relevant-group count
- evidence-block count
- component count
- exposure class
- contribution count
- whether each contribution is visible in the final Narrative

It also prints the final Narrative for each of the six groups.

Important boundary
------------------
This audit does not judge or repair Narrative ordering. The known ordering
issue remains Phase 149 / RC3.

No repository-wide pytest is run in RC2-4.
