Phase 144-6-R5-15J
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15I reduced the unresolved Narrative problem to:
- 11 direct PROVIDER_INPUT SUPPORT_ONLY edges
  - 7 visible
  - 4 hidden
- 109 visible nested RESIDUAL_SUPPORT edges
- 2239 hidden nested RESIDUAL_SUPPORT edges

R5-15J asks whether those differences can be explained by generic structural
statement shape rather than target identity, n/k, or inference-rule names.

Structural shape
----------------
The audit records dataclass field value categories such as:
- homotopy/toda-primary group
- homotopy map
- group structure
- relation
- boolean property
- integer parameter
- nested semantic object
- collection
- domain object

Concrete field values are not part of the shape key.

Diagnostics
-----------
Class-name lexical hints such as "isomorphism", "finite dimensional", "lemma",
and "decomposition" are printed only as audit diagnostics. They do NOT decide
classification or visibility.

Key questions
-------------
1. Do visible and hidden provider inputs have different structural shapes?
2. Does one structural shape occur on both sides?
3. How many distinct shapes explain the 109 visible residual edges?
4. How often are visible residual shapes also common among the 2239 hidden
   residual edges?

Constraints
-----------
No n/k-specific visibility rule.
No inference-rule-name parsing for visibility.
No production visibility changes.
No pytest because production code is unchanged.
