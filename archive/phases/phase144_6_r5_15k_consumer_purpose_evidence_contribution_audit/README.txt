Phase 144-6-R5-15K
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15J showed that structural statement shape alone cannot decide Narrative
visibility:
- direct PROVIDER_INPUT: 11 total, 7 visible, 4 hidden
- provider mixed structural shapes: 2
- residual: 109 visible, 2239 hidden
- all 4 visible residual structural shapes also occur hidden

R5-15K changes the unit of analysis from "what kind of statement is this?"
to "what does this premise contribute to this consumer?"

Evidence-contribution candidates
--------------------------------
ESTABLISH_GROUP
ESTABLISH_MAP
ESTABLISH_ISOMORPHISM
ESTABLISH_INJECTIVITY
ESTABLISH_SURJECTIVITY
ESTABLISH_ZERO
ESTABLISH_ORDER
ESTABLISH_DECOMPOSITION
ESTABLISH_RELATION
PROVIDE_REFERENCE
PROVIDE_PRECONDITION
SHARED_SEMANTIC_INPUT
UNRESOLVED

Consumer purpose
----------------
Derived from existing generic Narrative block roles and structural consumer
features. Concrete n/k values are not used.

Semantic overlap
----------------
The audit also records structural value overlap between premise and consumer
dataclass fields. Primitive int/bool/str values are excluded from overlap.

Constraints
-----------
No n/k-specific visibility rule.
No inference-rule-name parsing.
No production visibility changes.
No pytest because production code is unchanged.
Class-name hints are diagnostic only and do not decide visibility.
