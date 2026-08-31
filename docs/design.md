# ehp_proof 設計メモ

この文書は Phase 25 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

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

Phase 24 / 25 の repository layer は既知 knowledge の供給を担当し、新しい数学的推論そのものを generic engine に埋め込まない。

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
- ambient homotopy-group validation
- automatic generator-to-typing inference
- recursive global expression typing
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
GeneratorSymbol(family="η",index=3)
!=structural
GeneratorSymbol(family="μ",index=3)
```

```text
TodaBracket(...,index=1)
!=structural
TodaBracket(...,index=None)
```

Phase 24 theorem lookup と Phase 25 generator lookup は structural identity を current narrow lookup key として再利用する。

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

Phase 25 でも generic inference engine は変更しない。

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

# 8. Phase 25 design goal

Goal:

```text
GeneratorSymbol
+
explicit generator fact
↓
repository lookup
↓
typed HomotopyElement / ambient-group knowledge
```

Anti-goal:

```text
GeneratorSymbol.index
↓
family-specific formula
↓
automatic source / target
```

---

# 9. GeneratorTypingFact semantics

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

Representative:

```text
η₃ : S⁴ → S³
```

Current production fact: `ETA_3_TYPING_FACT`.

---

# 10. GeneratorAmbientGroupFact semantics

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

Representative:

```text
η₃ ∈ π₄(S³)
```

Current production fact: `ETA_3_AMBIENT_GROUP_FACT`.

Critical:

```text
typing fact
!=
ambient-group fact
```

No conversion or consistency rule between these fact families is introduced.

---

# 11. Representative generator identity

```text
ETA_3_GENERATOR
=
GeneratorSymbol(family="η", index=3)
```

This is production data, not a parsing rule.

---

# 12. GeneratorFactRepository

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
```

Production repository: `GENERATOR_FACT_REPOSITORY`.

No theorem facts are stored here.

---

# 13. Generator repository lookup semantics

Lookup identity:

```text
GeneratorSymbol structural equality
```

Therefore:

```text
η₃ → exact match
η₄ → no match
η → no match
μ₃ → no match
```

Unknown result is `None`.

No family fallback. No index inference. No display-name parsing. `HomotopyElement.name` is never used as the lookup key.

---

# 14. Repository uniqueness semantics

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

---

# 15. Typed-element materialization semantics

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

# 16. Existing / partial typing boundary

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

# 17. Ambient-group knowledge boundary

`GeneratorAmbientGroupFact` does not materialize source / target.

```text
ambient-group fact only
↛
typed HomotopyElement
```

No current rule states:

```text
group_dimension == source
sphere_dimension == target
```

---

# 18. Toda integration boundary

Phase 25 does not modify `TodaBracket`.

Instead:

```text
GeneratorTypingFact
↓
GeneratorFactRepository
↓
typed HomotopyElement
↓
TodaBracket
↓
existing compatibility query
```

No recursive bracket materializer is introduced.

---

# 19. Generator fact provenance semantics

Current provenance is data-path provenance:

```text
typed element
← materialize_typed_element()
← registered typing fact
← repository
```

No generator-fact `LiteratureReference`. No generator-fact `ProofStep.GIVEN`. No inference rule for materialization.

---

# 20. Repository separation

Current repositories:

```text
THEOREM_FACT_REPOSITORY
GENERATOR_FACT_REPOSITORY
```

are separate.

Do not unify these repositories until an actual cross-family requirement exists.

---

# 21. Phase 25 completion boundary

Implemented:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
exact structural lookup
unknown lookup boundary
duplicate rejection per fact family
explicit typed-element materialization
non-mutating materialization
already-typed / partial-typing protection
Toda compatibility connection
scope / repository-separation regression
```

Critical boundaries:

```text
GeneratorSymbol.index
↛
automatic typing
```

```text
HomotopyElement.name
↛
generator lookup
```

```text
ambient-group fact
↛
source / target materialization
```

```text
lookup / materialization
↛
generic inference engine
```

```text
generator repository
!=
theorem repository
```

Verified:

```text
tests/test_generator_facts.py
55 passed in 2.25s
```

```text
full suite
1245 passed in 65.71s
```

Generic inference engine unchanged.

---

# 22. Phase 25 non-goals

Not implemented:

- generator-fact `LiteratureReference`,
- generator-fact `ProofStep`,
- generator-fact inference rules,
- external generator-table loader,
- stable fact key / ID,
- name / generator consistency validation,
- `HomotopyElement.dimension` / generator validation,
- typing / ambient-group consistency validation,
- automatic η_n / ν_n / μ_n / ι_n typing,
- recursive expression typing,
- automatic typing of `Suspension(ν′)` from ν′ data,
- actual full ε₃ Toda entry typing from production generator facts,
- stable / unstable generator classification,
- stable homotopy groups,
- stable Toda brackets,
- higher Toda brackets.

---

# 23. Next design boundary

Natural next candidate:

```text
Phase 26
Generator fact provenance / actual Toda-generator typing expansion
```

Potential sub-directions:

```text
LiteratureReference-backed generator fact
ν′ / ν₇ production typing facts
typing ↔ ambient-group consistency validation
explicit nested Suspension typing from generator facts
```

Do not implement all directions together.

---

# 24. Testing principle

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

Structural-only Phase では存在しない inference / provenance を先取りしない。

---

# 25. Documentation policy

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
