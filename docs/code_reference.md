# EHP Proof Tracer コードリファレンス

この文書は EHP Proof Tracer の主要 Python module と、その責務・主要 class / function・探索方法をまとめる。

対象は **Phase 57 completion 時点**。

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
ι₅
α
β
```

### `GeneratorSymbol`

生成元 family と index を保持する。

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

## ここに追加すべきもの

```text
新しい「式の形」
```

が必要な場合。

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

Phase 57 representative run は 18 round で fixed point に到達。

## ここに追加しないもの

```text
Toda Lemma 5.2
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

Phase 57 でも:

```text
α∈π_i(S³)
β∈π_{i+2}(S³)
γ∈π_{i+2}(S⁴)
```

に利用。

## 主な rule

```text
barratt_hilton_first_inference_rule()
barratt_hilton_second_inference_rule()
```

## 設計上の注意

`HomotopyGroupMembershipStatement` がこの module にある配置は歴史的経緯による。

Phase 57 では移動しない。

将来 concrete need が生じた場合のみ配置変更を検討する。

---

# 10. toda_rules.py

## 役割

Toda 固有の theorem knowledge を置く中心 module。

Phase 57 までは:

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
toda_prop51_finite_dimensional_integration_inference_rule()
toda_52_eta2_composition_isomorphism_inference_rule()
```

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

```text
α∈π_i(S³)
↓
2ι₃∘α=2α
```

### Proposition 2.6 specialization

```text
toda_prop26_lemma52_hopf_bracket_inference_rule()
```

```text
β∈{η₃,2ι₄,Eα}_1
+
required zero compositions
↓
H(β) ∈ -Δ^-1(η₂∘2ι₃)∘E²α
```

### Δ inverse bridge

```text
toda_lemma52_delta_two_eta2_preimage_inference_rule()
```

```text
Δ(ι₅)=±2η₂
↓
Δ^-1(2η₂)=±ι₅
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

### `toda_rules.py` に追加しないもの

```text
generic equality transitivity
generic fixed-point engine
generic scalar normalization
generic Toda-bracket CAS normalization
generic coset algebra
generic sign solver
generic inverse-image solver
```

---

# 11. probes/

## 役割

人間が capability を確認できる代表実行。

probe は:

```text
actual representative GIVEN
+
production inference rules
↓
same-run derived result
```

を組み立てる integration fixture としても使う。

代表:

```text
probes/probe_phase49_capabilities.py
probes/probe_phase50_capabilities.py
probes/probe_phase55_capabilities.py
probes/probe_phase56_capabilities.py
probes/probe_phase57_capabilities.py
```

Phase 57:

```powershell
python -m probes.probe_phase57_capabilities
```

確認:

```text
H(beta)=E^2 alpha derived = True
2 beta relation derived = True
beta membership derived = True
Delta(E^2 alpha)=0 derived = True
all final results are INFERENCE = True
final results are GIVEN = False
fixed point = True
```

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
fixed point
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

completion regression:

```text
2997 passed in 38.45s
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

Phase 55 / 56 / 57 の integration では特に重要。

---

# 15. structural normalization を追加する前の確認

例えば:

```text
2*2-1 → 3
E^1α → Eα
-(order-two element) → element
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

# 16. code_reference.md の更新ルール

毎 Phase 必須ではない。

更新するのは主に:

```text
新規 module を追加した
主要 class family を追加した
module の責務が変わった
重要な end-to-end entry point が増えた
```

場合。

細かな helper をすべて追記しない。

---

# 17. Phase 58 で確認する場所

次 Phase:

```text
Toda (5.3) ν' consequence
```

まず確認:

```text
toda_rules.py
  Phase 57 Lemma 5.2 integration rules

expression.py
  η-family / Composition / Suspension

tests/test_phase57_lemma52_integration.py
  final theorem result representation

probes/probe_phase57_capabilities.py
  representative build pattern

Phase 54 / 55 tests
  η₄, η₅ family bridge
```

Phase 58 では Lemma 5.2 proof chain を再実装せず specialization として利用する。
