Phase 144-6-R5-13
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
Refine the R5-12 typed-provider prototype into three semantic layers:

1. ATOMIC
   Existing Narrative Definition/Order Arguments that directly establish a
   final generator or order component.

2. TRANSPORT
   Typed structural statements that transfer group/order/decomposition
   information to the final target.

3. INTEGRATION
   The root inference that assembles final group structure from its direct
   premises.

Why
---
R5-12 matched 8 of 24 final components. It successfully recognized:

- pi_12^5 through a typed Hopf isomorphism,
- pi_15^8 through transported_group,
- pi_16^9 order 16 through target_group + target_order.

It failed to recognize pi_6^3 and pi_8^5 because their final claims are
assembled from Definition/Order Arguments rather than a duplicate non-root
group statement.

It also failed to synthesize pi_10^4 through decomposition transport. R5-13
does not manufacture the composite generator by hand. Instead it audits
whether Toda56Nu4DecompositionStatement is a direct premise of the root
integration and separates that integration role from atomic/transport roles.

Targets
-------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

No rule-name parsing and no target-specific n/k matching are used in provider
classification.
