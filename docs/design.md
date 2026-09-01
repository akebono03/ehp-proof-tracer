# ehp_proof 設計メモ

この文書は Phase 26 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

過去の development log にある「未実装」「今後の課題」は historical statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
literature-backed theorem facts / repository
explicit generator facts / repository
        ↓
homotopy / EHP domain inference rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

基本原則:

```text
actual mathematical need
↓
minimal explicit representation
↓
knowledge supply / domain rule
↓
existing machinery
```

Phase 24 theorem repository と Phase 25 / 26 generator repository は既知 knowledge の供給を担当する。

Generic inference engine に generator-specific knowledge を埋め込まない。

---

# 2. Expression / structural layer

Current tree:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Separate structural objects:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Expression layer は syntax / structure を lossless に保持する。

担当しないもの:

- theorem applicability
- theorem repository lookup
- generator fact repository lookup
- literature provenance materialization
- automatic generator-to-typing inference
- automatic family formulas
- recursive repository traversal
- ambient homotopy-group validation
- stable homotopy classification

---

# 3. Structural equality principle

Python equality は structural equality。

Examples:

```text
IteratedSuspension(alpha,1)
!=structural
Suspension(alpha)
```

```text
GeneratorSymbol(family="ν",decoration="′")
!=structural
GeneratorSymbol(family="ν",index=7)
```

```text
TodaBracket(...,index=1)
!=structural
TodaBracket(...,index=None)
```

Typed / untyped HomotopyElement も structural に異なる。

```text
untyped η₃
!=structural
typed η₃ : S⁴ → S³
```

Therefore theorem-side untyped Toda notation と Phase 26 typed representative は bracket 全体の structural equality を要求しない。

---

# 4. Generic inference engine boundary

Engine responsibilities:

```text
match
bind
apply
deduplicate
iterate
trace
```

Phase 26 でも generic inference engine は変更しない。

Theorem repository responsibilities:

```text
store
validate uniqueness
lookup
materialize literature provenance
create existing-style GIVEN input
```

Generator repository responsibilities:

```text
store
validate uniqueness
lookup exact generator identity
materialize a new typed HomotopyElement
compare typing / ambient facts when explicitly requested
```

Generator repository は inference run を起動しない。

---

# 5. Typed HomotopyElement semantics

Current:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
  generator: GeneratorSymbol | None
```

`None` は wildcard ではない。

Important:

```text
type compatibility
!=
ZERO
!=
Toda definedness
```

---

# 6. GeneratorSymbol semantics

```text
GeneratorSymbol
  family: str
  index: int | None
  decoration: str | None
```

All fields participate in structural equality.

Critical:

```text
GeneratorSymbol.index
↛
automatic typing
```

```text
GeneratorSymbol.decoration
↛
automatic typing
```

`index=None` / `decoration=None` は wildcard ではない。

---

# 7. Phase 24 theorem repository

Structures:

```text
TheoremFactEntry
TheoremFactRepository
```

Current narrow fact family:

```text
TodaBracketMembershipTheoremStatement
```

Representative actual theorem:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Important:

```text
stored theorem
!=
automatically applicable theorem
```

```text
theorem repository
!=
universal theorem system
```

---

# 8. GeneratorTypingFact semantics

```text
GeneratorTypingFact
  generator: GeneratorSymbol
  source: int
  target: int
```

Meaning:

```text
generator : S^source → S^target
```

Current production typing facts:

```text
η₃ : S⁴ → S³
ν′ : S⁶ → S³
ν₇ : S¹⁰ → S⁷
```

---

# 9. GeneratorAmbientGroupFact semantics

```text
GeneratorAmbientGroupFact
  generator: GeneratorSymbol
  group_dimension: int
  sphere_dimension: int
```

Meaning:

```text
generator ∈ π_group_dimension(S^sphere_dimension)
```

Current production ambient-group facts:

```text
η₃ ∈ π₄(S³)
ν′ ∈ π₆(S³)
ν₇ ∈ π₁₀(S⁷)
```

Critical:

```text
typing fact
!=
ambient-group fact
```

No automatic conversion between the two fact families is introduced.

---

# 10. Production generator identities

```text
ETA_3_GENERATOR
=
GeneratorSymbol(family="η", index=3)
```

```text
NU_PRIME_GENERATOR
=
GeneratorSymbol(family="ν", decoration="′")
```

```text
NU_7_GENERATOR
=
GeneratorSymbol(family="ν", index=7)
```

These are production data, not parsing rules or family formulas.

---

# 11. GeneratorFactRepository

Current structure:

```text
GeneratorFactRepository
├── typing_facts
└── ambient_group_facts
```

Current APIs:

```text
lookup_typing(generator)
lookup_ambient_group(generator)
materialize_typed_element(element)
is_typing_ambient_group_consistent(generator)
```

Production repository:

```text
GENERATOR_FACT_REPOSITORY
```

Production coverage:

```text
η₃
ν′
ν₇
```

No theorem facts are stored here.

---

# 12. Generator repository lookup semantics

Lookup identity:

```text
GeneratorSymbol structural equality
```

Examples:

```text
η₃ → exact match
ν′ → exact match
ν₇ → exact match
ν₈ → no match
ν → no match
```

Unknown result is `None`.

No family fallback. No index inference. No display-name parsing. `HomotopyElement.name` is never used as the lookup key.

---

# 13. Repository uniqueness semantics

Within `typing_facts`:

```text
same generator appears twice
→ ValueError
```

Within `ambient_group_facts`:

```text
same generator appears twice
→ ValueError
```

Cross-family:

```text
one typing fact
+
one ambient-group fact
for same generator
→ allowed
```

Cross-family disagreement does not make repository construction fail in Phase 26.

---

# 14. Typed-element materialization semantics

```text
materialize_typed_element(element)
→ HomotopyElement | None
```

Success requires:

```text
element.generator is not None
element.source is None
element.target is None
matching GeneratorTypingFact exists
```

On success, a new `HomotopyElement` is returned with source / target from the registered fact.

Preserved:

```text
name
dimension
generator
```

Original element is not mutated.

---

# 15. Existing / partial typing boundary

Already typed or partially typed elements are not overwritten or completed.

```text
source=4,target=None
→ no implicit completion
```

```text
source=5,target=3
+
repository says source=4,target=3
→ no overwrite
```

---

# 16. Explicit Suspension typing connection

Phase 26 does not add a repository method such as:

```text
materialize_typed_suspension()
```

and does not add recursive expression typing.

Instead:

```text
repository-derived ν′ : S⁶ → S³
↓
existing Suspension semantics
↓
Eν′ : S⁷ → S⁴
```

The base element must be explicitly materialized first.

```text
Suspension(untyped ν′)
→ source=None
→ target=None
```

This preserves the rule:

```text
notation alone
↛
typing knowledge
```

---

# 17. Actual ε₃ Toda entry representation

Phase 26 can construct:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

and:

```text
TodaBracket(
  first=typed η₃,
  second=Suspension(typed ν′),
  third=typed ν₇,
  index=1,
)
```

This is the typed representative of:

```text
{η₃,Eν′,ν₇}_1
```

The theorem-side bracket and typed bracket share:

```text
first generator identity
second base generator identity under Suspension
third generator identity
index=1
```

but are not required to be structurally equal because the typed entries contain source / target annotations.

---

# 18. Toda type compatibility semantics

Current query:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

For the actual bracket:

```text
η₃.source == Eν′.target == 4
Eν′.source == ν₇.target == 7
```

Therefore:

```text
η₃ ∘ Eν′
→ type-compatible
```

```text
Eν′ ∘ ν₇
→ type-compatible
```

and:

```text
{η₃,Eν′,ν₇}_1
→ defining compositions are type-compatible
```

`TodaBracket.index` is not part of the current compatibility predicate.

Critical:

```text
type compatibility
!=
zero composition
!=
Toda definedness
```

---

# 19. Typing / ambient-group consistency semantics

Phase 26 adds:

```text
is_typing_ambient_group_consistent(generator)
→ bool | None
```

Semantics:

```text
True
=
both facts exist and agree
```

```text
False
=
both facts exist and disagree
```

```text
None
=
consistency cannot be evaluated because one or both facts are missing
```

Agreement means:

```text
typing.source == ambient.group_dimension
and
typing.target == ambient.sphere_dimension
```

Production results:

```text
η₃ → True
ν′ → True
ν₇ → True
```

Important:

```text
consistency query
↛
new typing fact
```

```text
consistency query
↛
new ambient-group fact
```

```text
False
↛
repository construction failure
```

---

# 20. Generator fact provenance semantics

Current provenance is data-path provenance.

```text
typed η₃
← materialize_typed_element()
← ETA_3_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

```text
typed Eν′
← Suspension
← typed ν′
← materialize_typed_element()
← NU_PRIME_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

```text
typed ν₇
← materialize_typed_element()
← NU_7_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

No generator-fact `LiteratureReference`.
No generator-fact `ProofStep.GIVEN`.
No inference rule for materialization.

---

# 21. Repository separation

Current repositories:

```text
THEOREM_FACT_REPOSITORY
GENERATOR_FACT_REPOSITORY
```

are separate.

Phase 26 regression ensures that generator materialization, Suspension construction, Toda compatibility checks, and consistency queries do not modify theorem repository state.

Do not unify these repositories until an actual cross-family requirement exists.

---

# 22. Phase 26 completion boundary

Implemented:

```text
NU_PRIME_GENERATOR
NU_PRIME_TYPING_FACT
NU_PRIME_AMBIENT_GROUP_FACT
NU_7_GENERATOR
NU_7_TYPING_FACT
NU_7_AMBIENT_GROUP_FACT
production registration of η₃ / ν′ / ν₇
production lookup for all six facts
production materialization of ν′ / ν₇
explicit ν′ → Eν′ typing connection via Suspension
actual typed η₃ / Eν′ / ν₇ entries
actual indexed ε₃ Toda representative
actual defining-composition type compatibility
index / compatibility separation
is_typing_ambient_group_consistent()
True / False / None consistency semantics
repository non-mutation regression
theorem repository non-mutation regression
consistency-query non-generation regression
no automatic ν_n family typing
explicit data-path provenance regression
```

Verified:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

Generic inference engine unchanged.

---

# 23. Phase 26 non-goals

Not implemented:

- generator-fact `LiteratureReference`,
- generator-fact `ProofStep`,
- generator-fact inference rules,
- external generator-table loader,
- stable fact key / ID,
- name / generator consistency validation,
- `HomotopyElement.dimension` / generator validation,
- automatic η_n / ν_n / μ_n / ι_n typing,
- recursive expression typing,
- repository traversal through arbitrary `Suspension`,
- ambient validation of arbitrary expressions,
- zero-composition facts for `η₃ ∘ Eν′` or `Eν′ ∘ ν₇`,
- automatic Toda definedness from type compatibility,
- automatic theorem applicability from typing,
- stable / unstable generator classification,
- stable homotopy groups,
- stable Toda brackets,
- higher Toda brackets.

---

# 24. Representative capability demo policy

Each suitable Phase completion should include a representative probe using production APIs.

Purpose:

```text
pytest
=
correctness / regression
```

```text
representative probe
=
human-readable mathematical capability demonstration
```

Phase 26 representative command:

```powershell
python -m probes.probe_phase26_capabilities
```

Expected visible chain:

```text
η₃ fact
ν′ fact
ν₇ fact
↓
GENERATOR_FACT_REPOSITORY
↓
typed η₃ / ν′ / ν₇
↓
Suspension
↓
typed Eν′
↓
{η₃,Eν′,ν₇}_1
↓
defining compositions are type-compatible
```

The probe may also display the existing theorem-side result:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

but must clearly distinguish:

```text
type compatibility
```

from:

```text
Toda definedness / membership inference
```

---

# 25. Next design boundary

A natural next direction is to deepen the same actual ε₃ proof chain.

Possible sequence:

```text
actual typed entries
↓
explicit zero-composition facts
↓
Toda definedness
↓
existing theorem fact
↓
ε₃ membership
↓
proof trace
```

Alternative next topics:

```text
generator-fact LiteratureReference
name / dimension / generator validation
external generator table loading
```

Do not widen all directions at once.

---

# 26. Testing principle

For each new mathematical layer:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. integration
6. provenance if inference exists
7. representative scenario
8. termination / scope boundary
9. full regression
10. human-readable representative demo when useful

Structural-only or validation-only Phase では存在しない inference / provenance を先取りしない。

---

# 27. Documentation policy

```text
README.md
=
current capabilities / current status

 docs/design.md
=
current architecture / semantics / boundaries

 docs/development_log.md
=
chronological implementation history

 docs/roadmap.md
=
future capability dependency
```

Current specification は latest README / design を優先する。
