Phase 143-75AF audit

Target:
TodaProp44FirstSummandRestrictionStatement

Established current inventory:
- 19 fallback occurrences
- 19 groups

GitHub related tests establish:
- fields are decomposition_map and suspension_map
- the suspension source must be the first direct summand
- the targets must agree
- this statement itself does NOT assert injectivity
- this statement itself does NOT assert isomorphism

This audit captures all target renderer calls from the current local proof
inventory and checks the first-summand/source and target correspondence.

No production changes.
No test changes.
No docs changes.
No pytest.
