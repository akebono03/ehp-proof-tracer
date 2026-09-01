# ehp_proof 設計メモ

この文書は Phase 29 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

過去の `development_log.md` にある「未実装」「今後の課題」は、その Phase 時点の historical statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map facts / repository
        ↓
homotopy / EHP / map-property domain inference rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda / map-property statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

基本原則:

```text
実際の数学的必要
↓
必要最小限の表現
↓
explicit fact / domain rule
↓
既存機構
```

Phase 24 の theorem repository、Phase 25 / 26 の generator repository、Phase 27 の composition fact repository、Phase 28 の map-property statement / rule、Phase 29 の actual map fact / repository は責務を分離する。

generic inference engine に個別の generator / Toda theorem / composition fact / map fact を埋め込まない。

---

# 2. Expression / structural layer

現在の主要 Expression:

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

別の structural object:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Expression layer は syntax / structure を lossless に保持する。

この層が担当しないもの:

- theorem applicability
- theorem repository lookup
- generator fact repository lookup
- composition fact repository lookup
- map fact repository lookup
- map property theorem applicability
- literature provenance materialization
- generator notation からの automatic typing
- map notation からの typing / injectivity / isomorphism 推測
- automatic family formula
- general recursive repository traversal
- ambient homotopy-group validation
- stable homotopy classification

---

# 3. Structural equality の原則

Python equality は structural equality とする。

例:

```text
IteratedSuspension(alpha,1)
!=
Suspension(alpha)
```

```text
GeneratorSymbol(family="ν",decoration="′")
!=
GeneratorSymbol(family="ν",index=7)
```

```text
TodaBracket(...,index=1)
!=
TodaBracket(...,index=None)
```

typed / untyped `HomotopyElement` も structural に異なる。

```text
untyped η₃
!=
typed η₃ : S⁴ → S³
```

map property についても:

```text
IsomorphismStatement(f)
!=
InjectiveMapStatement(f)
```

Phase 29 では knowledge-layer map objects についても structural equality を採用する。

```text
MapSymbol(H)
!=
MapTypingFact(H context)
```

```text
MapIsomorphismFact(H context)
!=
IsomorphismStatement(H)
```

数学的 implication / knowledge materialization は structural equality ではなく explicit API / inference rule で表す。

---

# 4. Generic inference engine の境界

generic engine の責務:

```text
match
bind
apply
deduplicate
iterate
trace
```

Phase 29 でも generic engine は変更しない。

Theorem repository の責務:

```text
store
重複検査
lookup
literature provenance の materialize
GIVEN ProofStep の作成
```

Generator repository の責務:

```text
store
重複検査
exact generator lookup
typed HomotopyElement の materialize
typing / ambient facts の整合性照会
```

Composition fact repository の責務:

```text
primitive zero-composition fact の store
重複検査
exact composition lookup
必要最小限の typed/untyped structure lookup
```

Phase 28 map-property layer の責務:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism → injective
injective-map equality reflection
same-map applicability guard
```

Phase 29 map-fact layer の責務:

```text
actual map identity
map typing context
map isomorphism fact
exact typing-context repository lookup
knowledge fact → ProofStep.GIVEN materialization
```

---

# 5. Typed HomotopyElement semantics

現在:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
  generator: GeneratorSymbol | None
```

`None` は wildcard ではない。

重要:

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

全 field が structural equality に参加する。

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

# 7. Theorem repository

主要構造:

```text
TheoremFactEntry
TheoremFactRepository
```

現在の代表 theorem:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

production:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
THEOREM_FACT_REPOSITORY
```

重要:

```text
stored theorem
!=
automatically applicable theorem
```

theorem fact は matching definedness と組み合わさって初めて membership に接続される。

---

# 8. Generator facts

現在の production generator typing:

```text
η₃ : S⁴ → S³
ν′ : S⁶ → S³
ν₇ : S¹⁰ → S⁷
```

ambient-group facts:

```text
η₃ ∈ π₄(S³)
ν′ ∈ π₆(S³)
ν₇ ∈ π₁₀(S⁷)
```

repository:

```text
GENERATOR_FACT_REPOSITORY
```

typing fact と ambient-group fact は別 knowledge family とする。

---

# 9. GeneratorFactRepository semantics

現在の API:

```text
lookup_typing(generator)
lookup_ambient_group(generator)
materialize_typed_element(element)
is_typing_ambient_group_consistent(generator)
```

lookup は `GeneratorSymbol` structural equality に基づく。

未知 generator は `None`。

family fallback、index formula、display-name parsing は行わない。

---

# 10. Explicit Suspension typing

Phase 26 の pattern:

```text
repository-derived ν′ : S⁶ → S³
↓
existing Suspension semantics
↓
Eν′ : S⁷ → S⁴
```

repository に recursive expression typing API は追加していない。

```text
Suspension(untyped ν′)
→ source=None
→ target=None
```

notation alone から typing knowledge は生成しない。

---

# 11. Actual ε₃ Toda typing

Phase 26 で構築可能:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

actual typed bracket:

```text
{η₃,Eν′,ν₇}_1
```

重要:

```text
type-compatible
↛
zero composition
```

---

# 12. Phase 27 composition knowledge

primitive zero-composition facts:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
```

Suspension identification:

```text
Eν₆ = ν₇
```

`Eν₆ = ν₇` は `RelationType.EQUALITY` であり、zero-composition repository には入れない。

---

# 13. ZeroCompositionFactRepository

現在の構造:

```text
ZeroCompositionFactRepository
  facts: tuple[Relation,...]
```

production repository:

```text
ZERO_COMPOSITION_FACT_REPOSITORY
```

constructor は少なくとも:

```text
lhs is Composition
rhs == Zero()
relation_type == RelationType.ZERO
duplicate composition がない
```

を検査する。

---

# 14. Exact lookup と typed/untyped structure lookup

exact lookup:

```text
lookup(composition)
```

は structural equality を使う。

Phase 27 の actual bridge のため:

```text
lookup_by_untyped_structure(composition)
```

を持つ。

この API が無視するのは:

```text
HomotopyElement.source
HomotopyElement.target
```

のみ。

---

# 15. Corrected indexed Toda definedness semantics

current corrected input:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

一般形:

```text
a ∘ Eb = 0
b ∘ c = 0
Ec = d
↓
{a,Eb,d}_1 is defined
```

implementation:

```text
indexed_toda_bracket_index1_defined_inference_rule()
```

---

# 16. Corrected end-to-end Toda inference

production inputs:

```text
GIVEN
η₃ ∘ Eν′ = 0

GIVEN
ν′ ∘ ν₆ = 0

GIVEN
Eν₆ = ν₇

GIVEN
Toda theorem:
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

同一 fixed-point run:

```text
Round 1
{η₃,Eν′,ν₇}_1 is defined

Round 2
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

---

# 17. Phase 28 map-property statement layer

追加 statement:

```text
InjectiveMapStatement
IsomorphismStatement
```

最小構造:

```text
InjectiveMapStatement(map=f)
IsomorphismStatement(map=f)
```

重要:

```text
MapSymbol(f)
↛
InjectiveMapStatement(f)
```

```text
MapSymbol(f)
↛
IsomorphismStatement(f)
```

map notation だけから property knowledge を生成しない。

---

# 18. Injectivity と isomorphism の structural distinction

同一 map `f` でも:

```text
InjectiveMapStatement(f)
!=
IsomorphismStatement(f)
```

数学的 implication:

```text
Isomorphism(f)
⇒
Injective(f)
```

は explicit inference rule で表す。

---

# 19. Isomorphism → Injective inference

```text
isomorphism_implies_injective_inference_rule()
```

semantics:

```text
Isomorphism(f)
↓
Injective(f)
```

reverse implication は追加しない。

---

# 20. MapApplication equality representation

```text
MapApplication(map=f, expression=a)
```

は `f(a)` を表す。

```text
f(a)=f(b)
```

は `RelationType.EQUALITY` で表現する。

専用 `MapEqualityStatement` は追加しない。

---

# 21. Injective map equality reflection

```text
injective_map_reflects_equality_inference_rule()
```

semantics:

```text
Injective(f)
+
f(a)=f(b)
↓
a=b
```

guard は:

```text
lhs is MapApplication
rhs is MapApplication
lhs.map == rhs.map
injective_statement.map == lhs.map
```

を要求する。

---

# 22. Equality reflection の invalid boundary

```text
Injective(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + f(a)=g(b)
↛ a=b
```

```text
Injective(f) + plain a=b
↛ equality-reflection rule
```

---

# 23. Phase 28 end-to-end fixed-point inference

```text
GIVEN
Isomorphism(f)

GIVEN
f(a)=f(b)

Round 1
Injective(f)

Round 2
a=b
```

termination:

```text
InferenceTerminationReason.FIXED_POINT
```

---

# 24. Phase 28 provenance

final equality step:

```text
premises =
  derived Injective(f)
  mapped equality f(a)=f(b)
```

injectivity step:

```text
premises =
  Isomorphism(f)
```

---

# 25. Phase 29 actual map identity

Phase 29-1 で production map identity を追加:

```text
HOPF_MAP = MapSymbol(name="H")
```

意味:

```text
project-wide actual map identity for H
```

ただし:

```text
HOPF_MAP
↛ typing
↛ isomorphism
↛ injectivity
```

`MapSymbol` 自体は generic structural identity のまま保持する。

---

# 26. MapTypingFact semantics

Phase 29-2 で追加:

```text
MapTypingFact
```

fields:

```text
map: MapSymbol
source_group_dimension: int
source_sphere_dimension: int
target_group_dimension: int
target_sphere_dimension: int
```

これは:

```text
π_m(S^n) → π_p(S^q)
```

型の map context を lossless に保持する。

`MapSymbol` に source / target を埋め込まない。

Critical:

```text
MapSymbol
!=
MapTypingFact
```

同じ `MapSymbol("H")` が将来異なる degree/context に現れても structural に区別できる。

---

# 27. Actual H typing fact

Phase 29-3 production knowledge:

```text
HOPF_MAP_TYPING_FACT
```

represents:

```text
H : π₃(S²) → π₃(S³)
```

structure:

```text
map = HOPF_MAP
source = π₃(S²)
target = π₃(S³)
```

`HOPF_MAP` 自体は unchanged。

---

# 28. MapIsomorphismFact semantics

Phase 29-4 で追加:

```text
MapIsomorphismFact
  typing: MapTypingFact
```

意味:

```text
この typing context の map は isomorphism
```

property fact は map identity だけではなく typing context を structural identity に含める。

Critical:

```text
MapIsomorphismFact
!=
IsomorphismStatement
```

前者は knowledge-layer object、後者は proof-level statement。

---

# 29. MapIsomorphismFactRepository semantics

Phase 29-5 で追加:

```text
MapIsomorphismFactRepository
```

production:

```text
HOPF_MAP_ISOMORPHISM_FACT
MAP_ISOMORPHISM_FACT_REPOSITORY
```

actual fact:

```text
H : π₃(S²) → π₃(S³)
is an isomorphism
```

repository API:

```text
lookup(typing: MapTypingFact)
```

lookup は exact structural equality。

```text
unknown typing
→ None
```

```text
same H + different typing
→ separate context
```

同一 typing context の duplicate isomorphism fact は reject。

---

# 30. Map isomorphism fact materialization

Phase 29-6 で:

```text
MapIsomorphismFact.to_proof_step()
```

を追加。

materialization:

```text
knowledge fact
↓
ProofStep.GIVEN
↓
IsomorphismStatement(map=fact.typing.map)
```

これは inference ではない。

```text
rule = ProofRule.GIVEN
premises = ()
inference_rule = None
```

Current boundary:

proof-level `IsomorphismStatement` は typing context を保持せず map identity のみを保持する。

Phase 29 の actual production context は1件なので narrow bridge として許容する。

将来、同じ map identity の複数 typing context を同一 proof graph 上で同時に扱う必要が生じた場合に typed property statement を検討する。

---

# 31. Actual H isomorphism → injectivity connection

Phase 29-7 では production code を追加せず existing Phase 28 rule を再利用する。

```text
MAP_ISOMORPHISM_FACT_REPOSITORY
↓ lookup
HOPF_MAP_ISOMORPHISM_FACT
↓ to_proof_step()
GIVEN Isomorphism(H)
↓ existing inference
Injective(H)
```

provenance:

```text
Injective(H).premises =
  actual fact-derived Isomorphism(H) step
```

---

# 32. Actual H end-to-end equality reflection

Phase 29-8 representative chain:

```text
PRODUCTION FACT
H : π₃(S²) → π₃(S³) is an isomorphism

↓ materialize

GIVEN
Isomorphism(H)

↓
Injective(H)

+

GIVEN
H(a)=H(b)

↓
a=b
```

single fixed-point run:

```text
Round 1
Injective(H)

Round 2
a=b
```

termination:

```text
InferenceTerminationReason.FIXED_POINT
```

Important boundary:

```text
actual H property
+
representative mapped equality
```

までであり、actual mapped equality はまだ計算しない。

---

# 33. Phase 29 provenance / invalid / scope semantics

Phase 29-9 で actual-H chain に対して regression を固定。

full proof-level provenance:

```text
a=b
↓
Injective(H)
↓
Isomorphism(H) GIVEN
```

and:

```text
a=b
↓
H(a)=H(b)
```

Different map:

```text
Injective(H) + g(a)=g(b)
↛ a=b
```

Unknown typing:

```text
same MapSymbol("H")
+
unregistered typing context
↛ H isomorphism fact
```

Unrelated fact:

```text
unrelated fact
↛ Injective(H) premises
↛ a=b premises
```

Deduplication:

```text
Injective(H)
→ exactly 1 derived step
```

```text
a=b
→ exactly 1 derived step
```

Genuine fixed point:

```text
derive_inference_round_result(
  rules,
  result.steps,
)
```

returns:

```text
new_steps == ()
```

---

# 34. Knowledge provenance boundary

`MapIsomorphismFact.to_proof_step()` は current proof graph に:

```text
ProofStep.GIVEN(Isomorphism(H))
```

を投入する。

現在、`ProofStep.premises` に `MapIsomorphismFact` 自体は保持しない。

したがって first-class proof-level provenance は:

```text
Isomorphism(H) GIVEN
↓
Injective(H)
↓
a=b
```

まで。

knowledge supply provenance:

```text
HOPF_MAP_ISOMORPHISM_FACT
↓ to_proof_step()
Isomorphism(H) GIVEN
```

は materialization API と repository lookup により追跡できるが、`ProofStep` graph の premise object ではない。

この provenance model を拡張する具体的必要が出るまで一般化しない。

---

# 35. Phase 29 representative probe

実行:

```powershell
python -m probes.probe_phase29_capabilities
```

表示:

```text
PRODUCTION FACT
H : π₃(S²) → π₃(S³) is an isomorphism

MATERIALIZE
↓

GIVEN
H is an isomorphism

INFERENCE
isomorphism implies injectivity
↓
H is injective

GIVEN
H(a)=H(b)

INFERENCE
injective map reflects equality
↓
a=b
```

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

---

# 36. Phase 29 completion boundary

実装済み:

```text
HOPF_MAP
MapTypingFact
HOPF_MAP_TYPING_FACT
MapIsomorphismFact
HOPF_MAP_ISOMORPHISM_FACT
MapIsomorphismFactRepository
MAP_ISOMORPHISM_FACT_REPOSITORY
exact typing-context lookup
duplicate fact rejection
MapIsomorphismFact.to_proof_step()
actual fact → IsomorphismStatement(H)
actual Isomorphism(H) → Injective(H)
actual-H fact-driven equality reflection
full proof-level provenance regression
different-map rejection
unknown-typing-context rejection
unrelated-fact exclusion
deduplication
genuine fixed-point regression
human-readable Phase 29 capability probe
```

generic inference engine:

```text
変更なし
```

最終確認:

```text
full suite
1408 passed in 96.81s
```

---

# 37. Phase 29 non-goals

未実装:

- typed `MapSymbol` domain / codomain
- typing-aware proof-level map-property statement
- literature provenance for map facts
- map fact as first-class `ProofStep` premise provenance
- Hopf formula
- smash product
- actual calculation of `H((2ι₂)η₂)`
- actual mapped equality `H((2ι₂)η₂)=H(4η₂)`
- actual proof `(2ι₂)η₂=4η₂`
- `SurjectiveMapStatement`
- preimage representation
- kernel-modulo equality shortcut

---

# 38. 次の設計境界

Phase 29 で:

```text
actual H mathematical knowledge
↓
proof-level Isomorphism(H)
↓
Injective(H)
↓
equality reflection
```

まで完成した。

次の Phase 30 は:

```text
Hopf formula minimum representation
```

を推奨する。

対象となる代表式:

```text
H(γ α)=(γ∧γ)H(α)
```

ただし Phase 30 では formula を structural に表現する最小 layer から開始し、無条件 generic rewrite や smash product の全面実装を先取りしない。

長期 dependency:

```text
Phase 29
actual H facts / equality reflection
↓
Phase 30
Hopf formula minimum representation
↓
Phase 31
smash product
↓
Phase 32+
actual H calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing equality reflection
↓
(2ι₂)η₂=4η₂
```

---

# 39. テスト原則

新しい数学的 layer ごとに:

1. 表現
2. structural distinction
3. validity / applicability
4. invalid case
5. integration
6. provenance
7. representative scenario
8. termination / scope
9. full regression
10. human-readable probe

を確認する。

structural-only Phase では存在しない inference / provenance を先取りしない。

---

# 40. 文書運用方針

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

current specification は latest README / design を優先する。
