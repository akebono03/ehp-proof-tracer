# EHP Proof Tracer コードリファレンス

この文書は EHP Proof Tracer の主要 Python module と、その責務・主要 class / function・探索方法をまとめる。

対象は **Phase 67 completion 時点**。

この文書は全 API を機械的に列挙する reference ではない。目的は:

```text
新しい Phase の必要数学
↓
どの module を確認すべきか
↓
既存 class / rule の再利用候補
↓
最小変更
```

を速く判断できるようにすることである。

実際の実装前には必ず current code と関連 test を確認する。

---

# 1. module 境界の概要

```text
expression.py
  数学式の structural representation

proof.py
  generic proof / inference engine

relation_rules.py
  generic equality / zero / composition propagation

scalar_rules.py
  scalar parity / congruence / inequality 等

homotopy_groups.py
  homotopy-group / Toda-specific group and map data

map_facts.py
  canonical E / H / Δ map symbols

map_property_rules.py
  injective / surjective / isomorphism 等の map property

barratt_hilton_rules.py
  Barratt–Hilton / Toda Prop.3.1 周辺

toda_rules.py
  Toda-specific theorem statements / inference rules

probes/
  representative end-to-end capability demonstrations

tests/
  generic regression と Phase-specific tests
```

設計原則:

```text
generic mechanics
!=
theorem knowledge
```

---

# 2. expression.py

## 役割

数学的な式を syntax tree として保持する。

ここでは theorem を適用しない。

```text
representation
!=
theorem knowledge
```

## 主な scalar structure

```text
ScalarExpression
ScalarSymbol
ScalarSum
ScalarProduct
ScalarPower
ScalarValue
```

用途:

```text
i
i+1
i-1
2n-1
n-3
(-1)^k
```

などの symbolic index / coefficient。

## 主な expression

### `HomotopyElement`

ホモトピー類を表す。

代表 field:

```text
name
dimension
source
target
generator
```

例:

```text
η₂
η₃
η₄
η₅
ν′
ι₅
α
β
```

### `GeneratorSymbol`

生成元 family、index、decoration を保持する。

Phase 58 の `ν′` は:

```text
family="ν"
decoration="′"
```

を保持する。

### `Multiple`

```text
2α
-α
rι_n
```

を structural に表現する。

### `Sum`

加法 expression。

### `Composition`

```text
α∘β
```

を表す。

`is_type_compatible()` は保持している source / target から structural compatibility を確認する。

ただし general symbolic dimension solver ではない。

### `Suspension`

```text
Eα
```

### `IteratedSuspension`

```text
E^k α
```

### `MapApplication`

```text
H(α)
Δ(α)
```

のような map application。

### `SmashProduct`

Barratt–Hilton で必要な:

```text
α∧β
```

### `WhiteheadProduct`

```text
[α,β]
```

### `TodaBracket`

```text
{α,β,γ}_n
```

の structural representation。

indexed bracket も `index` で保持する。

Phase 58 の representative input:

```text
{η₃,2ι₄,η₄}_1
```

も既存 `TodaBracket` で表現する。

## ここに追加すべきもの

```text
新しい「式の形」
```

が必要な場合。

## Literature metadata

### `LiteratureReference`

文献の所在を構造化する。

代表 field:

```text
label
author
title
year
locator
```

### `LiteratureStatement`

Phase 60-9 で追加。

```text
reference: LiteratureReference
statement: str
```

責務:

```text
LiteratureReference
= どの文献のどこか

LiteratureStatement
= そこで利用する数学 statement
```

これは metadata object であり、statement text を generic inference engine が自動適用することはない。

Phase 60 representative probe の `Used in:` は `LiteratureStatement` の field ではなく probe-local display metadata。

## ここに追加しないもの

```text
Toda theorem applicability
mathematical equality theorem
proof provenance
generic proof search
```

---

# 3. proof.py

## 役割

数学 theorem の内容を知らない generic proof / inference engine。

## 主な class

### `RelationType`

```text
EQUALITY
ZERO
ORDER
INEQUALITY
```

### `Relation`

```text
lhs
rhs
relation_type
source
note
```

### `ProofRule`

代表:

```text
GIVEN
RELATION
INFERENCE
EXACTNESS
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

### `ProofStep`

```text
conclusion
premises
rule
note
inference_rule
```

provenance の中心。

### `PremisePattern`

rule applicability の premise specification。

### `PatternVariable`

generic structural matching 用 variable。

### `InferenceRule`

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

### `InferenceMatch`

matching された rule と premise を保持。

### `InferenceRunResult`

fixed-point run の結果。

## 主な function

```text
find_inference_match()
find_inference_matches()
apply_inference_match()
derive_inference_round_result()
run_inference_until_stable_with_history()
```

Phase 58 では fixed-point-safe stage と one-shot stage を分ける。

```text
fixed-point-safe rule family
→ run_inference_until_stable_with_history()

repeatable composition propagation
→ find_inference_match()
→ apply_inference_match()
```

## ここに追加しないもの

```text
Toda Lemma 5.2
Toda (5.3)
η-family normalization
concrete homotopy-group fact
```

---

# 4. relation_rules.py

## 役割

domain-independent な relation propagation。

## 主な rule family

```text
additive_inverse_inference_rule()
sum_commutativity_inference_rule()
sum_associativity_inference_rule()
double_equals_repeated_sum_inference_rule()
order_implies_zero_multiple_inference_rule()
zero_equality_implies_zero_inference_rule()
composition_equality_to_zero_inference_rule()
zero_composition_equality_implies_zero_inference_rule()
zero_composition_reverse_equality_implies_zero_inference_rule()
iterated_suspension_one_bridge_inference_rule()
suspension_preserves_equality_inference_rule()
suspension_composition_functoriality_inference_rule()
suspension_preserves_zero_inference_rule()
suspension_preserves_zero_multiple_inference_rule()
equality_preserved_under_right_composition_inference_rule()
equality_preserved_under_left_composition_inference_rule()
equality_preserved_under_multiple_inference_rule()
nested_integer_multiple_inference_rule()
equality_symmetry_inference_rule()
equality_transitivity_inference_rule()
```

Phase 57-2 では:

```text
2ι₃∘α=2α
+
2α=0
↓
2ι₃∘α=0
```

の後半を generic `zero_equality_implies_zero_inference_rule()` に任せた。

Phase 58-5 では:

```text
Eη₃=η₄
↓
Eη₃∘η₅=η₄∘η₅
↓
η₃∘(Eη₃∘η₅)=η₃∘(η₄∘η₅)
```

に左右 composition preservation rule を利用する。

重要な API:

```text
equality_preserved_under_right_composition_inference_rule(right_expression)
equality_preserved_under_left_composition_inference_rule(left_expression)
```

factor は premise ではなく rule constructor に渡す。

これらは出力 Relation に再適用可能なので、Phase 58 representative flow では one-shot application とする。

---

# 5. scalar_rules.py

## 役割

symbolic scalar に関する statement / rule。

代表:

```text
OddScalarStatement
EvenScalarStatement
ScalarGreaterEqualStatement
ScalarCongruenceStatement
```

Phase 46 stable range、Phase 56 `i≥3` などで利用。

一般 symbolic CAS ではない。

---

# 6. homotopy_groups.py

## 役割

ホモトピー群・primary component・Toda-specific group / map instance の structural data。

## 主な class family

```text
PrimaryComponent
TodaPrimaryGroup
PrimaryComponentMembershipStatement
TodaPrimaryGroupMembershipStatement
TodaPrimaryGroupZeroStatement
PreimageSubgroup
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
```

EHP / Toda map object:

```text
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
TodaIteratedSuspensionMap
TodaProp44DecompositionMap
TodaEHPExactnessWindow
```

重要:

```text
PreimageSubgroup
!=
specific element preimage Δ^-1(x)
```

Phase 57 では後者を dedicated statement で扱う。

---

# 7. map_facts.py

## 役割

canonical map symbols。

```text
EHP_E_MAP
EHP_H_MAP
EHP_DELTA_MAP
```

`MapApplication` と組み合わせて:

```text
H(β)
Δ(E²α)
H(ν′)
```

を表す。

---

# 8. map_property_rules.py

## 役割

injective / surjective / isomorphism 等の generic map property。

代表 statement:

```text
InjectiveMapStatement
SurjectiveMapStatement
IsomorphismStatement
```

Toda-specific theorem instance と generic map property を分離する。

---

# 9. barratt_hilton_rules.py

## 役割

Barratt–Hilton / Toda Proposition 3.1 周辺。

## 主な class

### `HomotopyGroupMembershipStatement`

```text
element ∈ π_k(S^n)
```

の current generic membership statement。

Phase 57 / 58 では:

```text
α∈π_i(S³)
β∈π_{i+2}(S³)
γ∈π_{i+2}(S⁴)
ν′∈π_6(S³)
```

に利用。

## 主な rule

```text
barratt_hilton_first_inference_rule()
barratt_hilton_second_inference_rule()
```

## 設計上の注意

`HomotopyGroupMembershipStatement` がこの module にある配置は歴史的経緯による。

Phase 58 では移動しない。

将来 concrete need が生じた場合のみ配置変更を検討する。

---

# 10. toda_rules.py

## 役割

Toda 固有の theorem knowledge を置く中心 module。

Phase 59 までは:

```text
actual proof need
↓
minimum consequence
```

を追加する方針。

full theorem CAS ではない。

---

## 10.1 Toda bracket 基盤

代表 statement:

```text
TodaBracketMembershipStatement
TodaBracketMembershipTheoremStatement
TodaBracketDefinedStatement
```

代表 rule:

```text
toda_bracket_membership_from_theorem_inference_rule()
indexed_toda_bracket_membership_from_theorem_inference_rule()
toda_bracket_defined_by_zero_compositions_inference_rule()
indexed_toda_bracket_index1_defined_inference_rule()
```

---

## 10.2 Toda Lemma 4.1 / Proposition 4.2 / (4.5) / Proposition 4.4

代表 statement:

```text
TodaProp42ExactnessStatement
Toda45IsomorphismStatement
TodaProp44IsomorphismStatement
TodaProp44FirstSummandRestrictionStatement
TodaProp44SecondSummandRestrictionStatement
TodaProp44SuspensionInjectiveStatement
```

代表 rule:

```text
toda_lemma41_odd_case_inference_rule()
toda_lemma41_even_nonzero_case_inference_rule()
toda_lemma41_even_zero_case_inference_rule()
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
toda_45_pi4_3_finite_cyclic_transport_inference_rule()
toda_prop44_isomorphism_inference_rule()
toda_prop44_first_summand_restriction_inference_rule()
toda_prop44_suspension_injective_inference_rule()
toda_prop44_eta2_n2_isomorphism_inference_rule()
toda_prop44_eta2_second_summand_restriction_inference_rule()
```

---

## 10.3 concrete π_3^2 / π_4^3 branch

代表 statement:

```text
TodaPi32Eta2DefinitionStatement
TodaProp27HopfInvariantUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
TodaDeltaImageUpToSignStatement
```

代表結果:

```text
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
Δ(ι₅)=±2η₂
```

---

## 10.4 η-family / Proposition 5.1 / Toda (5.2)

代表:

```text
TodaEtaFamilyDefinitionStatement
TodaProp51FiniteDimensionalStatement
Toda52CompositionIsomorphismStatement
```

代表 rule:

```text
toda_eta_family_definition_statement()
toda_eta3_suspension_relation_inference_rule()
toda_higher_eta_family_bridge_inference_rule()
toda_prop51_finite_dimensional_integration_inference_rule()
toda_52_eta2_composition_isomorphism_inference_rule()
```

Phase 54 symbolic higher η bridge は `ScalarSymbol` index を対象とする。

---

## 10.5 Phase 57：Lemma 5.2

Phase 57 で追加された主要 statement:

```text
TodaProp26HopfBracketConsequenceStatement
TodaDeltaPreimageUpToSignStatement
TodaLemma52BracketCompositionMembershipStatement
TodaLemma52BracketRepresentativeStatement
```

### Lemma 4.5 minimum rule

```text
toda_lemma45_n4_two_iota3_composition_inference_rule()
```

### Proposition 2.6 specialization

```text
toda_prop26_lemma52_hopf_bracket_inference_rule()
```

### Δ inverse bridge

```text
toda_lemma52_delta_two_eta2_preimage_inference_rule()
```

### Proposition 1.4 / 1.3 / Corollary 3.7

```text
toda_prop14_lemma52_bracket_transformation_inference_rule()
toda_prop13_lemma52_bracket_transformation_inference_rule()
toda_cor37_lemma52_representative_inference_rule()
```

### indeterminacy vanishing

```text
toda_prop51_eta4_twice_zero_inference_rule()
toda_21_lemma52_suspended_indeterminacy_zero_inference_rule()
toda_lemma45_n4_suspension_zero_reflection_inference_rule()
```

### end-to-end integration

```text
toda_lemma52_prop26_first_zero_inference_rule()
toda_lemma52_hopf_value_inference_rule()
toda_lemma52_double_value_inference_rule()
toda_lemma52_beta_membership_inference_rule()
toda_lemma52_delta_e2_alpha_zero_inference_rule()
```

最終:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

---

## 10.6 Phase 58：Toda (5.3) ν′ consequence

主要 statement:

```text
Toda53NuPrimeBracketSpecializationStatement
```

### ν′ bracket specialization

```text
toda_53_nu_prime_bracket_specialization_inference_rule()
```

認識:

```text
ν′∈{η₃,2ι₄,η₄}_1
↓
α=η₃
i=4
β=ν′
```

### 2η₃=0

```text
toda_53_eta3_twice_zero_inference_rule()
```

derived:

```text
π_4^3=Z/2{η₃}
↓
2η₃=0
```

### raw Lemma 5.2 specialization

```text
toda_53_nu_prime_lemma52_hopf_inference_rule()
toda_53_nu_prime_lemma52_double_inference_rule()
toda_53_nu_prime_lemma52_membership_inference_rule()
```

raw result:

```text
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
ν′∈π_6^3
```

### concrete η₅ bridge

```text
toda_53_eta5_iterated_suspension_bridge_inference_rule()
```

```text
E²η₃=η₅
```

### concrete η₄ bridge

```text
toda_53_eta4_suspension_bridge_inference_rule()
```

```text
Eη₃=η₄
```

Phase 58 専用 bridge は concrete constructor の `η_4` / `η_5` と canonical `η₄` / `η₅` を局所的に接続する。

global η-name normalization はしない。

### final relation

generic relation rule を再利用して:

```text
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

を導出する。

`toda_rules.py` に generic composition rewrite は追加していない。

---

### `toda_rules.py` に追加しないもの

```text
generic equality transitivity
generic fixed-point engine
generic scalar normalization
generic concrete η normalization
generic Toda-bracket CAS normalization
generic Toda-bracket specialization framework
generic coset algebra
generic sign solver
generic inverse-image solver
```


## 10.7 Phase 59：Toda Proposition 5.3 finite-dimensional branch

主要 aggregate:

```text
TodaProp53FiniteDimensionalStatement
```

保持:

```text
pi4_2_group_relation
pi5_3_group_relation
pi6_4_group_relation
higher_eta_squared_group_relation
higher_range
```

主要 Phase 59 rule family:

```text
toda_52_pi4_2_finite_cyclic_transport_inference_rule()

toda_53_n3_prop51_delta_injective_inference_rule()
toda_53_n3_delta_injective_hopf_zero_inference_rule()
toda_53_n3_hopf_zero_suspension_surjective_inference_rule()
toda_53_n3_hopf_eta5_surjective_inference_rule()
toda_53_n3_hopf_surjective_delta_zero_inference_rule()
toda_53_n3_delta_zero_suspension_injective_inference_rule()
toda_53_n3_suspension_isomorphism_inference_rule()

toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()

toda_prop53_n4_phase48_injectivity_bridge_inference_rule()
toda_prop53_n4_zero_right_suspension_surjective_inference_rule()
toda_prop53_n4_suspension_isomorphism_inference_rule()

toda_prop53_n4_eta_square_suspension_bridge_inference_rule()
toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule()

toda_prop53_eta4_squared_stable_transport_inference_rule()
toda_prop53_higher_eta_squared_bridge_inference_rule()
toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule()
toda_prop53_finite_dimensional_integration_inference_rule()
```

主要 final results:

```text
π_4^2=Z/2{η₂²}
π_5^3=Z/2{η₃²}
π_6^4=Z/2{η₄²}
π_{n+2}^n=Z/2{η_n²}, n≥5
```

`η_n²` は dedicated class ではなく:

```text
Composition(η_n,η_{n+1})
```

として保持する。

Phase 46 の symbolic exponent は structural に:

```text
ScalarSum(n,ScalarProduct(-1,4))
```

を維持する。`ScalarSum(n,-4)` への global scalar normalization は行わない。

Phase 59 で追加しないもの:

```text
EtaSquare
generic cyclic-generator transport
generic suspension/composition normalization
generic η-family normalization
stable homotopy-group model
```

---


## 10.8 Phase 60：Toda Lemma 5.4 / ν₄ construction

### Toda (5.4) statement / indeterminacy

主要 statement:

```text
Toda54BracketUpToSignStatement
Toda54IndeterminacyGeneratorStatement
```

主要 rule:

```text
toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule()
toda_54_nu_prime_triple_eta_transport_inference_rule()
toda_54_indeterminacy_double_nu_prime_generator_inference_rule()
toda_54_nu_prime_bracket_inclusion_inference_rule()
toda_54_t_ge_1_up_to_sign_inference_rule()
toda_32_phase60_suspension_surjective_inference_rule()
toda_54_t0_bridge_inference_rule()
```

final symbolic result:

```text
{η_n,2ι_(n+1),η_(n+1)}_t
=
{±E^(n-3)ν′}
```

`t=0` は unindexed `TodaBracket` で保持する。

### Theorem 3.6 specialization

主要 statement:

```text
Toda36Lemma54SpecializationStatement
TodaLemma54DoubleSuspensionUpToSignStatement
```

主要 rule:

```text
toda_lemma54_eta6_twice_zero_inference_rule()
toda_36_lemma54_specialization_inference_rule()
toda_54_n5_t3_specialization_inference_rule()
toda_lemma54_double_suspension_up_to_sign_inference_rule()
```

final:

```text
α*∈π_7^4
2Eα*=±E²ν′
```

### Hopf parity

statement:

```text
TodaLemma54HopfOddMultipleStatement
```

rule:

```text
toda_lemma54_pi6_5_finite_cyclic_inference_rule()
toda_48_lemma54_hopf_odd_multiple_inference_rule()
```

意味:

```text
H(α*)=(2s+1)ι₇
```

`parameter=s` を Whitehead correction へ渡す。

### Whitehead correction

statement:

```text
TodaLemma54WhiteheadCorrectionDataStatement
TodaLemma54Nu4BranchFormula
TodaLemma54Nu4ConstructionStatement
```

rule:

```text
toda_lemma54_whitehead_correction_data_inference_rule()
toda_lemma54_nu4_piecewise_construction_inference_rule()
toda_lemma54_nu4_membership_inference_rule()
toda_lemma54_nu4_hopf_inference_rule()
toda_lemma54_nu4_double_suspension_inference_rule()
```

final:

```text
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
```

### Lemma 5.4 aggregate

statement:

```text
TodaLemma54Statement
```

helper / rule:

```text
toda_lemma54_literature_statements()
toda_lemma54_integration_inference_rule()
```

aggregate は Phase 60-8 の3 derived result のみを premise とする。

```text
membership        INFERENCE
Hopf relation     INFERENCE
double suspension INFERENCE
↓
TodaLemma54Statement INFERENCE
```

### Phase 60 で追加しないもの

```text
generic Toda-bracket coset algebra
generic sign solver
generic divisibility framework
generic existential witness framework
generic Whitehead correction algebra
full Theorem 3.6 formalization
full Toda (4.8) formalization
theorem statement repository / search
```

---


## 10.9 Phase 61：Toda Lemma 5.5 bracket transport

### statement

```text
TodaLemma55BracketContainsUpToSignStatement
TodaLemma55SuspensionUpToSignStatement
TodaLemma55Statement
```

#### `TodaLemma55BracketContainsUpToSignStatement`

```text
bracket
positive_value
```

意味:

```text
bracket contains positive_value or -positive_value
```

Phase 60 `Toda54BracketUpToSignStatement` の `{±x}` value-set semantics とは異なる。

#### `TodaLemma55SuspensionUpToSignStatement`

```text
left
positive_value
```

Phase 61 concrete use:

```text
left = E^tν₄
positive_value = E^tα*
```

意味:

```text
E^tν₄=±E^tα*
```

#### `TodaLemma55Statement`

final aggregate。保持:

```text
nu4
lemma54_statement
beta_membership
beta_eta_zero_relation
t_range
bracket_inclusion
literature_statements
```

`lemma54_statement` を nested に保持し、Phase 60 theorem-level provenance を切らない。

### rule

```text
toda_lemma55_alpha_star_bracket_inclusion_inference_rule()
toda_lemma55_nu4_suspension_correction_inference_rule()
toda_lemma55_alpha_star_to_nu4_composition_inference_rule()
toda_lemma55_integration_inference_rule()
```

#### α* bracket inclusion

```text
Toda36Lemma54SpecializationStatement  INFERENCE
β∈π_(t+2)(S^m)
β∘η_(t+2)=0
t≥1
↓
bracket contains ±(E²β∘E^tα*)
```

#### ν₄ suspension correction

```text
TodaLemma54Nu4ConstructionStatement INFERENCE
+ t≥1
+ E[ι₄,ι₄]=0 stored in whitehead_data
↓
E^tν₄=±E^tα*
```

#### composition bridge

```text
bracket contains ±(E²β∘E^tα*)
+
E^tν₄=±E^tα*
↓
bracket contains ±(E²β∘E^tν₄)
```

Lemma-5.5-specific rule。generic up-to-sign transitivity ではない。

#### integration

```text
TodaLemma54Statement                  INFERENCE
β membership                         GIVEN
β∘η zero                             GIVEN
t≥1                                  GIVEN
final ν₄ bracket inclusion           INFERENCE
↓
TodaLemma55Statement                 INFERENCE
```

### literature helper

```text
toda_lemma55_literature_statements()
```

直接保持:

```text
Toda Lemma 5.5
Toda Lemma 5.5 proof
```

Phase 60 literature は `TodaLemma55Statement.lemma54_statement.literature_statements` から参照する。

### probe

```text
probes/probe_phase61_capabilities.py
```

主要 function:

```text
build_phase61_representative_result()
print_phase61_results()
print_phase61_derivation_chain()
print_phase61_provenance()
phase61_literature_usage()
print_phase61_literature_statements()
print_phase61_boundary()
main()
```

Phase 60 と同じく focused integration builder を representative fixture として再利用し、probe 側へ theorem logic を複製しない。

Phase 61 固有表示:

```text
theorem dependencies are INFERENCE = True
Lemma 5.5 hypotheses remain GIVEN = True
```

### tests

```text
tests/test_phase61_lemma55_statement.py
tests/test_phase61_lemma55_alpha_star_inclusion.py
tests/test_phase61_lemma55_nu4_suspension.py
tests/test_phase61_lemma55_nu4_composition.py
tests/test_phase61_lemma55_integration.py
tests/test_phase61_lemma55_applicability_provenance.py
tests/test_phase61_probe.py
```

Phase 61-7 は production code を変更せず、wrong-instance rejection / GIVEN-INFERENCE boundary / ancestry reachability / acyclicity を regression で固定する。

### deferred boundary

```text
generic bracket containment algebra
generic up-to-sign transitivity
generic sign solver
generic Whitehead correction algebra
full Theorem 3.6 formalization
automatic proof narrative generator
```

# 11. probes/

## 役割

人間が capability を確認できる代表実行。

probe は:

```text
actual representative GIVEN
+
production inference rules
↓
derived result
```

を組み立てる integration fixture としても使う。

代表:

```text
probes/probe_phase49_capabilities.py
probes/probe_phase50_capabilities.py
probes/probe_phase55_capabilities.py
probes/probe_phase56_capabilities.py
probes/probe_phase57_capabilities.py
probes/probe_phase58_capabilities.py
probes/probe_phase59_capabilities.py
probes/probe_phase60_capabilities.py
probes/probe_phase61_capabilities.py
probes/probe_phase62_capabilities.py
```

Phase 58:

```powershell
python -m probes.probe_phase58_capabilities
```

確認:

```text
ν′ ∈ π_6^3
H(ν′) = η₅
2ν′ = η₃∘η₄∘η₅
```

provenance:

```text
all final results are INFERENCE = True
final results are GIVEN = False
```

execution:

```text
fixed-point-safe stages complete = True
composition propagation one-shot = True
shared raw specialization = True
```

---


Phase 60:

```powershell
python -m probes.probe_phase60_capabilities
```

確認:

```text
ν₄ ∈ π_7^4
H(ν₄) = ι₇
2Eν₄ = E²ν′
```

provenance:

```text
final aggregate derived = True
final aggregate is GIVEN = False
all final premises are INFERENCE = True
fixed point = True
```

literature:

```text
Reference / Locator / Author / Source / Year
Used in: Phase 60-x ...
Statement: ...
```

`phase60_literature_usage()` は probe-local display mapping であり production theorem model ではない。

### `print_phase60_derivation_chain()`

Phase 60-10 proof-style derivation improvement で追加。

責務:

```text
Phase 60-3〜8 の proof flow を
Toda の証明本文に近い順序で表示する
```

代表表示:

```text
Phase 60-4: bracket inclusion

ν′ ∈ {η₃,2ι₄,η₄}_1
↓
E^(n-3)ν′
∈ E^(n-3){η₃,2ι₄,η₄}_1
⊂ (-1)^(n-3){η_n,2ι_(n+1),η_(n+1)}_(n-2)
  [Toda Proposition 1.3]
⊂ (-1)^(n-3){η_n,2ι_(n+1),η_(n+1)}_t
  [Toda (1.15)]
```

重要な境界:

```text
この関数は presentation-only
proof semantics を生成しない
ProofStep graph から自動生成していない
```

current `main()` display order:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Completion boundary
```

将来は `ProofStep` / `Expression` / `InferenceRule` / `LiteratureStatement` から同種の表示を自動生成する proof narrative generator を検討する。current Phase 60 code をその generic framework と誤認しないこと。

---

# 12. tests/

## 役割

```text
representation
applicability
wrong input rejection
integration
provenance
scope
fixed point / execution scope
```

を検証する。

Phase-specific naming:

```text
tests/test_phaseNN_*.py
```

Phase 57:

```text
test_phase57_lemma45_two_iota3.py
test_phase57_prop26_hopf_bracket.py
test_phase57_delta_two_eta2_preimage.py
test_phase57_bracket_transformation_chain.py
test_phase57_indeterminacy_vanishing.py
test_phase57_lemma52_integration.py
test_phase57_probe.py
```

Phase 58:

```text
test_phase58_nu_prime_specialization.py
test_phase58_lemma52_specialization.py
test_phase58_hopf_eta5_bridge.py
test_phase58_double_eta4_bridge.py
test_phase58_probe.py
```

Phase 59 completion regression:

```text
3177 passed in 123.99s
```

---


Phase 60 focused suites:

```text
tests/test_phase60_toda54_bracket_statement.py
tests/test_phase60_toda54_indeterminacy.py
tests/test_phase60_toda54_bracket_inclusion.py
tests/test_phase60_toda54_t0_bridge.py
tests/test_phase60_toda36_specialization.py
tests/test_phase60_toda48_hopf_parity.py
tests/test_phase60_nu4_whitehead_correction.py
tests/test_phase60_lemma54_integration.py
tests/test_phase60_probe.py
```

Phase 60 completion full regression:

```text
3334 passed in 132.72s
```

---

# 13. 新しい Phase で最初に見る場所

## 新しい式が必要

```text
expression.py
関連 expression tests
```

## 新しい group / map object が必要

```text
homotopy_groups.py
map_facts.py
```

## generic relation mechanics が不足

```text
relation_rules.py
proof.py
```

ただし theorem 固有なら theorem-specific module を優先。

## Toda の theorem / lemma

```text
toda_rules.py
既存 Phase-specific tests
source material
```

## end-to-end capability

```text
probes/
integration tests
```

---

# 14. provenance を壊さないための確認

theorem-specific final rule で:

```text
proof_rule=ProofRule.INFERENCE
```

を premise pattern に要求する場合がある。

目的:

```text
過去 Phase で derived した theorem result
```

を `GIVEN` として再投入して循環・shortcut を作らないこと。

Phase 55 / 56 / 57 / 58 の integration では特に重要。

Phase 58 probe では `2η₃=0` の step を単に:

```text
rule == INFERENCE
```

で選ばず、期待する conclusion:

```text
2η₃=0
```

そのものに一致する step を選ぶ。

入力 step 自体も `INFERENCE` の場合があるため、rule 種別だけでは provenance source を特定できない。

---

# 15. structural normalization を追加する前の確認

例えば:

```text
2*2-1 → 3
E^1α → Eα
-(order-two element) → element
η_4 → η₄
η_5 → η₅
```

を global normalizer にする前に:

```text
今回の concrete theorem にだけ必要か？
```

を確認する。

YES の場合:

```text
dedicated bridge / specialization
```

を優先する。

複数 independent branch で同じ generic need が繰り返し発生した時点で generalization を検討する。

---

# 16. repeatable inference rule の実行境界

`Relation → Relation` の rule は、出力が再び同じ rule の premise になる可能性がある。

Phase 58 で確認した例:

```text
equality_preserved_under_right_composition_inference_rule(η₅)
equality_preserved_under_left_composition_inference_rule(η₃)
```

unrestricted fixed-point に入れると:

```text
a=b
↓
a∘η₅=b∘η₅
↓
(a∘η₅)∘η₅=(b∘η₅)∘η₅
↓
...
```

のように distinct conclusion が増え続ける。

したがって:

```text
fixed-point-safe
→ fixed-point runner

repeatable / scope-sensitive
→ one-shot or staged application
```

を使い分ける。

generic engine を変更して自動抑制することは Phase 58 の scope 外。

---

# 17. code_reference.md の更新ルール

毎 Phase 必須ではない。

更新するのは主に:

```text
新規 module を追加した
主要 class family を追加した
module の責務が変わった
重要な end-to-end entry point が増えた
execution-scope 上の重要な注意が増えた
```

場合。

細かな helper をすべて追記しない。

---

# 18. 将来 proof narrative generation で確認する場所

current manual representative:

```text
probes/probe_phase60_capabilities.py
  print_phase60_derivation_chain()
  phase60_literature_usage()
```

将来 generic generator を検討するときの主要 input:

```text
proof.py
  ProofStep
  InferenceRule
  LiteratureReference
  LiteratureStatement

expression.py
  Expression family

toda_rules.py / domain rules
  theorem-specific provenance
  rule descriptions

probes/
  concrete human-readable output examples
```

候補 pipeline:

```text
ProofStep graph
↓
path extraction
↓
step grouping / compression
↓
equation rendering
↓
citation insertion
↓
narrative template
↓
console / Markdown / LaTeX
```

複数 Phase で display pattern が安定するまでは専用 probe 表示を優先する。

---

# 19. Phase 62 で最初に確認する場所

Phase 61 implementation は完了。

Phase 62 target:

```text
ν-family / Toda (5.5)
```

最初に確認:

```text
Toda source material
  Toda (5.5) statement / proof

toda_rules.py
  TodaLemma54Statement
  TodaLemma55Statement
  Phase 58 ν′ relation
  η-family bridge rule family

expression.py
  Composition
  IteratedSuspension
  HomotopyElement

relation_rules.py
  suspension / equality transport の既存 rule

probes/probe_phase61_capabilities.py
  current ν₄ provenance / proof-display boundary

tests/test_phase60_*.py
tests/test_phase61_*.py
  ν₄ / provenance regression

docs/roadmap.md
  Phase 62 finite-dimensional / stable boundary
```

Phase 62 では:

```text
ν_n:=E^(n-4)ν₄
↓
2ν_n=E^(n-3)ν′
↓
4ν_n=η_n³
```

の minimum bridge を先に調べる。

引き続き:

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

を維持する。

---

# 20. Phase 62：ν-family / Toda (5.5)

## statement

```text
TodaNuFamilyDefinitionStatement
Toda55NuFamilyFiniteDimensionalStatement
```

### `TodaNuFamilyDefinitionStatement`

field:

```text
index
element
iterated_suspension
```

helper:

```text
toda_nu_family_definition_statement(n)
```

意味:

```text
ν_n:=E^(n-4)ν₄
```

concrete `n<4` は reject。

symbolic exponent:

```text
ScalarSum(n,-4)
```

### `Toda55NuFamilyFiniteDimensionalStatement`

保持:

```text
nu_family_definition
lemma54_statement
n_range
double_nu_relation
quadruple_nu_relation
literature_statements
```

---

# 21. Phase 62 double-value transport

rule:

```text
toda_55_nu_family_double_suspension_transport_inference_rule()
```

input:

```text
TodaLemma54Statement       INFERENCE
TodaNuFamilyDefinitionStatement
ScalarGreaterEqualStatement(n,5)
```

validate:

```text
definition matches symbolic n
base ν₄ matches Lemma 5.4
Lemma 5.4 relation is exactly 2Eν₄=E²ν′
```

output:

```text
2ν_n=E^(n-3)ν′
```

reject:

```text
GIVEN Lemma 5.4
n≥4
wrong symbolic index
wrong family definition
wrong Lemma 5.4 relation
```

---

# 22. Phase 62 eta-cube bridge

production theorem rule:

```text
追加なし
```

test builder:

```text
tests/test_phase62_nu_family_eta_cube_bridge.py
  build_phase62_4_data()
```

reused generic rule:

```text
equality_preserved_under_multiple_inference_rule()
nested_integer_multiple_inference_rule()
equality_symmetry_inference_rule()
equality_transitivity_inference_rule()
```

Phase 60 builder から:

```text
2E^(n-3)ν′
=
η_n∘η_(n+1)∘η_(n+2)
```

を再利用。

---

# 23. Phase 62 integration / literature

literature helper:

```text
toda_55_nu_family_literature_statements()
```

integration:

```text
toda_55_nu_family_finite_dimensional_integration_inference_rule()
```

premises:

```text
TodaLemma54Statement                INFERENCE
TodaNuFamilyDefinitionStatement     GIVEN
ScalarGreaterEqualStatement         GIVEN
2ν_n relation                       INFERENCE
4ν_n relation                       INFERENCE
```

final:

```text
Toda55NuFamilyFiniteDimensionalStatement
ProofRule.INFERENCE
```

direct literature:

```text
Toda (5.5)
Equation (5.5)
```

Phase 60 literature は nested `lemma54_statement` から参照。

---

# 24. Phase 62 test builders

```text
tests/test_phase62_nu_family_double_transport.py
  build_phase62_3_data()

tests/test_phase62_nu_family_eta_cube_bridge.py
  build_phase62_4_data()

tests/test_phase62_applicability_provenance.py
  build_phase62_5_data()

tests/test_phase62_toda55_integration.py
  build_phase62_6_data()

tests/test_phase62_toda55_applicability_provenance.py
  build_phase62_7_data()
```

重要:

```text
id() ancestor check
→ same nested fixture tree を共有
```

同じ conclusion を持つ別 `ProofStep` instance を再構築しない。

---

# 25. Phase 62 representative probe

module:

```text
probes/probe_phase62_capabilities.py
```

主要 function:

```text
build_phase62_representative_result()
print_phase62_results()
print_phase62_derivation_chain()
print_phase62_provenance()
phase62_literature_usage()
print_phase62_literature_statements()
print_phase62_boundary()
main()
```

focused integration builder:

```text
build_phase62_6_data()
```

を representative fixture として再利用し、probe 側へ theorem logic を複製しない。

---

# 26. Phase 62 focused tests

```text
tests/test_phase62_nu_family_definition.py               9 passed
tests/test_phase62_nu_family_double_transport.py        14 passed
tests/test_phase62_nu_family_eta_cube_bridge.py         13 passed
tests/test_phase62_applicability_provenance.py          17 passed
tests/test_phase62_toda55_integration.py                24 passed
tests/test_phase62_toda55_applicability_provenance.py   19 passed
tests/test_phase62_probe.py                             18 passed
```

full regression:

```text
3550 passed in 411.22s
```

---

# 27. Phase 63 開始時点で最初に確認した場所（履歴）

target:

```text
Toda (5.6)
```

確認:

```text
Toda source
  Equation (5.6)

toda_rules.py
  TodaProp44IsomorphismStatement
  Prop.4.4 rule family
  TodaLemma54Statement
  ν₄ Hopf relation

homotopy_groups.py
  TodaProp44DecompositionMap
  DirectSumGroup
  TodaPrimaryGroup

tests/test_phase47_*.py
  Prop.4.4 decomposition behavior

tests/test_phase60_*.py
  ν₄ / H(ν₄)=ι₇ provenance

probes/probe_phase62_capabilities.py
  current proof-display pattern
```

compatibility target:

```text
n=4
α=ν₄
H(ν₄)=ι₇
↓
Prop.4.4
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

map formula:

```text
(α,β)
↦
Eα+ν₄∘β
```

Phase 63 では concrete specialization の minimum bridge のみ追加する。

stable ν / η³、generic direct-sum framework extension、automatic proof narrative generation は先取りしない。



---

# 28. Phase 63：Toda (5.6) ν₄ decomposition

## `toda_rules.py`

Phase 63 で追加した主要 statement:

```text
Toda56Nu4Prop44SpecializationStatement
Toda56Nu4DecompositionIsomorphismStatement
Toda56Nu4DecompositionStatement
```

### `Toda56Nu4Prop44SpecializationStatement`

保持:

```text
lemma54_statement
n
alpha
membership
hopf_relation
```

Phase 60 `TodaLemma54Statement` を Phase 47 Proposition 4.4 の concrete `n=4`, `α=ν₄` specialization premise に接続する。

重要 bridge:

```text
HomotopyGroupMembershipStatement(ν₄,7,4)
↓ narrow Phase 63 specialization
TodaPrimaryGroupMembershipStatement(ν₄, π_7^4)
```

rule:

```text
toda_56_nu4_prop44_specialization_inference_rule()
```

### `Toda56Nu4DecompositionIsomorphismStatement`

field:

```text
prop44_isomorphism
```

既存 `TodaProp44IsomorphismStatement` を Toda (5.6) 専用 semantics として保持する。

rule:

```text
toda_56_nu4_decomposition_isomorphism_inference_rule()
```

### `Toda56Nu4DecompositionStatement`

field:

```text
decomposition_isomorphism
lemma54_statement
literature_statements
```

final literature-aware aggregate。

helper / integration rule:

```text
toda_56_nu4_decomposition_literature_statements()
toda_56_nu4_decomposition_integration_inference_rule()
```

---

# 29. Phase 63 Proposition 4.4 specialization

Phase 63-3 では新しい map / group class を追加しない。

再利用:

```text
homotopy_groups.py
  DirectSumGroup
  TodaPrimaryGroup
  TodaProp44DecompositionMap

toda_rules.py
  TodaProp44IsomorphismStatement
```

symbolic `i`:

```text
ScalarSymbol("i")
```

first summand:

```text
TodaPrimaryGroup(
  group_dimension=ScalarSum(i,-1),
  sphere_dimension=3,
)
```

second summand:

```text
TodaPrimaryGroup(
  group_dimension=i,
  sphere_dimension=7,
)
```

target:

```text
TodaPrimaryGroup(
  group_dimension=i,
  sphere_dimension=4,
)
```

formula:

```text
Sum(
  Suspension(first_variable),
  Composition(ν₄, second_variable),
)
```

意味:

```text
Eα+ν₄∘β
```

Phase 47 field naming:

```text
map.beta  = displayed α
map.gamma = displayed β
```

rule:

```text
toda_56_nu4_prop44_isomorphism_inference_rule()
```

重要 boundary:

```text
TodaProp44DecompositionMap      GIVEN
TodaProp44IsomorphismStatement  INFERENCE
```

---

# 30. Phase 63 provenance / literature

provenance spine:

```text
Phase 60 membership / Hopf / double relations
↓
TodaLemma54Statement
↓
Toda56Nu4Prop44SpecializationStatement
↓
TodaProp44IsomorphismStatement
↓
Toda56Nu4DecompositionIsomorphismStatement
↓
Toda56Nu4DecompositionStatement
```

`tests/test_phase63_applicability_provenance.py` では identity-based ancestor traversal を使う。

確認:

```text
GIVEN theorem replacement rejection
ancestor reachability
acyclic final graph
final conclusion absent from ancestors
upstream independence
```

direct literature:

```text
Toda (5.6)
Equation (5.6)
```

inherited literature:

```text
Toda56Nu4DecompositionStatement
└─ lemma54_statement
   └─ literature_statements
```

---

# 31. Phase 63 representative probe

```text
probes/probe_phase63_capabilities.py
```

entry point:

```powershell
python -m probes.probe_phase63_capabilities
```

主要 helper:

```text
build_phase63_representative_result()
print_phase63_results()
print_phase63_derivation_chain()
print_phase63_provenance()
phase63_literature_usage()
print_phase63_literature_statements()
print_phase63_boundary()
main()
```

既存 display helper を再利用:

```text
probes.probe_phase50_capabilities.print_separator
probes.probe_phase61_capabilities.print_literature_item
```

probe は:

```text
tests/test_phase63_toda56_integration.py
  build_phase63_6_data()
```

を representative fixture として再利用する。

theorem logic は probe 側へ複製しない。

proof-style derivation は hand-authored presentation layer。

---

# 32. Phase 63 focused tests

```text
tests/test_phase63_nu4_prop44_specialization.py              15 passed
tests/test_phase63_prop44_decomposition_specialization.py    19 passed
tests/test_phase63_toda56_semantics.py                       17 passed
tests/test_phase63_applicability_provenance.py               20 passed
tests/test_phase63_toda56_integration.py                     19 passed
tests/test_phase63_probe.py                                  17 passed
```

full regression:

```text
3657 passed in 939.47s
```

---

# 33. Phase 63 completion boundary

実装済み:

```text
n=4 / α=ν₄ specialization bridge
Toda-primary ν₄ membership bridge
concrete Proposition 4.4 decomposition specialization
Toda (5.6) map / isomorphism semantics
literature-aware aggregate
Phase 60 inherited literature
applicability / acyclic provenance regression
representative proof-style probe
```

未実装:

```text
generic Proposition 4.4 specialization framework
generic scalar normalization
generic membership normalization
generic direct-sum simplification
stable ν / η³
automatic proof narrative generation
later Toda consequences after Equation (5.6)
```

---


# 34. Phase 64：performance-related code reference

Phase 64 は新しい数学 theorem family を追加しない。

主な変更対象:

```text
proof.py
tests / probes の deterministic builder
tests/test_algebra.py
```

---

# 35. `proof.py` Phase 64 matching path

Phase 64-5 で追加:

```text
_find_all_matching_premise_bindings()
```

責務:

```text
recursive premise assignment
+
merged VariableBinding
```

を同時に返す。

既存 public:

```text
find_all_matching_premises()
```

は従来どおり premise tuple の collection を返す。

`find_inference_matches_for_rule()` は private helper の bindings を再利用し、同じ premise assignment に対する再 binding を避ける。

確認対象:

```text
match_premise_pattern()
merge_variable_bindings()
_find_all_matching_premise_bindings()
find_all_matching_premises()
find_inference_matches_for_rule()
find_inference_matches()
```

未実装:

```text
premise-type index
agenda/worklist
incremental fixed-point engine
global proof memoization
```

---

# 36. deterministic Phase builder cache

Phase 57–63 の一部 builder は:

```text
no-arg
deterministic
caller が returned proof graph を mutate しない
```

場合に:

```python
@lru_cache(maxsize=1)
```

を利用する。

cache 前に確認:

```text
no-arg
deterministic
returned data is not mutated
identity reuse is semantically safe
```

---

# 37. `tests/test_algebra.py` Phase 64 boundary

主要 exhaustive crosscheck:

```text
test_finite_presentation_crosscheck()
test_finite_exactness_presentation_crosscheck()
```

目的:

```text
finite explicit enumeration
vs
presentation / integer-lattice calculation
```

維持:

```text
group case set
matrix entry ranges
checked > 500
checked > 100
```

local precomputation で利用する主な API:

```text
GroupMap.image_subgroup()
GroupMap.kernel_subgroup()
GroupMap.image_lattice_basis()
GroupMap.kernel_lattice_basis()
relation_matrix()
lattice_coordinates()
structure_from_presentation()
lattices_equal()
```

production `GroupMap` cache は追加していない。

---

# 38. Phase 64 performance reference

same-machine full regression:

```text
baseline
259.11s

after Phase 64-3c
150.42s

after Phase 64-3d
81.79s

after Phase 64-3e
43.54s

after Phase 64-5
42.67s

after Phase 64-6b
40.69s

after Phase 64-6d
29.97s
```

final:

```text
3657 passed in 29.97s
```

algebra:

```text
109 passed in 7.46s
```

remaining dominant single test:

```text
test_finite_presentation_crosscheck
約 5.2s
```

現状は許容し、production cache / SNF-HNF redesign は concrete need が再発するまで deferred。

---

---

# 39. Phase 65：Toda Proposition 5.6 code reference

Phase 65 では主に:

```text
toda_rules.py
homotopy_groups.py
probes/probe_phase65_capabilities.py
tests/test_phase65_*.py
```

を更新 / 追加した。

generic `proof.py` inference machinery は Phase 65 では変更していない。

---

# 40. Phase 65 主要 statement

`toda_rules.py` の Phase 65 主要 statement:

```text
TodaSuspensionInjectiveStatement
TodaIteratedSuspensionInjectiveStatement
TodaProp56Pi8_5QuotientStatement
TodaProp56FiniteDimensionalStatement
```

### `TodaIteratedSuspensionInjectiveStatement`

保持:

```text
map: TodaIteratedSuspensionMap
```

Phase 65 concrete use:

```text
E²:π_6^3→π_8^5 injective
```

generic map-property solver を追加せず、Toda-specific iterated suspension instance を保持する。

### `TodaProp56Pi8_5QuotientStatement`

保持:

```text
ambient_group
subobject_map
quotient_order
```

Phase 65 concrete meaning:

```text
π_8^5 / E²π_6^3 ≅ Z/2
```

symbolic `QuotientGroup` algebraへの一般化はしない。

### `TodaProp56FiniteDimensionalStatement`

保持:

```text
pi5_2_group_relation
pi6_3_group_relation
pi7_4_group_relation
pi8_5_group_relation
higher_nu_group_relation
higher_range
literature_statements
```

final aggregate:

```text
ProofRule.INFERENCE
```

---

# 41. Phase 65-2 / 65-3 rule family

主要 rule:

```text
toda_prop56_pi5_2_eta2_cube_inference_rule()

toda_57_nu_prime_eta6_hopf_inference_rule()
toda_prop56_pi7_3_hopf_surjective_inference_rule()
toda_prop56_pi7_5_delta_zero_inference_rule()
toda_prop56_pi5_2_suspension_injective_inference_rule()
```

end-to-end:

```text
π_5^2=Z/2{η₂³}

H(ν′∘η₆)=η₅²
+
π_7^5=Z/2{η₅²}
↓
H surjective
↓
Δ=0
↓
E:π_5^2→π_6^3 injective
```

η₅ / η₆ concrete definition の structural-name 差は Phase 58 と同様に local guard / canonical construction で処理する。

global η normalization は追加しない。

---

# 42. Phase 65-4 order / π_6^3 rule family

```text
toda_prop56_eta3_cube_order_two_inference_rule()
toda_prop56_nu_prime_order_four_inference_rule()
toda_prop56_pi6_3_finite_cyclic_inference_rule()
```

導出:

```text
ord(η₃³)=2
ord(ν′)=4
π_6^3=Z/4{ν′}
```

generic order arithmetic framework は追加しない。

---

# 43. Phase 65-5 π_7^4 decomposition

`homotopy_groups.py`:

```text
DirectSumGroup.summands
```

は `FiniteCyclicGroup` を含められるよう拡張。

低次元 fact:

```text
π_7^7=Z{ι₇}
```

を利用。

rule:

```text
toda_prop56_pi7_4_decomposition_inference_rule()
```

final:

```text
π_7^4
=
Z{ν₄}
⊕
Z/4{Eν′}
```

---

# 44. Phase 65-6 quotient / E² injectivity

rule:

```text
toda_prop56_pi8_5_quotient_inference_rule()
toda_prop56_pi6_3_e2_injective_inference_rule()
```

両方とも Phase 63 `Toda56Nu4DecompositionStatement` の derived theorem semantics を provenance anchor とする。

generic Prop.4.4 specialization framework は追加しない。

---

# 45. Phase 65-7 n=5 order / group

rule:

```text
toda_prop56_nu5_double_relation_inference_rule()
toda_prop56_e2_nu_prime_order_four_inference_rule()
toda_prop56_nu5_order_eight_inference_rule()
toda_prop56_pi8_5_finite_cyclic_inference_rule()
```

chain:

```text
Toda (5.5), n=5
↓
2ν₅=E²ν′

π_6^3=Z/4{ν′}
+
E² injective
↓
ord(E²ν′)=4
↓
ord(ν₅)=8

quotient order 2
+
image order 4
↓
π_8^5=Z/8{ν₅}
```

---

# 46. Phase 65-8 higher transport

rule:

```text
toda_prop56_nu5_stable_transport_inference_rule()
toda_prop56_higher_nu_family_bridge_inference_rule()
toda_prop56_higher_nu_finite_cyclic_generator_inference_rule()
```

Toda (4.5):

```text
E^(n-5):π_8^5≅π_(n+3)^n
```

と ν-family definition を接続し:

```text
π_(n+3)^n=Z/8{ν_n}
(n≥6)
```

を導出する。

---

# 47. Phase 65-9 aggregate / literature

helper:

```text
toda_prop56_finite_dimensional_literature_statements()
```

integration:

```text
toda_prop56_finite_dimensional_integration_inference_rule()
```

premises:

```text
π_5^2 relation       INFERENCE
π_6^3 relation       INFERENCE
π_7^4 relation       INFERENCE
π_8^5 relation       INFERENCE
higher ν relation    INFERENCE
n≥6                  GIVEN
```

final:

```text
TodaProp56FiniteDimensionalStatement
ProofRule.INFERENCE
```

---

# 48. Phase 65 representative probe

module:

```text
probes/probe_phase65_capabilities.py
```

主要 function:

```text
build_phase65_representative_result()
print_section()
print_phase65_results()
print_phase65_exact_sequence()
print_phase65_derivation_chain()
print_phase65_provenance()
print_phase65_literature()
print_phase65_boundary()
main()
```

EHP display:

```text
π_7^3 ─H→ π_7^5 ─Δ→ π_5^2 ─E→ π_6^3 ─H→ π_6^5
```

`print_phase65_derivation_chain()` は presentation-only。

automatic proof narrative generator ではない。

probe は `tests/test_phase65_prop56_integration.py` の deterministic builder を representative fixture として再利用する。

`tests/` が Python package ではないため、probe は既存 probe pattern と同様に tests directory を `sys.path` に追加して focused integration builder を import する。

---

# 49. Phase 65 tests

主要:

```text
tests/test_phase65_pi5_2_eta2_cube.py
tests/test_phase65_equation57_injectivity.py
tests/test_phase65_nu_prime_order_pi6_3.py
tests/test_phase65_pi7_4_decomposition.py
tests/test_phase65_n5_quotient_e2_injectivity.py
tests/test_phase65_nu5_order_pi8_5.py
tests/test_phase65_nu5_stable_transport.py
tests/test_phase65_prop56_integration.py
tests/test_phase65_probe.py
tests/test_phase65_provenance.py
```

重要な deterministic builder は:

```text
@lru_cache(maxsize=1)
```

を最初から付け、Phase 64 の performance stabilization 方針を維持する。

final regression:

```text
3841 passed in 31.82s
```

---

# 50. current provenance / persistence boundary

current `ProofStep` graph は:

```text
in-memory provenance
```

である。

```text
same Python process
→ cached builder reuse possible

new process
→ normally reconstruct inference
```

persistent proof repository はまだない。

将来 repository を実装するときの確認対象:

```text
proof.py
  ProofStep
  InferenceRule

toda_rules.py
  theorem aggregates
  literature metadata

homotopy_groups.py
  group / generator representation

probes/
  human-readable proof expectations
```

---

# 51. 次 Phase で最初に確認する場所

Phase 65 は COMPLETE。

次の concrete Toda source statement / consequence が決まったら:

```text
Toda source material
  statement / proof / locator

toda_rules.py
  TodaProp56FiniteDimensionalStatement
  Phase 65 rule family

tests/test_phase65_*.py
  current Proposition 5.6 boundary

probes/probe_phase65_capabilities.py
  current proof-style / provenance display
```

を確認する。

Equation (5.8) が次 target なら:

```text
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

の current representation compatibility を最初に調べる。

Proof Repository は 7-stem 程度まで concrete calculations が蓄積した時点で separate design Phase を検討し、8–10 stem で schema を実例検証する。

引き続き:

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

を維持する。

---

# 26. Phase 66：Toda Equation (5.8)

Phase 66 target:

```text
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

production change の中心は `toda_rules.py`。

generic engine / expression / map infrastructure は変更しない。

## statement

### `Toda58WhiteheadSquareUpToSignStatement`

field:

```text
whitehead_square
positive_value
```

意味:

```text
whitehead_square
=
± positive_value
```

Phase 66 concrete use:

```text
[ι₄,ι₄]
=
±(2ν₄-Eν′)
```

Phase 52 の `TodaPi32WhiteheadSquareUpToSignStatement` は `ι₂` branch 専用なので流用しない。

### `Toda58EquationStatement`

field:

```text
delta_nu_relation
whitehead_nu_relation
delta_whitehead_relation
literature_statements
```

Equation (5.8) の3表示をまとめる literature-aware aggregate。

---

# 27. Phase 66 rule family

## `toda_58_delta_iota9_nu4_nu_prime_inference_rule()`

input:

```text
π_7^4=Z{ν₄}⊕Z/4{Eν′}
INFERENCE
```

output:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₉)=±(2ν₄-Eν′)
```

guard:

```text
exact π_7^4 decomposition
ν₄ free summand
Eν′ order-4 summand
```

## `toda_58_whitehead_square_nu_expression_inference_rule()`

input:

```text
Phase 66-3 Δ statement     INFERENCE
Phase 60 Whitehead data    INFERENCE
```

output:

```text
Toda58WhiteheadSquareUpToSignStatement

[ι₄,ι₄]=±(2ν₄-Eν′)
```

## `toda_58_delta_iota9_whitehead_square_inference_rule()`

input:

```text
Δ(ι₉)=±(2ν₄-Eν′)          INFERENCE
[ι₄,ι₄]=±(2ν₄-Eν′)        INFERENCE
```

output:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₉)=±[ι₄,ι₄]
```

generic up-to-sign transitivity ではない。

guard で concrete Equation (5.8) instance を確認する。

## `toda_58_literature_statements()`

direct literature metadata:

```text
Toda (5.8)
Equation (5.8)
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
```

## `toda_58_integration_inference_rule()`

input:

```text
Phase 66-3 result  INFERENCE
Phase 66-4 result  INFERENCE
Phase 66-5 result  INFERENCE
```

output:

```text
Toda58EquationStatement
INFERENCE
```

---

# 28. Phase 66 tests

```text
tests/test_phase66_expression_sign_compatibility.py
tests/test_phase66_delta_iota9_nu_expression.py
tests/test_phase66_whitehead_square_nu_expression.py
tests/test_phase66_delta_iota9_whitehead_square.py
tests/test_phase66_applicability_provenance.py
tests/test_phase66_literature_aggregate.py
tests/test_phase66_probe.py
```

focused completion:

```text
12 + 19 + 18 + 22 + 20 + 21 + 17
=
129 passed
```

full regression:

```text
3970 passed in 31.96s
```

fixture builder で重い同一 object graph を再利用する場合は:

```python
@lru_cache(maxsize=1)
```

を利用する。

---

# 29. Phase 66 representative probe

```text
probes/probe_phase66_capabilities.py
```

entry:

```powershell
python -m probes.probe_phase66_capabilities
```

主要 function:

```text
build_phase66_representative_result()
print_phase66_results()
print_phase66_derivation_chain()
print_phase66_provenance()
print_phase66_literature()
print_phase66_proof_record()
print_phase66_boundary()
main()
```

display order:

```text
Toda Equation (5.8) result
Proof-style derivation
Provenance / integration
Literature statements used
Proof record
Phase 66 completion boundary
```

重要:

```text
print_phase66_derivation_chain()
= presentation-only
```

automatic proof narrative generator ではない。

---

# 30. `docs/proof_records.md`

Phase 66-8 から正式導入。

責務:

```text
representative theorem / equation
human-readable proof-style derivation
machine provenance
literature
GIVEN / INFERENCE boundary
representation boundary
representative probe
regression status
```

最初の正式 record:

```text
Toda Equation (5.8)
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

persistent Proof Repository ではない。

---

# 31. Phase 66 completion 後に最初に見る場所

次の concrete Toda statement / consequence に進む前に:

```text
Toda source material
  statement / proof / locator

toda_rules.py
  Phase 66 Equation (5.8) rule family
  Toda58EquationStatement

tests/test_phase66_*.py
  current sign / Δ / Whitehead boundary

probes/probe_phase66_capabilities.py
  current proof-style / provenance display

docs/proof_records.md
  current representative proof format
```

を確認する。

Proof Repository を実装する場合は別 Phase とし、
Phase 66 の proof record documentation と混同しない。

引き続き:

```text
source statement
↓
dependency analysis
↓
current code / related tests
↓
minimum implementation
```

を維持する。

---

# 32. Phase 67：Toda Lemma 5.7

Phase 67 の target:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
→
E(η₂∘α)=0

特に:
E(η₂∘ν′)=0
Δ(ν₅)=±(η₂∘ν′)
```

production implementation は `toda_rules.py` に theorem-specific minimum semantics を追加し、generic inference engine は変更しない。

## 32.1 `TodaLemma57TwoIota5ImageMembershipStatement`

field:

```text
element
source_group
```

意味:

```text
element ∈ 2ι₅∘source_group
```

Phase 67 concrete use:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
```

generic `ImageMembership` / existential witness / image object は追加しない。

## 32.2 general Lemma 5.7 rule family

```text
toda_lemma57_e2_eta2_alpha_composition_inference_rule()
toda_lemma57_e2_eta2_alpha_zero_inference_rule()
toda_lemma45_n3_suspension_zero_reflection_inference_rule()
```

chain:

```text
E²α image hypothesis
↓
E²(η₂∘α)=η₄∘E²α
+
2η₄=0
↓
E²(η₂∘α)=0
↓
E(η₂∘α)=0
```

concrete `ν′` compatibility のため、`α∈π_i(S³)` の index `i` は `alpha.source` から読む。

symbolic branch:

```text
alpha.source = i
```

concrete ν′ branch:

```text
alpha.source = 6
```

を同じ rule family で扱う。

## 32.3 ν′ hypothesis bridge

```text
toda_lemma57_nu_prime_hypothesis_inference_rule()
```

input:

```text
TodaLemma54Statement                         INFERENCE
TodaNuFamilyDefinitionStatement(n=5)
```

uses:

```text
2Eν₄=E²ν′
ν₅=Eν₄
```

output:

```text
E²ν′ ∈ 2ι₅∘π_8(S⁵)
INFERENCE
```

ν′ 専用に general proof を複製せず、general Lemma 5.7 chain を再利用する。

## 32.4 `π_6^2=Z/4{η₂∘ν′}`

rule:

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule()
```

input:

```text
TodaProp56FiniteDimensionalStatement  INFERENCE
Toda52CompositionIsomorphismStatement INFERENCE
```

uses:

```text
π_6^3=Z/4{ν′}
η₂∘- : π_i^3≅π_i^2
```

output:

```text
π_6^2=Z/4{η₂∘ν′}
INFERENCE
```

concrete transport のみに限定し、generic cyclic-generator transport は追加しない。

## 32.5 `TodaDeltaSurjectiveStatement`

Phase 67-7 で追加した Toda-specific map property:

```text
TodaDeltaSurjectiveStatement
```

field:

```text
map: TodaDeltaMap
```

既存 `TodaDeltaInjectiveStatement` と同じ theorem-specific level で Δ の surjectivity を保持する。

## 32.6 concrete Toda (4.4) exactness

```text
toda_lemma57_concrete_delta_e_exactness_inference_rule()
```

recognizes exactly:

```text
π_8^5 ─Δ→ π_6^2 ─E→ π_7^3
```

and derives:

```text
TodaProp42ExactnessStatement
```

既存 symbolic `toda_prop42_delta_e_exactness_inference_rule()` は変更しない。

## 32.7 Δ surjectivity

```text
toda_lemma57_delta_surjective_inference_rule()
```

input:

```text
E(η₂∘ν′)=0                          INFERENCE
π_6^2=Z/4{η₂∘ν′}                    INFERENCE
concrete Toda (4.4) exactness        INFERENCE
```

output:

```text
TodaDeltaSurjectiveStatement
INFERENCE
```

concrete cyclic target に限定し、generic `generator maps to zero → map zero` solver は追加しない。

## 32.8 `Δ(ν₅)=±(η₂∘ν′)`

```text
toda_lemma57_delta_nu5_generator_inference_rule()
```

input:

```text
Δ surjective                         INFERENCE
π_6^2=Z/4{η₂∘ν′}                    INFERENCE
Toda Proposition 5.6 aggregate      INFERENCE
```

Phase 65 aggregate から:

```text
π_8^5=Z/8{ν₅}
```

を利用する。

canonical `ν₅` validation は:

```text
toda_nu_family_definition_statement(5).element
```

を再利用する。

output:

```text
TodaDeltaImageUpToSignStatement
Δ(ν₅)=±(η₂∘ν′)
```

## 32.9 Phase 67 tests

主要 tests:

```text
tests/test_phase67_lemma57_hypothesis_statement.py
tests/test_phase67_lemma57_first_branch.py
tests/test_phase67_lemma57_n3_zero_reflection.py
tests/test_phase67_lemma57_nu_prime_specialization.py
tests/test_phase67_pi6_2_eta2_nu_prime.py
tests/test_phase67_lemma57_delta_generator.py
tests/test_phase67_lemma57_applicability_provenance.py
tests/test_phase67_probe.py
```

heavy representative builders は必要に応じて:

```python
@lru_cache(maxsize=1)
```

で同一 object graph を再利用する。

Phase 67-8 は production code を変更せず、ancestor reachability / acyclicity / Phase 66 independence を regression で固定する。

## 32.10 representative probe

module:

```text
probes/probe_phase67_capabilities.py
```

entry:

```powershell
python -m probes.probe_phase67_capabilities
```

主要 function:

```text
build_phase67_representative_result()
print_phase67_results()
print_phase67_derivation_chain()
print_phase67_provenance()
print_phase67_source()
print_phase67_proof_record()
print_phase67_boundary()
main()
```

focused end-to-end builder:

```text
build_phase67_7_data()
```

を再利用し、probe 側に theorem inference を複製しない。

`print_phase67_derivation_chain()` は presentation-only。automatic proof narrative generator ではない。

## 32.11 Phase 67 completion regression

```text
Phase 67 probe: 21 passed
repository-wide: 4102 passed in 32.75s
```

---

# 33. Phase 67 completion 後に最初に見る場所

次の concrete Toda statement に進む前に:

```text
Toda source material
  Lemma 5.7 後の statement / proof / locator

toda_rules.py
  Phase 67 Lemma 5.7 rule family
  Delta surjectivity / generator consequence

tests/test_phase67_*.py
  current applicability / provenance boundary

probes/probe_phase67_capabilities.py
  current proof-style / provenance display

docs/proof_records.md
  Toda Lemma 5.7 record
```

Phase 68 は source statement を確認して target を確定する。

