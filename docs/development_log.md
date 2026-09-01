# ehp_proof 開発記録

この文書は Phase 28 完了時点までの開発履歴を、現在の実装と矛盾しない形で整理した改訂版である。

```text
各 Phase の「未実装」「次の課題」
=
その Phase 時点の historical statement
```

current specification は README.md / docs/design.md を優先する。

---

# Phase 1–17 概要

Phase 1: finite abelian-group calculations.

Phase 2: structured subgroup calculations.

Phase 3: quotient / exact sequence / extension.

Phase 4: presentation-based finitely generated abelian groups.

Phase 5: generic proof / inference engine foundation.

Phase 6: EHP domain inference foundation.

Phase 7: element-order reasoning.

Phase 8: Suspension reasoning.

Phase 9: Freudenthal / stable-range reasoning.

Phase 10: composition reasoning.

Phase 11: generalized Hopf-invariant reasoning.

Phase 12: additive expression / reasoning.

Phase 13: homomorphism reasoning.

Phase 14: set / subgroup reasoning.

Phase 15: coset / modulo reasoning.

Phase 16: symbolic scalar constraints.

Phase 17: indeterminacy.

### 状態

完了

---

# Phase 18：Toda bracket minimum representation

追加:

```text
TodaBracket
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

### 状態

完了

---

# Phase 19：Toda bracket membership / first theorem bridge

追加:

```text
TodaBracketMembershipTheoremStatement
```

bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

### 状態

完了

---

# Phase 20：Indexed unstable Toda notation

追加:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
IndexedTodaBracketData.is_consistent()
```

### 状態

完了

---

# Phase 21：Typed homotopy elements / source-target context

追加:

```text
HomotopyElement.source
HomotopyElement.target
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

### 状態

完了

---

# Phase 22：Structured Generator Representation

追加:

```text
GeneratorSymbol
  family
  index
  decoration
```

重要:

```text
generator notation
↛
automatic source / target typing
```

### 状態

完了

---

# Phase 23：Indexed Toda theorem / validity connection

actual bridge:

```text
ε₃ theorem fact
+
exactly matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

### 状態

完了

---

# Phase 24：Theorem fact / knowledge-table integration

追加:

```text
TheoremFactEntry
TheoremFactRepository
EPSILON_3_TODA_MEMBERSHIP_FACT
THEOREM_FACT_REPOSITORY
```

### 状態

完了

---

# Phase 25：Generator typing / ambient-group facts

主な追加:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
materialize_typed_element()
```

代表:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

### 状態

完了

---

# Phase 26：actual Toda-generator typing expansion

production generator coverage:

```text
η₃
ν′
ν₇
```

typing:

```text
η₃ : S⁴ → S³
ν′ : S⁶ → S³
ν₇ : S¹⁰ → S⁷
```

Suspension:

```text
ν′
↓
Eν′ : S⁷ → S⁴
```

actual bracket:

```text
{η₃,Eν′,ν₇}_1
```

displayed adjacent compositions は type-compatible。

重要:

```text
type-compatible
!=
composition is zero
!=
Toda definedness
```

### 状態

完了

---

# Phase 27：corrected actual ε₃ Toda-definedness / end-to-end inference

目的:

actual indexed Toda definedness を explicit mathematical facts から導出し、existing theorem fact と接続する。

primitive knowledge:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

corrected rule:

```text
a ∘ Eb = 0
b ∘ c = 0
Ec = d
↓
{a,Eb,d}_1 is defined
```

actual result:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
```

さらに theorem fact と接続:

```text
Toda theorem fact
+
derived definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

single fixed-point run:

```text
Round 1
definedness

Round 2
membership
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

### 状態

完了

---

# Phase 28：map-property equality-reflection foundation

目的:

Toda 型の次の代表的な証明形式:

```text
写像した先で等しい
+
その写像が単射 / 同型
↓
元でも等しい
```

を proof graph 上で扱うための generic foundation を追加する。

Phase 28 では actual Hopf map `H` の数学的 fact はまだ追加せず、map-property reasoning そのものに限定した。

---

## Phase 28-1：InjectiveMapStatement の最小表現

追加:

```text
InjectiveMapStatement
```

構造:

```text
InjectiveMapStatement(
  map=f,
)
```

意味:

```text
f is injective
```

境界:

```text
MapSymbol(f)
↛
InjectiveMapStatement(f)
```

map notation 自体から injectivity を推測しない。

focused:

```text
4 passed
```

full suite:

```text
1336 passed
```

### 状態

完了

---

## Phase 28-2：IsomorphismStatement の最小表現

追加:

```text
IsomorphismStatement
```

構造:

```text
IsomorphismStatement(
  map=f,
)
```

重要:

```text
IsomorphismStatement(f)
!=
InjectiveMapStatement(f)
```

数学的 implication と structural equality を分離する。

full suite:

```text
1340 passed
```

### 状態

完了

---

## Phase 28-3：Isomorphism(f) → Injective(f)

追加:

```text
isomorphism_implies_injective_inference_rule()
```

rule:

```text
Isomorphism(f)
↓
Injective(f)
```

provenance:

```text
derived Injective(f)
premises =
  Isomorphism(f)
```

negative boundary:

```text
Isomorphism(f)
↛
Injective(g)
```

```text
Injective(f)
↛
Isomorphism(f)
```

focused:

```text
12 passed
```

full suite:

```text
1344 passed
```

### 状態

完了

---

## Phase 28-4：MapApplication を使った f(a)=f(b) の表現確認

production code の追加なし。

既存:

```text
MapApplication(
  map=f,
  expression=a,
)
```

を用いて:

```text
Relation(
  lhs=f(a),
  rhs=f(b),
  relation_type=EQUALITY,
)
```

を表現可能であることを確認。

重要:

```text
f(a)=f(b)
!=
f(a)=g(b)
```

focused:

```text
16 passed
```

full suite:

```text
1348 passed
```

### 状態

完了

---

## Phase 28-5：Injective(f) + f(a)=f(b) → a=b

追加:

```text
injective_map_reflects_equality_inference_rule()
```

rule:

```text
Injective(f)
+
f(a)=f(b)
↓
a=b
```

guard:

```text
lhs is MapApplication
rhs is MapApplication
lhs.map == rhs.map
injective.map == lhs.map
```

conclusion は mapped expression の `expression` をそのまま使う。

focused:

```text
17 passed
```

full suite:

```text
1349 passed
```

### 状態

完了

---

## Phase 28-6：provenance chain

production code の追加なし。

同一 fixed-point run:

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

provenance:

```text
a=b
premises =
  derived Injective(f)
  f(a)=f(b)
```

さらに:

```text
derived Injective(f)
premises =
  Isomorphism(f)
```

最終 `a=b` から2段階の chain を辿れる。

focused:

```text
19 passed
```

full suite:

```text
1351 passed
```

### 状態

完了

---

## Phase 28-7：invalid / mismatched map regression

production code の追加なし。

以下を reject:

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

focused:

```text
23 passed
```

full suite:

```text
1355 passed
```

### 状態

完了

---

## Phase 28-8：representative end-to-end example

新規:

```text
probes/probe_phase28_capabilities.py
```

実行:

```powershell
python -m probes.probe_phase28_capabilities
```

visible chain:

```text
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

表示:

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

重要:

```text
H
=
representative MapSymbol only
```

まだ actual Hopf map fact ではない。

full suite:

```text
1355 passed
```

### 状態

完了

---

## Phase 28-9：scope / fixed-point regression

production code の追加なし。

unrelated fact exclusion:

```text
unrelated fact
↛ Injective(f) provenance
```

```text
unrelated fact
↛ a=b provenance
```

deduplication:

```text
Injective(f)
→ exactly 1 derived step
```

```text
a=b
→ exactly 1 derived step
```

genuine fixed point:

```text
derive_inference_round_result(
  rules,
  result.steps,
)
```

で:

```text
new_steps == ()
```

を確認。

最終確認:

```text
tests/test_map_property_rules.py
26 passed in 1.42s
```

```text
full suite
1358 passed in 102.90s
```

### 状態

完了

---

## Phase 28-10：Phase 28 完了整理

Phase 28 completion chain:

```text
Isomorphism(f)
↓
Injective(f)

+

f(a)=f(b)

↓
a=b
```

single fixed-point run:

```text
Round 1
Injective(f)

Round 2
a=b

↓
genuine FIXED_POINT
```

実装済み:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism → injective inference
MapApplication equality representation
injective equality reflection
same-map validity guard
two-level provenance
invalid / mismatched map rejection
unrelated-fact exclusion
deduplication
genuine fixed-point regression
human-readable capability probe
```

generic inference engine:

```text
変更なし
```

representative probe:

```powershell
python -m probes.probe_phase28_capabilities
```

current verified status:

```text
tests/test_map_property_rules.py
26 passed in 1.42s
```

```text
full suite
1358 passed in 102.90s
```

No failures.

### 状態

完了

---

# Phase 28 completion boundary

Phase 28 で一般的な:

```text
f(a)=f(b)
+
f is injective / isomorphism
↓
a=b
```

の proof trace が可能になった。

ただし actual mathematical knowledge として:

```text
H is the required Hopf map
H has a required domain / codomain
H is an isomorphism in the required case
```

はまだ入っていない。

したがって Phase 28 の `H` probe は representative example であり、actual Toda calculation ではない。

---

# 次の Phase

次は:

```text
Phase 29
actual H map facts / typing
```

が自然。

候補:

```text
actual H identity
actual H source / target
actual H isomorphism property
必要最小限の explicit fact / provenance
existing Phase 28 equality reflection への接続
```

その後:

```text
Phase 30+
Hopf formula
smash product
actual H calculation
```

へ進み、

```text
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

という実例へ接続する。

---

# 文書運用方針

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

historical limitation と current limitation を混同しない。
