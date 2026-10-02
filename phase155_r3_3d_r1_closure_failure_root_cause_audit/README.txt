Phase 155-R3-3D-r1 — closure failure root-cause audit

R3-3D passed the critical safety checks but closure remained false because:
- 2 removable pairs still have both endpoints present.
- 8 source-level duplicate top-level test names remain.

This package changes nothing. It identifies the exact remaining pairs and
duplicate-name groups, determines whether duplicate definitions have identical
or divergent AST bodies, and checks whether the unresolved pair endpoints
overlap those source-level duplicate names.

Repository-wide pytest is NOT run.
