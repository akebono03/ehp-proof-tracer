# ehp_proof 設計メモ

この文書は Phase 28 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

過去の `development_log.md` にある「未実装」「今後の課題」は、その Phase 時点の historical statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map-property statements / future map facts
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

Phase 24 の theorem repository、Phase 25 / 26 の generator repository、Phase 27 の composition fact repository、Phase 28 の map-property statement / rule は、それぞれ責務を分離する。

generic inference engine に個別の generator / Toda theorem / composition fact / map property fact を埋め込まない。

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
- map property theorem applicability
- literature provenance materialization
- generator notation からの automatic typing
- map notation からの injectivity / isomorphism 推測
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

Phase 28 では map property についても同じ原則を採用する。

```text
IsomorphismStatement(f)
!=
InjectiveMapStatement(f)
```

数学的 implication は structural equality ではなく explicit inference rule で表す。

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

Phase 28 でも generic engine は変更しない。

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

Phase 28 の map-property layer の責務:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism → injective
injective-map equality reflection
same-map applicability guard
```

Phase 28 では map-property repository はまだ追加しない。

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
TodaBracket(
  first=typed η₃,
  second=Suspension(typed ν′),
  third=typed ν₇,
  index=1,
)
```

表示上:

```text
{η₃,Eν′,ν₇}_1
```

displayed adjacent compositions の type compatibility:

```text
η₃.source == Eν′.target == 4
Eν′.source == ν₇.target == 7
```

ただし:

```text
type-compatible
↛
zero composition
```

---

# 12. Phase 27 composition knowledge

Phase 27 では actual ε₃ indexed Toda bracket の definedness に必要な explicit composition knowledge を追加した。

primitive zero-composition facts:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
```

さらに Suspension identification:

```text
Eν₆ = ν₇
```

重要:

```text
Eν₆ = ν₇
```

は `RelationType.EQUALITY` であり、zero-composition repository には入れない。

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

constructor は少なくとも以下を検査する:

```text
lhs is Composition
rhs == Zero()
relation_type == RelationType.ZERO
duplicate composition がない
```

---

# 14. Exact lookup と typed/untyped structure lookup

exact lookup:

```text
lookup(composition)
```

は通常の structural equality を使う。

Phase 27 の actual bridge のために:

```text
lookup_by_untyped_structure(composition)
```

を追加した。

この API が無視するのは:

```text
HomotopyElement.source
HomotopyElement.target
```

だけである。

無視しないもの:

```text
name
dimension
generator
Suspension structure
Composition left/right structure
```

これは general wildcard equality ではない。

---

# 15. Corrected indexed Toda definedness semantics

Phase 27 の重要な correction:

表示上の bracket が

```text
{η₃,Eν′,ν₇}_1
```

であっても、index 1 の defining condition を単純な displayed-adjacent pair として扱わない。

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

rules:

```text
indexed_toda_bracket_index1_defined_inference_rule()
toda_bracket_membership_from_theorem_inference_rule()
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

Phase 28 では map-theoretic equality reflection の最小基盤を追加した。

追加 statement:

```text
InjectiveMapStatement
IsomorphismStatement
```

最小構造:

```text
InjectiveMapStatement(
  map: MapSymbol
)
```

```text
IsomorphismStatement(
  map: MapSymbol
)
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

数学的には:

```text
Isomorphism(f)
⇒
Injective(f)
```

だが、この implication は structural equality ではなく inference rule で表す。

---

# 19. Isomorphism → Injective inference

Phase 28-3 で追加:

```text
isomorphism_implies_injective_inference_rule()
```

semantics:

```text
Isomorphism(f)
↓
Injective(f)
```

conclusion は premise 内の同じ `MapSymbol` を保持する。

```text
Isomorphism(f)
↛
Injective(g)
```

reverse implication:

```text
Injective(f)
↛
Isomorphism(f)
```

は追加しない。

---

# 20. MapApplication equality representation

既存 `MapApplication`:

```text
MapApplication(
  map=f,
  expression=a,
)
```

は `f(a)` を表す。

したがって:

```text
f(a)=f(b)
```

は既存 `Relation` で:

```text
Relation(
  lhs=MapApplication(
    map=f,
    expression=a,
  ),
  rhs=MapApplication(
    map=f,
    expression=b,
  ),
  relation_type=RelationType.EQUALITY,
)
```

と表現できる。

専用の:

```text
MapEqualityStatement
ImageEqualityStatement
```

は追加しない。

---

# 21. Injective map equality reflection

Phase 28-5 で追加:

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

guard は少なくとも:

```text
equality lhs is MapApplication
equality rhs is MapApplication
lhs.map == rhs.map
injective_statement.map == lhs.map
```

を要求する。

conclusion:

```text
Relation(
  lhs=lhs.expression,
  rhs=rhs.expression,
  relation_type=RelationType.EQUALITY,
)
```

つまり mapped expression 自体を lossless に取り出し、名前解析などで復元しない。

---

# 22. Equality reflection の invalid boundary

以下では rule を適用しない。

```text
Injective(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + f(a)=g(b)
↛ a=b
```

```text
Isomorphism(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + plain a=b
↛ equality-reflection rule
```

必要条件は:

```text
same map on both MapApplications
+
injectivity of that same map
```

である。

---

# 23. Phase 28 end-to-end fixed-point inference

initial knowledge:

```text
GIVEN
Isomorphism(f)

GIVEN
f(a)=f(b)
```

rules:

```text
isomorphism_implies_injective_inference_rule()
injective_map_reflects_equality_inference_rule()
```

結果:

```text
Round 1
Injective(f)

Round 2
a=b
```

termination:

```text
InferenceTerminationReason.FIXED_POINT
```

```text
round_count == 2
```

---

# 24. Phase 28 provenance

derived injectivity step:

```text
rule = ProofRule.INFERENCE
inference_rule = isomorphism_implies_injective_inference_rule()
premises =
  isomorphism_step
```

derived equality step:

```text
rule = ProofRule.INFERENCE
inference_rule = injective_map_reflects_equality_inference_rule()
premises =
  derived injective_step
  mapped_equality_step
```

したがって final `a=b` から:

```text
a=b
↓
Injective(f)
↓
Isomorphism(f)
```

および:

```text
a=b
↓
f(a)=f(b)
```

まで辿れる。

---

# 25. Unrelated fact exclusion

inference run に unrelated fact が含まれていても:

```text
unrelated fact
↛ Injective(f) premises
```

```text
unrelated fact
↛ a=b premises
```

を保証する。

provenance は applicability に実際に必要だった premise のみ保持する。

---

# 26. Deduplication / genuine fixed point

Phase 28 end-to-end chain では:

```text
Injective(f)
→ 1個
```

```text
a=b
→ 1個
```

に deduplicate される。

完了後の knowledge に対し:

```text
derive_inference_round_result(
  rules,
  result.steps,
)
```

を再実行すると:

```text
new_steps == ()
```

したがって genuine fixed point に達している。

---

# 27. Phase 28 representative probe

実行:

```powershell
python -m probes.probe_phase28_capabilities
```

表示する chain:

```text
GIVEN
H is an isomorphism

INFERENCE
H is injective

GIVEN
H(a)=H(b)

INFERENCE
a=b
```

表示:

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

重要:

```text
H
=
Phase 28 では representative MapSymbol
```

actual Hopf map property fact ではない。

probe は production APIs / rules / generic engine を再利用し、数学を別実装しない。

---

# 28. Phase 28 completion boundary

実装済み:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism → injective inference
MapApplication equality representation
injective equality reflection
same-map guard
two-round end-to-end inference
full ProofStep provenance
mismatched-map rejection
plain-equality rejection
unrelated-fact exclusion
deduplication
genuine fixed-point regression
human-readable capability probe
```

generic inference engine:

```text
変更なし
```

最終確認:

```text
tests/test_map_property_rules.py
26 passed in 1.42s
```

```text
full suite
1358 passed in 102.90s
```

---

# 29. Phase 28 non-goals

未実装:

- typed `MapSymbol` domain / codomain
- actual Hopf map `H` identity facts
- actual `H` isomorphism facts
- map-property fact repository
- map-property literature provenance
- `SurjectiveMapStatement`
- preimage representation
- kernel-modulo equality shortcut
- Hopf invariant formula
- smash product
- actual `(2ι₂)η₂=4η₂` calculation

---

# 30. 次の設計境界

Phase 28 で generic map-property equality reflection は完成した。

次の Phase 29 は:

```text
actual H map facts / typing
```

を推奨する。

目的は Phase 28 の representative:

```text
H is an isomorphism
H(a)=H(b)
↓
a=b
```

のうち、`H is an isomorphism` を仮の GIVEN ではなく actual mathematical knowledge に置き換えることである。

候補:

```text
actual H map identity
actual H source / target context
actual H isomorphism property
必要なら explicit fact / repository / provenance
```

Phase 29 ではまだ:

```text
H((2ι₂)η₂)=4ι₃
```

の計算全体を先取りしない。

長期 dependency:

```text
Phase 28
generic injectivity / isomorphism / equality reflection
↓
Phase 29
actual H map facts / typing
↓
Phase 30+
Hopf formula / smash product / actual calculation
↓
(2ι₂)η₂=4η₂
```

---

# 31. テスト原則

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

# 32. 文書運用方針

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
