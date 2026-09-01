# ehp_proof 開発記録

この文書は Phase 27 完了時点までの開発履歴を、現在の実装と矛盾しない形で整理した改訂版である。

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

代表的な Phase 17 形式:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Phase 17 完了時:

```text
full suite
1024 passed in 66.01s
```

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

確認:

```text
full suite
1048 passed in 61.09s
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

確認:

```text
full suite
1064 passed in 61.64s
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

確認:

```text
full suite
1098 passed in 61.30s
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

確認:

```text
full suite
1125 passed in 22.75s
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

確認:

```text
full suite
1153 passed in 24.83s
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

確認:

```text
full suite
1175 passed in 22.96s
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

確認:

```text
tests/test_theorem_facts.py
15 passed
```

```text
full suite
1190 passed in 61.30s
```

### 状態

完了

---

# Phase 25：Generator typing / ambient-group facts

原則:

```text
GeneratorSymbol.index
↛
automatic typing
```

typing は explicit registered fact だけから供給する。

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

確認:

```text
tests/test_generator_facts.py
55 passed in 2.25s
```

```text
full suite
1245 passed in 65.71s
```

代表 probe:

```powershell
python -m probes.probe_phase25_capabilities
```

### 状態

完了

---

# Phase 26：actual Toda-generator typing expansion

目的:

```text
{η₃,Eν′,ν₇}_1
```

の3 entry を notation から推測するのではなく、explicit generator facts から typed にし、既存 Toda type-compatibility machinery に接続する。

---

## Phase 26-1：ν′ generator typing fact

追加:

```text
NU_PRIME_GENERATOR
NU_PRIME_TYPING_FACT
```

typing:

```text
ν′ : S⁶ → S³
```

### 状態

完了

---

## Phase 26-2：ν₇ generator typing fact

追加:

```text
NU_7_GENERATOR
NU_7_TYPING_FACT
```

typing:

```text
ν₇ : S¹⁰ → S⁷
```

### 状態

完了

---

## Phase 26-3：ν′ / ν₇ ambient-group fact

追加:

```text
NU_PRIME_AMBIENT_GROUP_FACT
NU_7_AMBIENT_GROUP_FACT
```

facts:

```text
ν′ ∈ π₆(S³)
ν₇ ∈ π₁₀(S⁷)
```

### 状態

完了

---

## Phase 26-4：production repository 登録

production repository coverage:

```text
η₃
ν′
ν₇
```

typing / ambient-group lookup と typed materialization が利用可能になった。

### 状態

完了

---

## Phase 26-5：Eν′ の explicit typing connection

production code の新規追加なし。

```text
ν′ : S⁶ → S³
↓
Suspension
↓
Eν′ : S⁷ → S⁴
```

### 状態

完了

---

## Phase 26-6：actual bracket entry typing

構築:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

```text
{η₃,Eν′,ν₇}_1
```

### 状態

完了

---

## Phase 26-7：type compatibility

確認:

```text
η₃ ∘ Eν′
Eν′ ∘ ν₇
```

は type-compatible。

境界:

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

## Phase 26-8：typing / ambient-group consistency

追加:

```text
GeneratorFactRepository.is_typing_ambient_group_consistent()
```

semantics:

```text
True
False
None
```

production:

```text
η₃ → True
ν′ → True
ν₇ → True
```

### 状態

完了

---

## Phase 26-9：provenance / regression / scope

固定:

```text
actual Toda typing chain
↛
generator repository mutation
```

```text
actual Toda typing chain
↛
theorem repository mutation
```

```text
ν₇ registered
↛
general ν_n automatic typing
```

### 状態

完了

---

## Phase 26-10：Phase 26 完了整理

代表 probe:

```powershell
python -m probes.probe_phase26_capabilities
```

最終確認:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

### 状態

完了

---

# Phase 27：corrected actual ε₃ Toda-definedness / end-to-end inference

目的:

Phase 26 で得た actual bracket typing / compatibility の先へ進み、actual indexed Toda definedness を explicit mathematical facts から導出し、existing theorem fact とつないで:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

まで corrected end-to-end proof trace を構築する。

Phase 27 では途中で indexed defining condition の解釈を correction し、表示上の adjacent composition をそのまま primitive condition とみなさない設計を確定した。

---

## Phase 27-1：`η₃ ∘ Eν′ = 0` explicit fact

追加:

```text
ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
```

内容:

```text
η₃ ∘ Eν′ = 0
```

`RelationType.ZERO` として保持。

この fact 自体には source / target typing を暗黙追加しない。

### 状態

完了

---

## Phase 27-2：corrected second primitive fact

追加:

```text
NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
```

内容:

```text
ν′ ∘ ν₆ = 0
```

さらに indexed bracket の third displayed entry へ接続する equality:

```text
E_NU_6_EQUALS_NU_7_FACT
```

内容:

```text
Eν₆ = ν₇
```

を使用する。

ここで重要な correction:

```text
Eν′ ∘ ν₇ = 0
```

を index-1 bracket の second primitive defining condition として扱わない。

### 状態

完了

---

## Phase 27-3：ZeroCompositionFactRepository

追加:

```text
ZeroCompositionFactRepository
ZERO_COMPOSITION_FACT_REPOSITORY
```

production repository の primitive facts:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
```

`Eν₆ = ν₇` は equality fact なのでこの repository には登録しない。

validation:

```text
lhs is Composition
rhs == Zero()
relation_type == ZERO
duplicate rejection
```

### 状態

完了

---

## Phase 27-4：typed actual composition と untyped fact の接続

追加:

```text
lookup_by_untyped_structure()
```

目的:

typed actual composition と、typing annotation を持たない production mathematical fact を必要最小限で接続する。

無視するもの:

```text
source
target
```

保持するもの:

```text
name
dimension
generator
Suspension structure
Composition structure
```

したがって general wildcard matching ではない。

regression:

```text
different generator → reject
missing Suspension → reject
wrong name → reject
```

### 状態

完了

---

## Phase 27-5：corrected indexed Toda definedness

追加:

```text
indexed_toda_bracket_index1_defined_inference_rule()
```

一般形:

```text
a ∘ Eb = 0
b ∘ c = 0
Ec = d
↓
{a,Eb,d}_1 is defined
```

actual inputs:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

から:

```text
{η₃,Eν′,ν₇}_1 is defined
```

を導出。

provenance:

```text
defined_step.premises
=
first_zero_step
second_zero_step
suspension_step
```

negative regression:

```text
η₃ ∘ Eν′ = 0
Eν′ ∘ ν₇ = 0
Eν₆ = ν₇
```

では actual indexed definedness を導出しない。

確認:

```text
tests/test_phase27_toda_definedness.py
4 passed
```

### 状態

完了

---

## Phase 27-6：actual theorem connection

Phase 27-5 で derived した actual definedness が:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
```

の bracket と一致することを確認。

theorem repository:

```text
THEOREM_FACT_REPOSITORY
```

から theorem step を materialize し、既存:

```text
toda_bracket_membership_from_theorem_inference_rule()
```

へ接続。

theorem fact 単独では membership を導出しないことも確認。

### 状態

完了

---

## Phase 27-7：corrected end-to-end inference

Phase 27-6 までは definedness derivation と membership bridge を段階的に確認していた。

Phase 27-7 では同一 fixed-point run に:

```text
indexed_toda_bracket_index1_defined_inference_rule()
toda_bracket_membership_from_theorem_inference_rule()
```

を投入。

initial knowledge:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
Toda theorem fact
```

結果:

```text
Round 1
{η₃,Eν′,ν₇}_1 is defined

Round 2
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

termination:

```text
FIXED_POINT
```

```text
round_count = 2
```

確認時:

```text
tests/test_phase27_theorem_connection.py
7 passed
```

```text
full suite
1328 passed in 88.44s
```

### 状態

完了

---

## Phase 27-8：corrected end-to-end capability probe

新規:

```text
probes/probe_phase27_capabilities.py
```

実行:

```powershell
python -m probes.probe_phase27_capabilities
```

visible chain:

```text
GIVEN
η₃ ∘ Eν′ = 0

GIVEN
ν′ ∘ ν₆ = 0

GIVEN
Eν₆ = ν₇

INFERENCE
{η₃,Eν′,ν₇}_1 is defined

GIVEN
Toda theorem:
ε₃ ∈ {η₃,Eν′,ν₇}_1

INFERENCE
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

表示:

```text
rounds = 2
termination = FIXED_POINT
```

さらに:

```text
Eν′ ∘ ν₇ = 0
```

を primitive defining knowledge として使っていないことを明示。

この probe は production APIs / facts / inference rules を使用し、数学的ロジックを別実装しない。

確認:

```text
full suite
1328 passed in 91.17s
```

### 状態

完了

---

## Phase 27-9：provenance / regression / scope boundary

新しい production code は追加しない。

回帰テストで以下を固定:

### unrelated fact exclusion

```text
unrelated fact
↛
definedness provenance
```

```text
unrelated fact
↛
membership provenance
```

### repository non-mutation

```text
inference run
↛
ZERO_COMPOSITION_FACT_REPOSITORY mutation
```

```text
inference run
↛
THEOREM_FACT_REPOSITORY mutation
```

### deduplication

```text
actual definedness
→ 1 step
```

```text
actual membership
→ 1 step
```

### genuine fixed point

terminal state から:

```text
derive_inference_round_result()
```

を再実行して:

```text
new_steps == ()
```

を確認。

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

## Phase 27-10：Phase 27 完了整理

Phase 27 completion chain:

```text
explicit primitive composition facts
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0

+
Suspension identification
Eν₆ = ν₇

↓
indexed_toda_bracket_index1_defined_inference_rule()

↓
{η₃,Eν′,ν₇}_1 is defined

+
THEOREM_FACT_REPOSITORY
Toda theorem fact

↓
toda_bracket_membership_from_theorem_inference_rule()

↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

2 round で genuine fixed point に到達する。

重要な corrected boundary:

```text
displayed Eν′ ∘ ν₇ = 0
!=
primitive second defining condition
```

Phase 27 では:

```text
ν′ ∘ ν₆ = 0
+
Eν₆ = ν₇
```

を使う。

代表 probe:

```powershell
python -m probes.probe_phase27_capabilities
```

最終 verified status:

```text
tests/test_phase27_theorem_connection.py
11 passed in 0.69s
```

```text
full suite
1332 passed in 86.87s
```

generic inference engine:

```text
変更なし
```

更新文書:

```text
README.md
docs/design.md
docs/development_log.md
docs/roadmap.md
```

### 状態

完了

---

# Phase 27 completion boundary

実装済み:

```text
explicit corrected zero-composition knowledge
zero-composition fact repository
typed/untyped narrow structure lookup
corrected index-1 Toda definedness
actual definedness ProofStep provenance
theorem fact connection
single-run end-to-end ε₃ membership
two-round fixed point
full provenance chain
unrelated fact exclusion
repository non-mutation
deduplication
genuine fixed-point regression
human-readable capability probe
```

重要な境界:

```text
type compatibility
↛
ZERO
```

```text
displayed adjacency
↛
indexed defining conditions
```

```text
lookup_by_untyped_structure
!=
general wildcard equality
```

```text
inference
↛
repository mutation
```

```text
generic inference engine
=
unchanged
```

current verified status:

```text
1332 passed in 86.87s
```

No failures.

### 状態

完了

---

# 次の候補

Phase 27 で actual ε₃ Toda proof chain は corrected end-to-end まで到達した。

次は、既に roadmap に記録している map-theoretic reasoning が有力。

候補:

```text
MapSymbol の domain / codomain typing
InjectiveMapStatement
IsomorphismStatement
SurjectiveMapStatement
equality reflection under injectivity
```

代表的な将来目標:

```text
H((2ι₂)η₂)=H(4η₂)
+
H isomorphism
↓
(2ι₂)η₂=4η₂
```

および:

```text
HP(ι₅)=H(±2η₂)
+
H isomorphism
↓
P(ι₅)=±2η₂
```

actual mathematical need から必要最小限の Phase を切る。

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
