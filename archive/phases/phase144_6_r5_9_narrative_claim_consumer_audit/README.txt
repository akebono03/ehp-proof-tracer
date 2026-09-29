Phase 144-6-R5-9
==================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-8 showed that "the child purpose subject occurs somewhere in the parent's
visible statements" is far too broad: almost every root-reachable Argument
passed that test.

R5-9 starts from the final mathematical claim instead.

For a root group-structure conclusion such as

  pi = Z/m{alpha}

the audit derives these claim components:

  generator = alpha
  order(alpha) = m

For a direct sum, the same components are derived per supported cyclic summand.

The audit then compares those claim components with existing Argument
conclusions:

- Definition Argument: its purpose subject must equal a final generator.
- Order Argument: its ORDER conclusion must have the same generator and order
  as a finite cyclic summand of the final group.

This is deliberately stricter than subject occurrence in calculations.

Representative groups
---------------------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

Important limitation
--------------------
This audit identifies semantic claim providers. If several Arguments prove the
same final generator/order claim, R5-9 reports all of them. It does not yet
choose the correct proof occurrence.

No production selection rule is implemented.
