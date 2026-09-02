# ehp_proof 設計メモ

この文書は Phase 31 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

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
├── SmashProduct
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

Phase 30 / 31 でも generic engine は変更しない。

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

# 38. Phase 30 right Prop.2.2 representation boundary

Phase 30 の対象は [Toda] Prop.2.2 の右側公式:

```text
H(a ∘ Eb)=H(a) ∘ Eb
```

のみ。

この式は新しい dedicated formula object を導入せず、既存 structural objects:

```text
MapApplication
Composition
Suspension
Relation(RelationType.EQUALITY)
```

で lossless に表現する。

重要:

```text
representable formula
!=
automatically valid theorem instance
```

---

# 39. Phase 11 Hopf statement と actual-H equality の distinction

Phase 11 の:

```text
HopfInvariantStatement(
  expression=a,
  value=β,
)
```

と proof-level actual-H equality:

```text
Relation(
  lhs=MapApplication(H,a),
  rhs=β,
  relation_type=EQUALITY,
)
```

は structural に別 object。

```text
HopfInvariantStatement
!=
Relation(MapApplication(H,...))
```

`HopfInvariantStatement` 自体は map field を持たない。

したがって implicit conversion は行わない。

---

# 40. HopfInvariantStatement → actual EHP H equality bridge

Phase 30 で利用する explicit bridge:

```text
hopf_invariant_statement_to_ehp_h_equality_inference_rule()
```

semantics:

```text
HopfInvariantStatement(x,y)
↓
H(x)=y
```

production map identity:

```text
EHP_H_MAP
```

を使用する。

この bridge は mathematical inference として `ProofRule.INFERENCE` を持ち、premise は元の Hopf statement step。

---

# 41. Existing generalized Hopf composition law reuse

Phase 30 は Phase 11 の:

```text
hopf_composition_law_inference_rule()
hopf_composition_formula_inference_rule()
```

を変更せず再利用する。

base fact:

```text
H(a)=β
```

から:

```text
HopfCompositionLawStatement(
  alpha=a,
  beta=β,
)
```

を得て、さらに expression `b` と組み合わせ:

```text
HopfInvariantStatement(
  expression=a ∘ Eb,
  value=β ∘ Eb,
)
```

を得る。

actual-H bridge 後:

```text
H(a ∘ Eb)=β ∘ Eb
```

となる。

---

# 42. Right-hand branch construction

base actual-H equality:

```text
H(a)=β
```

に対して existing generic equality rules を staged に使う。

```text
H(a)=β
↓ equality symmetry
β=H(a)
```

次に:

```text
β=H(a)
↓ equality preserved under right composition by Eb
β ∘ Eb=H(a) ∘ Eb
```

この段階では right-composition rule は1回だけ明示適用する。

---

# 43. Prop.2.2 right-formula closure

二つの equality:

```text
H(a ∘ Eb)=β ∘ Eb
```

```text
β ∘ Eb=H(a) ∘ Eb
```

に existing:

```text
equality_transitivity_inference_rule()
```

を適用して:

```text
H(a ∘ Eb)=H(a) ∘ Eb
```

を得る。

専用の「H preserves composition」rule は導入しない。

重要:

```text
Toda Prop.2.2 right formula
!=
general H composition homomorphism law
```

---

# 44. Provenance semantics

final equality step:

```text
premises =
  H(a∘Eb)=β∘Eb step
  β∘Eb=H(a)∘Eb step
```

left branch:

```text
final premise
↓
actual-H bridge
↓
Hopf composition formula
↓
Hopf composition law
↓
base Hopf fact
```

right branch:

```text
final premise
↓
staged right composition
↓
equality symmetry
↓
actual-H bridge
↓
base Hopf fact
```

同じ base Hopf fact から分岐していることを proof graph 上で保持する。

---

# 45. Invalid / mismatch semantics

Phase 30 regressions は少なくとも以下を reject する。

```text
H(a∘b)=H(a)∘b
```

は suspended right factor を持つ formula と structural に同一視しない。

```text
H(a∘Eb)=β∘Eb
γ∘Eb=H(a)∘Eb
```

で `β != γ` なら transitivity closure しない。

```text
H(a∘Eb)=β∘Eb
β∘Ec=H(a)∘Ec
```

で `Eb != Ec` なら closure しない。

unrelated equality は final provenance に入らない。

さらに別の valid Hopf fact:

```text
H(c)=γ
```

から:

```text
γ∘Eb=H(c)∘Eb
```

が正しく導出できても、`a / β` branch の Prop.2.2 closure には使えない。

---

# 46. Right-composition staged-rule boundary

```text
equality_preserved_under_right_composition_inference_rule(Eb)
```

は structural growth を生む productive rule。

同じ rule を再適用すると:

```text
x=y
↓
x∘Eb=y∘Eb
↓
(x∘Eb)∘Eb=(y∘Eb)∘Eb
↓
...
```

となり得る。

したがって Phase 30 の representative proof では:

```text
right composition
=
one staged application
```

とする。

これは engine-side の hidden termination ではなく active-rule scope の設計判断。

---

# 47. Terminal / deduplication semantics

最終 transitivity conclusion:

```text
H(a∘Eb)=H(a)∘Eb
```

は tested round 内で一意に derived される。

最終 transitivity rule を既知 steps に対して再度適用した terminal round は:

```text
new_steps == ()
```

となる。

ただし staged right-composition rule を unrestricted fixed-point rule set に含めた termination を主張しているわけではない。

---

# 48. Phase 30 representative probe

実行:

```powershell
python -m probes.probe_phase30_capabilities
```

表示する proof chain:

```text
GIVEN H(a)=β
↓
Hopf composition law
↓
H(a∘Eb)=β∘Eb
```

and:

```text
H(a)=β
↓ symmetry
β=H(a)
↓ staged right composition
β∘Eb=H(a)∘Eb
```

then:

```text
transitivity
↓
H(a∘Eb)=H(a)∘Eb
```

probe は production APIs と existing inference rules を再利用し、数学的推論を別実装しない。

---

# 49. Phase 30 completion boundary

実装済み:

```text
right Prop.2.2 formula structural representation
Phase 11 Hopf statement / actual-H equality distinction
explicit actual EHP H equality bridge
existing Hopf composition law reuse
existing Hopf composition formula reuse
actual H(a∘Eb)=β∘Eb equality
actual H(a)=β equality
symmetry bridge
staged right-composition bridge
transitivity closure
H(a∘Eb)=H(a)∘Eb
full proof provenance
mismatch rejection
right-factor mismatch rejection
unrelated equality exclusion
unrelated valid Hopf branch rejection
round-level deduplication
terminal transitivity regression
staged structural-growth boundary
human-readable Phase 30 probe
```

generic inference engine:

```text
変更なし
```

verified:

```text
tests/test_phase30_prop22.py
21 passed in 0.19s
```

```text
full suite
1439 passed in 23.44s
```

---

# 50. Phase 30 non-goals

Phase 30 では未実装:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

および:

- `SmashProduct`
- general smash-product algebra
- Barratt-Hilton Prop.3.1
- symbolic scalar `(-1)^n` expression tree
- actual `H((2ι₂)η₂)` calculation
- actual `H((2ι₂)η₂)=H(4η₂)`
- actual `(2ι₂)η₂=4η₂`

右側公式を一般の「H preserves composition」へ一般化しない。

---

# 51. 次の設計境界

Phase 30 で:

```text
H(a∘Eb)=H(a)∘Eb
```

まで proof-level end-to-end に閉じた。

次は:

```text
Phase 31
SmashProduct minimum representation
```

を推奨する。

対象:

```text
a ∧ b
```

候補 structural object:

```text
SmashProduct(
  left=a,
  right=b,
)
```

重要:

```text
SmashProduct(a,b)
!=
Barratt-Hilton theorem knowledge
```

Phase 31 では smash product の structural identity / equality / minimal typing needs を確認し、一般 algebra や Barratt-Hilton を先取りしない。

この representation が整って初めて、Toda Prop.2.2 の左側公式:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

を lossless に表現できる。

長期 dependency:

```text
Phase 30
right Prop.2.2 formula complete
↓
Phase 31
SmashProduct minimum representation
↓
left Prop.2.2 formula support
↓
IteratedSuspension / symbolic sign support
↓
Toda Prop.3.1 Barratt-Hilton
↓
actual H calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing equality reflection
↓
(2ι₂)η₂=4η₂
```

---

# 52. テスト原則

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

structural growth を生む rule は、fixed-point rule set に無条件で常駐させず、actual proof scenario に必要な active scope を明示する。

---

# 53. 文書運用方針

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

---

# 54. Phase 31 SmashProduct minimum representation

Phase 31 は Toda Prop.2.2 左側公式:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

に必要な `c∧c` を表現するため、最小 structural expression として `SmashProduct` を追加する。

structure:

```text
SmashProduct(Expression)
  left: Expression
  right: Expression
```

意味:

```text
SmashProduct(a,b)
=
a ∧ b の structural syntax
```

重要:

```text
SmashProduct(a,b)
!=
Barratt-Hilton theorem knowledge
```

```text
representation
!=
theorem knowledge
```

を維持する。

---

# 55. SmashProduct structural equality semantics

`SmashProduct` は frozen dataclass として Python structural equality を使用する。

したがって:

```text
SmashProduct(a,b)
==
SmashProduct(a,b)
```

一方:

```text
SmashProduct(a,b)
!=
SmashProduct(b,a)
```

```text
SmashProduct(a,b)
!=
SmashProduct(a,c)
```

である。

これは smash product の数学的非可換性を主張する theorem ではない。

意味は:

```text
different syntax tree
→
structurally distinct
```

である。

---

# 56. Expression-family distinction

同じ operands でも expression family は区別する。

```text
SmashProduct(a,b)
!=
Sum(a,b)
```

```text
SmashProduct(a,b)
!=
Composition(a,b)
```

将来 Barratt-Hilton により `a∧b` と composition expression の equality が得られる場合も、それは structural equality ではなく explicit theorem / proof-level equality として扱う。

---

# 57. Expression hierarchy connection

`SmashProduct` は `Expression` を継承するため、既存 expression containers の内部に lossless に保持できる。

確認済み:

```text
Suspension(SmashProduct(a,b))
MapApplication(f,SmashProduct(a,b))
Multiple(2,SmashProduct(a,b))
Sum(SmashProduct(a,b),c)
SmashProduct(SmashProduct(a,b),c)
```

この接続のための新しい inference rule や generic engine change は不要。

---

# 58. Representative c ∧ c construction

Toda Prop.2.2 左側で直接必要となる代表形:

```text
c ∧ c
```

は:

```text
SmashProduct(
  left=c,
  right=c,
)
```

として表現する。

同一 operand を受け取った場合も left / right をそのまま保持し、hidden copy / normalization は行わない。

---

# 59. E(c ∧ c) representation

既存 `Suspension` と組み合わせて:

```text
E(c ∧ c)
```

を:

```text
Suspension(
  expression=SmashProduct(
    left=c,
    right=c,
  ),
)
```

として lossless に表現できる。

代表 chain:

```text
c
↓
c ∧ c
↓
E(c ∧ c)
```

これにより Toda Prop.2.2 左側公式の右辺に必要な syntax は揃った。

---

# 60. Phase 31 typing boundary

Phase 31 では `SmashProduct` の typing semantics を追加しない。

`SmashProduct` 自体は:

```text
source property を持たない
target property を持たない
```

operands が typed でも:

```text
typed a + typed b
↛
typed SmashProduct(a,b)
```

既存 `Suspension` は `SmashProduct` から typing を導出しないため:

```text
Suspension(SmashProduct(c,c)).source = None
Suspension(SmashProduct(c,c)).target = None
```

となる。

重要:

```text
representable
!=
typed
```

---

# 61. Composition compatibility boundary

`Composition` は `SmashProduct` を operand とする syntax tree 自体は構築できる。

しかし current `Composition.is_type_compatible()` は `SmashProduct` を typed expression family として扱わない。

したがって:

```text
constructible
!=
type-compatible
```

である。

Phase 31 ではこの境界を regression で固定し、smash-product typing を先取りしない。

---

# 62. Phase 31 invalid / scope semantics

Phase 31 は異なる syntax の implicit identification を reject する。

例:

```text
SmashProduct(a,b) != SmashProduct(a,c)
SmashProduct(a,b) != SmashProduct(b,a)
E(a∧b) != E(a∧c)
E(a∧b) != E(b∧a)
E(a∧b) != a∧b
a∧b != a∘b
```

これらは mathematical inequality theorem ではなく structural distinction。

automatic normalization は行わない。

---

# 63. Phase 31 representative probe

実行:

```powershell
python -m probes.probe_phase31_capabilities
```

表示する代表 capability:

```text
c
↓
c ∧ c
↓
E(c ∧ c)
```

さらに:

```text
SmashProduct has source: False
SmashProduct has target: False
E(c ∧ c).source = None
E(c ∧ c).target = None
```

を表示して、

```text
representation != typing
representation != theorem knowledge
```

を人間が目で確認できる。

---

# 64. Phase 31 completion boundary

実装済み:

```text
SmashProduct(Expression)
structural equality
operand distinction
operand-order distinction
Sum / Composition distinction
Expression hierarchy connection
nested SmashProduct preservation
c ∧ c representative construction
E(c ∧ c) representation
typing boundary regression
composition-compatibility boundary
invalid / scope regression
final regression
human-readable capability probe
```

generic inference engine:

```text
変更なし
```

theorem / knowledge layers:

```text
変更なし
```

verified:

```text
tests/test_expression.py
145 passed in 0.58s
```

```text
full suite
1466 passed in 23.63s
```

---

# 65. Phase 31 non-goals

未実装:

```text
SmashProduct source / target typing
SmashProduct.is_type_compatible()
smash-product algebra
smash-product symmetry theorem
smash-product associativity theorem
smash-product normalization
H((Ec)∘a)=E(c∧c)∘H(a)
Toda Prop.3.1 Barratt-Hilton
symbolic (-1)^n algebra
actual H((2ι₂)η₂) calculation
```

---

# 66. 次の設計境界

Phase 31 により left Toda Prop.2.2 formula に必要な:

```text
c ∧ c
E(c ∧ c)
```

の syntax は揃った。

次は:

```text
Phase 32
Toda Prop.2.2 left suspended-composition formula support
```

を推奨する。

Target:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

Phase 32 では actual `H` representation と existing proof-level equality machinery を再利用し、Barratt-Hilton や general smash-product algebra は先取りしない。

