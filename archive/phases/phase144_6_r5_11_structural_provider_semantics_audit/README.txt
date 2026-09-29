Phase 144-6-R5-11
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-10 classified several final-claim providers as OTHER_STATEMENT and found
no non-root provider candidate for pi_10^4.

R5-11 inspects the typed semantic fields instead of using rule-name text.

Targets
-------
pi_10^4
pi_12^5
pi_15^8
pi_16^9

Statements of special interest
------------------------------
TodaProp515Pi12_5HopfIsomorphismStatement
Toda515Sigma8TransportedDecompositionStatement
Toda48Pi16_9OrderAndE4InjectiveStatement

For every target the audit prints:
- the root final claim,
- root inference rule for diagnostics,
- every direct root premise and all dataclass fields,
- known structural provider statements anywhere in full provenance,
- whether each structural statement is a direct root premise.

Questions
---------
1. Does pi_12^5 carry order-two information in typed statement fields?
2. Does pi_15^8 transported_group structurally encode sigma_8, E sigma-prime,
   and order 8?
3. Does pi_16^9 already carry order 16 and E^4 injectivity in a typed
   aggregate statement?
4. Is pi_10^4's composite generator/order available only in the root
   integration conclusion, or in a typed premise we can classify generically?

Rule names are printed only for diagnostics. They are not proposed as a
production semantic classifier.
