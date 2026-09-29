Phase 144-6-R5-15Q
====================

Remaining 49 visible unresolved edge audit.

Scope
-----
Audit only.

15P measured:
- visible_edges = 2698
- visible_resolved_edges = 2649
- visible_unresolved_edges = 49
- visible_resolution_ratio = 0.981838

15Q does not add another EvidenceContribution.

Main question
-------------
The 15P visibility metric is step-global: if a premise step is visible in any
Argument local body, every edge using that premise step can be counted as
visible.

15Q therefore distinguishes:

- EDGE_LOCAL_VISIBLE
- EDGE_LOCAL_HIDDEN
- EDGE_LOCAL_OTHER
- CONSUMER_ARGUMENT_NO_PREMISE_LOCAL
- CONSUMER_NOT_ARGUMENT_CONCLUSION

For each of the 49 step-global visible unresolved edges, the audit also prints:
- premise statement type,
- premise generic block role,
- consumer statement type,
- consumer generic block role,
- premise dataclass field signature.

Decision rule
-------------
Only EDGE_LOCAL_VISIBLE unresolved edges are strong candidates for a genuine
new generic EvidenceContribution.

Edges visible only because the same premise step is used elsewhere should not
drive vocabulary expansion.

Boundary
--------
No production code is changed.
No contribution enum is changed.
No mapper is changed.
No R4 visibility is changed.
No renderer, CLI, Web, or project document is changed.
No statement class name is used as a production rule.
No n/k-specific production rule is introduced.

Focused pytest only. Full pytest remains deferred until the end of Phase 144.
