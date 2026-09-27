Phase 144-6-R5-12
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
Prototype a typed provider-semantic model for Narrative-required final claims.

The prototype does not parse inference-rule names.

Final claim kinds
-----------------
GROUP_GENERATOR
ELEMENT_ORDER
FREE_SUMMAND
FINITE_SUMMAND
GROUP_DECOMPOSITION

Provider kinds
--------------
GROUP_RELATION
HOPF_ISOMORPHISM
TRANSPORTED_DECOMPOSITION
TARGET_ORDER
DECOMPOSITION_TRANSPORT

Targets
-------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

R5-11 findings used
--------------------
- pi_12^5: TodaProp515Pi12_5HopfIsomorphismStatement carries image-group
  order and source_generator.
- pi_15^8: Toda515Sigma8TransportedDecompositionStatement carries a typed
  transported_group.
- pi_16^9: Toda48Pi16_9OrderAndE4InjectiveStatement carries target_group
  and target_order.
- pi_10^4: the final composite generator is distributed across a typed
  source-group relation and Toda56Nu4DecompositionStatement.

Questions
---------
1. Can final claim components be matched by typed non-root providers?
2. Can pi_10^4 be handled by a generic decomposition-transport provider?
3. Which expected components remain root-only integration claims?
4. Are remaining problems provider selection rather than provider discovery?
