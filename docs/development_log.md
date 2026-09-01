# ehp_proof 開発記録

この文書は Phase 29 完了時点までの開発履歴を、現在の実装と矛盾しない形で整理した改訂版である。

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
full suite
1332 passed in 86.87s
```

### 状態

完了

---

# Phase 28：map-property equality-reflection foundation

目的:

```text
写像した先で等しい
+
その写像が単射 / 同型
↓
元でも等しい
```

を proof graph 上で扱う generic foundation を追加する。

Phase 28 では actual Hopf map `H` の数学的 fact はまだ追加せず、map-property reasoning そのものに限定した。

## Phase 28-1：InjectiveMapStatement

追加:

```text
InjectiveMapStatement
```

### 状態

完了

## Phase 28-2：IsomorphismStatement

追加:

```text
IsomorphismStatement
```

重要:

```text
IsomorphismStatement(f)
!=
InjectiveMapStatement(f)
```

### 状態

完了

## Phase 28-3：Isomorphism(f) → Injective(f)

追加:

```text
isomorphism_implies_injective_inference_rule()
```

### 状態

完了

## Phase 28-4：MapApplication equality representation

既存 `MapApplication` と `RelationType.EQUALITY` で:

```text
f(a)=f(b)
```

を表現可能であることを確認。

### 状態

完了

## Phase 28-5：Injective(f) + f(a)=f(b) → a=b

追加:

```text
injective_map_reflects_equality_inference_rule()
```

### 状態

完了

## Phase 28-6：provenance chain

```text
GIVEN Isomorphism(f)
GIVEN f(a)=f(b)
↓
Round 1 Injective(f)
↓
Round 2 a=b
```

### 状態

完了

## Phase 28-7：invalid / mismatched map regression

reject:

```text
Injective(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + f(a)=g(b)
↛ a=b
```

### 状態

完了

## Phase 28-8：representative end-to-end example

新規:

```text
probes/probe_phase28_capabilities.py
```

important boundary:

```text
H = representative MapSymbol only
```

### 状態

完了

## Phase 28-9：scope / fixed-point regression

確認:

```text
unrelated fact exclusion
deduplication
genuine fixed point
```

最終確認:

```text
full suite
1358 passed in 102.90s
```

### 状態

完了

## Phase 28-10：Phase 28 完了整理

completion chain:

```text
Isomorphism(f)
↓
Injective(f)
+
f(a)=f(b)
↓
a=b
```

### 状態

完了

---

# Phase 29：actual H map facts / typing

目的:

Phase 28 の representative:

```text
GIVEN
H is an isomorphism
```

を actual production mathematical knowledge に置き換え、既存 generic map-property reasoning へ接続する。

Phase 29 ではまだ actual Hopf formula calculation は実装しない。

---

## Phase 29-1：actual H map identity

新規:

```text
map_facts.py
```

production identity:

```text
HOPF_MAP = MapSymbol(name="H")
```

確認:

```text
MapSymbol identity only
```

まだ typing / property を暗黙に持たない。

focused:

```text
4 passed
```

full suite:

```text
1362 passed
```

### 状態

完了

---

## Phase 29-2：H domain / codomain typing の最小表現

追加:

```text
MapTypingFact
```

fields:

```text
map
source_group_dimension
source_sphere_dimension
target_group_dimension
target_sphere_dimension
```

これにより:

```text
H : π₃(S²) → π₃(S³)
```

のような homotopy-group 間 map typing を表現可能にした。

重要:

```text
MapSymbol
!=
MapTypingFact
```

focused:

```text
14 passed
```

full suite:

```text
1372 passed
```

### 状態

完了

---

## Phase 29-3：actual H typing fact

追加 production fact:

```text
HOPF_MAP_TYPING_FACT
```

meaning:

```text
H : π₃(S²) → π₃(S³)
```

boundary:

```text
HOPF_MAP_TYPING_FACT
↛
IsomorphismStatement(H)
```

focused:

```text
20 passed
```

full suite:

```text
1378 passed
```

### 状態

完了

---

## Phase 29-4：H isomorphism property fact の最小表現

追加:

```text
MapIsomorphismFact
```

structure:

```text
MapIsomorphismFact(
  typing=MapTypingFact(...)
)
```

意味:

```text
この map はこの typing context で isomorphism
```

重要:

```text
MapIsomorphismFact
!=
IsomorphismStatement
```

focused:

```text
26 passed
```

full suite:

```text
1384 passed
```

### 状態

完了

---

## Phase 29-5：production fact / lookup

追加:

```text
MapIsomorphismFactRepository
HOPF_MAP_ISOMORPHISM_FACT
MAP_ISOMORPHISM_FACT_REPOSITORY
```

actual fact:

```text
H : π₃(S²) → π₃(S³)
is an isomorphism
```

lookup:

```text
MAP_ISOMORPHISM_FACT_REPOSITORY.lookup(
  HOPF_MAP_TYPING_FACT
)
↓
HOPF_MAP_ISOMORPHISM_FACT
```

unknown typing context:

```text
→ None
```

duplicate typing-context fact:

```text
→ ValueError
```

focused:

```text
35 passed
```

full suite:

```text
1393 passed
```

### 状態

完了

---

## Phase 29-6：actual H fact → IsomorphismStatement(H)

追加:

```text
MapIsomorphismFact.to_proof_step()
```

materialization:

```text
HOPF_MAP_ISOMORPHISM_FACT
↓
to_proof_step()
↓
ProofStep.GIVEN
↓
IsomorphismStatement(HOPF_MAP)
```

materialization は inference ではない。

```text
rule = ProofRule.GIVEN
premises = ()
inference_rule = None
```

focused:

```text
41 passed
```

full suite:

```text
1399 passed
```

### 状態

完了

---

## Phase 29-7：Isomorphism(H) → Injective(H) actual connection

production code 変更なし。

existing Phase 28 rule と接続:

```text
repository lookup
↓
actual H fact
↓
to_proof_step()
↓
GIVEN Isomorphism(H)
↓
isomorphism_implies_injective_inference_rule()
↓
Injective(H)
```

provenance:

```text
Injective(H).premises =
  actual fact-derived Isomorphism(H) step
```

focused:

```text
43 passed
```

full suite:

```text
1401 passed
```

### 状態

完了

---

## Phase 29-8：representative actual-H end-to-end example

production code 変更なし。

新規 probe:

```text
probes/probe_phase29_capabilities.py
```

single fixed-point chain:

```text
PRODUCTION FACT
H : π₃(S²) → π₃(S³) is an isomorphism

↓ materialize

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

probe result:

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

Important boundary:

```text
H(a)=H(b)
```

は representative GIVEN。

まだ:

```text
H((2ι₂)η₂)=H(4η₂)
```

を actual calculation から導出していない。

full suite:

```text
1402 passed
```

### 状態

完了

---

## Phase 29-9：provenance / invalid / scope regression

production code 変更なし。

追加 regression:

```text
full provenance chain
different map rejection
unknown typing context rejection
unrelated fact exclusion
derived conclusion uniqueness
genuine fixed point
```

full provenance:

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

different map:

```text
Injective(H) + g(a)=g(b)
↛ a=b
```

unknown typing:

```text
unregistered H typing context
↛ actual isomorphism fact
```

unrelated fact:

```text
unrelated fact
↛ provenance
```

deduplication:

```text
Injective(H)
→ exactly 1 derived step
```

```text
a=b
→ exactly 1 derived step
```

genuine fixed point:

```text
terminal derive_inference_round_result()
→ new_steps == ()
```

final full suite:

```text
1408 passed in 96.81s
```

### 状態

完了

---

## Phase 29-10：Phase 29 完了整理

Phase 29 completion chain:

```text
HOPF_MAP
↓
actual map identity

HOPF_MAP_TYPING_FACT
↓
H : π₃(S²) → π₃(S³)

HOPF_MAP_ISOMORPHISM_FACT
↓
H : π₃(S²) → π₃(S³) is an isomorphism

MAP_ISOMORPHISM_FACT_REPOSITORY
↓ lookup

MapIsomorphismFact.to_proof_step()
↓
GIVEN Isomorphism(H)

↓ existing Phase 28 inference

Injective(H)

+

GIVEN H(a)=H(b)

↓ existing Phase 28 equality reflection

a=b
```

実装済み:

```text
actual H identity
map typing representation
actual H typing fact
typed-context isomorphism fact representation
actual H isomorphism production fact
map isomorphism fact repository
exact typing-context lookup
duplicate rejection
fact → ProofStep.GIVEN materialization
actual H IsomorphismStatement
actual H injectivity derivation
actual-H equality-reflection end-to-end probe
full proof-level provenance
different-map rejection
unknown-typing-context rejection
unrelated-fact exclusion
deduplication
genuine fixed-point regression
```

generic inference engine:

```text
変更なし
```

current verified status:

```text
full suite
1408 passed in 96.81s
```

No failures.

### 状態

完了

---

# Phase 29 completion boundary

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

まで production knowledge から end-to-end に接続した。

ただし actual mapped equality:

```text
H((2ι₂)η₂)=H(4η₂)
```

はまだ未実装。

したがって actual target:

```text
(2ι₂)η₂=4η₂
```

はまだ証明していない。

---

# 次の Phase

次は:

```text
Phase 30
Hopf formula minimum representation
```

を推奨する。

代表的な数学的対象:

```text
H(γ α)=(γ∧γ)H(α)
```

Phase 30 では formula の最小表現から開始し、smash product の一般機構や actual `(2ι₂)η₂` calculation を先取りしない。

その後:

```text
Phase 31
smash product

↓
Phase 32+
actual H calculation

↓
H((2ι₂)η₂)=H(4η₂)

↓
Phase 28/29 equality reflection

↓
(2ι₂)η₂=4η₂
```

へ進む。

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
