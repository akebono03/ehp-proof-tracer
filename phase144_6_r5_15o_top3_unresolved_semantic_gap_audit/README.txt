Phase 144-6-R5-15O
====================

Top-3 unresolved semantic gap audit.

Scope
-----
Audit only.

15N found 968 production-visible unresolved premise edges. The top three
statement populations account for 912 / 968:

- TodaProp42ExactnessStatement: 672
- TodaNuFamilyDefinitionStatement: 184
- TodaBracketMembershipStatement: 56

15O asks whether those populations already carry generic mathematical block
roles before the 15M evidence-contribution mapper.

Current-code observation
------------------------
The current generic block recognizer already maps:

- TodaProp42ExactnessStatement -> EXACTNESS
- TodaNuFamilyDefinitionStatement -> DEFINITION via DEFINITION_STATEMENT_TYPES

The audit verifies these mappings across the actual six-target population and
checks TodaBracketMembershipStatement as well.

The audit prints:
- generic block role distribution,
- visibility x current 15M contribution,
- dataclass field signatures,
- top consumer statement types,
- projected visible resolution if the top-3 mapper gap is filled.

Boundary
--------
No production code is changed.
No visibility policy is changed.
No existing test is changed.
No project document is changed.
No n/k-specific production rule is introduced.
No inference-rule-name parsing is introduced.

Statement class names are used only to select the known 15N top-3 audit
population. They are not proposed as production classification rules.

The full test suite is not run because Phase 144 is still in progress.
