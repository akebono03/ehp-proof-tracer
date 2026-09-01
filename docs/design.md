# ehp_proof 設計メモ

この文書は Phase 27 完了時点の current architecture / semantics / design boundary を正本としてまとめる。

過去の `development_log.md` にある「未実装」「今後の課題」は、その Phase 時点の historical statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
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
実際の数学的必要
↓
必要最小限の表現
↓
explicit fact / domain rule
↓
既存機構
```

Phase 24 の theorem repository、Phase 25 / 26 の generator repository、Phase 27 の composition fact repository は、既知 knowledge の供給を担当する。

generic inference engine に個別の generator / Toda theorem / composition fact を埋め込まない。

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
- literature provenance materialization
- generator notation からの automatic typing
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

したがって、Phase 27 の `lookup_by_untyped_structure()` は Python equality を変更しない。

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

Phase 27 でも generic engine は変更しない。

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

repository 自体は inference run を起動しない。

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

Phase 27 でもこの境界は維持する。

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

production identities:

```text
ETA_3_GENERATOR
NU_PRIME_GENERATOR
NU_7_GENERATOR
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

したがって type-compatible である。

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

production constants:

```text
ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
```

さらに Suspension identification:

```text
Eν₆ = ν₇
```

production constant:

```text
E_NU_6_EQUALS_NU_7_FACT
```

重要:

```text
E_NU_6_EQUALS_NU_7_FACT
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

現在の production facts:

```text
ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
```

constructor は以下を検査する:

```text
lhs is Composition
rhs == Zero()
relation_type == RelationType.ZERO
duplicate composition がない
```

不正 fact は:

```text
ValueError("invalid zero-composition fact")
```

重複は:

```text
ValueError("duplicate zero-composition fact")
```

---

# 14. Exact lookup と typed/untyped structure lookup

exact lookup:

```text
lookup(composition)
```

は通常の structural equality を使う。

そのため:

```text
stored untyped composition
!=
typed composition
```

であり、exact lookup は typed expression を暗黙に一致させない。

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

したがって:

```text
typing annotation の差
→ match 可能
```

だが:

```text
別 generator
missing Suspension
wrong name
wrong dimension
→ match 不可
```

これは general wildcard equality ではない。

---

# 15. Corrected indexed Toda definedness semantics

Phase 27 の重要な correction:

表示上の bracket が

```text
{η₃,Eν′,ν₇}_1
```

であっても、index 1 の defining condition を単純な displayed-adjacent pair:

```text
η₃ ∘ Eν′ = 0
Eν′ ∘ ν₇ = 0
```

として扱わない。

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

この rule は index `1` 専用であり、general indexed Toda definedness system ではない。

---

# 16. Corrected definedness rule の guard

3 premises:

```text
first RelationType.ZERO
second RelationType.ZERO
third RelationType.EQUALITY
```

guard は少なくとも次を要求する:

```text
first lhs is Composition
second lhs is Composition
first.right is Suspension
first.right.expression == second.left
third.lhs is Suspension
third.lhs.expression == second.right
```

conclusion:

```text
TodaBracketDefinedStatement(
  bracket=TodaBracket(
    first=first.left,
    second=first.right,
    third=third.rhs,
    index=1,
  ),
)
```

actual inputs では:

```text
first  = η₃ ∘ Eν′ = 0
second = ν′ ∘ ν₆ = 0
third  = Eν₆ = ν₇
```

から:

```text
{η₃,Eν′,ν₇}_1 is defined
```

を導出する。

---

# 17. Displayed adjacent zero の境界

次の relation:

```text
Eν′ ∘ ν₇ = 0
```

を作ること自体は expression model 上可能である。

しかし Phase 27 の corrected indexed definedness rule の second primitive premise の代わりにはならない。

したがって:

```text
η₃ ∘ Eν′ = 0
Eν′ ∘ ν₇ = 0
Eν₆ = ν₇
```

から actual index-1 definedness は導出しない。

これは Phase 27 の最重要 regression boundary の一つである。

---

# 18. Toda theorem connection

既存 rule:

```text
toda_bracket_membership_from_theorem_inference_rule()
```

は:

```text
matching TodaBracketMembershipTheoremStatement
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

を表す。

Phase 27 では definedness を GIVEN で仮置きせず、corrected primitive inputs から実際に derived `ProofStep` として作れるようになった。

---

# 19. Corrected end-to-end inference

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

termination:

```text
InferenceTerminationReason.FIXED_POINT
```

```text
round_count == 2
```

---

# 20. ProofStep provenance

definedness step:

```text
rule = ProofRule.INFERENCE
inference_rule = indexed_toda_bracket_index1_defined_inference_rule()
premises =
  first_zero_step
  second_zero_step
  suspension_step
```

membership step:

```text
rule = ProofRule.INFERENCE
inference_rule = toda_bracket_membership_from_theorem_inference_rule()
premises =
  theorem_step
  definedness_step
```

theorem step:

```text
rule = ProofRule.GIVEN
source = LiteratureReference(label="Toda", ...)
```

したがって final membership から corrected primitive conditions まで provenance を辿れる。

---

# 21. Unrelated fact の排除

inference run に unrelated fact が含まれていても:

```text
unrelated fact
↛
definedness premises
```

```text
unrelated fact
↛
membership premises
```

を保証する。

provenance は applicability に実際に必要だった premise のみを保持する。

---

# 22. Repository non-mutation

Phase 27 inference の前後で:

```text
ZERO_COMPOSITION_FACT_REPOSITORY.facts
```

および:

```text
THEOREM_FACT_REPOSITORY.entries
```

は不変。

したがって:

```text
inference run
↛
knowledge repository mutation
```

knowledge supply と proof derivation の責務を分離する。

---

# 23. Deduplication / genuine fixed point

actual chain では:

```text
actual definedness step
→ 1個
```

```text
actual membership step
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

したがって単に round limit で停止したのではなく、genuine fixed point に達している。

---

# 24. Phase 27 representative probe

実行:

```powershell
python -m probes.probe_phase27_capabilities
```

表示する chain:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
+
Toda theorem
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

さらに:

```text
Eν′ ∘ ν₇ = 0
```

を primitive defining knowledge として使っていないことを明示する。

probe は production APIs / repositories / rules / generic engine を再利用し、数学を別実装しない。

---

# 25. Phase 27 completion boundary

実装済み:

```text
η₃ ∘ Eν′ = 0 explicit fact
ν′ ∘ ν₆ = 0 explicit fact
Eν₆ = ν₇ explicit equality fact
ZeroCompositionFactRepository
production zero-composition registration
exact lookup
typed/untyped narrow structure lookup
index-1 corrected Toda definedness rule
actual corrected definedness derivation
three-premise ProofStep provenance
theorem repository connection
single-run end-to-end membership
two-round fixed point
membership full provenance
unrelated-fact exclusion
repository non-mutation
deduplication
genuine fixed-point regression
human-readable Phase 27 probe
```

generic inference engine:

```text
変更なし
```

最終確認:

```text
tests/test_phase27_theorem_connection.py
11 passed in 0.69s
```

```text
full suite
1332 passed in 86.87s
```

---

# 26. Phase 27 non-goals

未実装:

- arbitrary index の general indexed Toda definedness
- displayed entries から defining conditions を自動生成する一般則
- type compatibility から ZERO fact を生成する規則
- composition fact の literature provenance
- composition fact の `ProofStep.GIVEN` repository materialization API
- generator fact の `LiteratureReference`
- generator fact の `ProofStep`
- general theorem quantification / instantiation
- generator name / dimension validation
- arbitrary recursive expression typing
- stable homotopy group model
- stable Toda bracket
- higher Toda bracket

---

# 27. Current knowledge-layer separation

現在の主要 knowledge repositories:

```text
THEOREM_FACT_REPOSITORY
GENERATOR_FACT_REPOSITORY
ZERO_COMPOSITION_FACT_REPOSITORY
```

それぞれの役割:

```text
THEOREM_FACT_REPOSITORY
=
literature-backed theorem statements
```

```text
GENERATOR_FACT_REPOSITORY
=
generator typing / ambient-group facts
```

```text
ZERO_COMPOSITION_FACT_REPOSITORY
=
primitive zero-composition facts
```

必要性が生じるまで一つの general repository に統合しない。

---

# 28. 次の設計境界

Phase 27 で actual ε₃ Toda proof chain は corrected end-to-end まで到達した。

次の有力候補は map-theoretic reasoning。

候補:

```text
typed MapSymbol domain / codomain
InjectiveMapStatement
IsomorphismStatement
SurjectiveMapStatement
```

重要な bridge:

```text
Isomorphism(f)
↓
Injective(f)
```

```text
Injective(f)
f(a)=f(b)
↓
a=b
```

これは将来:

```text
H((2ι₂)η₂) = H(4η₂)
+
H isomorphism
↓
(2ι₂)η₂ = 4η₂
```

のような Toda 型計算を trace するために重要となる。

---

# 29. テスト原則

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

# 30. 文書運用方針

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
