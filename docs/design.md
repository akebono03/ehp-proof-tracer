# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の current architecture、semantics、design boundary を記録する。

historical な実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

---

# 1. 基本設計原則

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule
↓
existing generic inference engine
```

generic inference engine に数学固有の theorem knowledge を埋め込まない。

重要な区別:

```text
representation
!=
typing
!=
theorem knowledge
```

```text
structural equality
!=
mathematical equality
```

---

# 2. Layer separation

```text
literature-backed theorem / explicit facts
↓
domain-specific inference rules
↓
generic ProofStep / InferenceRule machinery
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

Phase 45・46 でも generic inference engine は変更していない。

---

# 3. Expression layer

現在の主要 expression:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── WhiteheadProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

constructor は theorem-aware normalization を行わない。

必要な数学的同値は proof-level statement / `Relation` として導出する。

---

# 4. Scalar-expression layer

minimum scalar tree:

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

`ScalarValue` により integer / symbolic scalar expression を共通に扱う。

Phase 45 では:

```text
i+1
i-1
n+1
2n+1
```

を structural scalar expression として保持する。

general-purpose CAS は導入しない。

---

# 5. Symbolic generator index

`GeneratorSymbol.index` は `ScalarValue | None` を受ける。

これにより:

```text
ι_{n-1}
ι_{2n-1}
ι_{2n+1}
```

を structural に保持できる。

同様に `HomotopyElement.dimension` は symbolic `ScalarValue` を保持できる。

ただし `source` / `target` の symbolic typing までは拡張しない。

---

# 6. WhiteheadProduct

production object:

```text
WhiteheadProduct
├── left: Expression
└── right: Expression
```

representative:

```text
[ι_{n-1},ι_{n-1}]
```

重要:

```text
WhiteheadProduct
!= Composition
!= SmashProduct
```

Whitehead-product constructor は zero theorem、nonzero theorem、bilinearity、antisymmetry、typing theorem を持たない。

---

# 7. Whitehead zero / nonzero premise

Phase 43 から:

```text
RelationType.ZERO
RelationType.INEQUALITY
```

を使用する。

zero:

```text
[ι_{n-1},ι_{n-1}] = 0
```

nonzero:

```text
[ι_{n-1},ι_{n-1}] != 0
```

重要:

```text
ZERO
!=
INEQUALITY
```

既存 equality / zero inference rules は relation-type strict のまま。

---

# 8. PrimaryComponent

production object:

```text
PrimaryComponent
├── group_dimension: ScalarValue
├── sphere_dimension: ScalarValue
└── prime: int
```

representative:

```text
π_i(S^n;p)
π_{2n-1}(S^n;2)
π_{2n}(S^{n+1};2)
```

重要:

```text
PrimaryComponent
!= AbelianGroup
!= membership statement
```

---

# 9. TodaPrimaryGroup

production object:

```text
TodaPrimaryGroup
├── group_dimension: ScalarValue
└── sphere_dimension: ScalarValue
```

representative:

```text
π_i^n
π_{i+1}^{n+1}
π_{i+1}^{2n+1}
π_{i-1}^n
```

重要:

```text
TodaPrimaryGroup
!= PrimaryComponent
```

Toda notation を ordinary p-primary group term に constructor-level で変換しない。

---

# 10. FreeCyclicGroup

symbolic group decomposition 用 structural free summand。

```text
FreeCyclicGroup
└── generator: Expression
```

representative:

```text
Z{P(ι_{2n+1})}
Z{α}
```

concrete calculation layer の `GroupComponent` とは別。

```text
FreeCyclicGroup
!= GroupComponent
```

---

# 11. DirectSumGroup

symbolic group decomposition 用。

```text
DirectSumGroup
└── summands:
    tuple[
      FreeCyclicGroup | PrimaryComponent,
      ...
    ]
```

representative:

```text
Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^n;2)
Z{α} ⊕ π_{2n-1}(S^n;2)
```

重要:

```text
DirectSumGroup
!= AbelianGroup
```

---

# 12. PrimaryComponentMembershipStatement

production object:

```text
PrimaryComponentMembershipStatement
├── element: Expression
└── component: PrimaryComponent
```

representative:

```text
Eα ∈ π_{2n}(S^{n+1};2)
```

これは ordinary `HomotopyGroupMembershipStatement` とは別 statement。

重要:

```text
PrimaryComponentMembershipStatement
!= PrimaryComponent
!= HomotopyGroupMembershipStatement
```

---

# 13. Toda Lemma 4.1 odd case

premise:

```text
OddScalarStatement(n)
```

conclusion:

```text
π_{2n-1}^n = π_{2n-1}(S^n;2)
```

rule:

```text
toda_lemma41_odd_case_inference_rule()
```

Whitehead premise は要求しない。

---

# 14. Toda Lemma 4.1 even / Whitehead nonzero case

premises:

```text
EvenScalarStatement(n)
[ι_{n-1},ι_{n-1}] != 0
```

conclusion:

```text
π_{2n-1}^n
=
Z{P(ι_{2n+1})}
⊕
π_{2n-1}(S^n;2)
```

rule:

```text
toda_lemma41_even_nonzero_case_inference_rule()
```

`match_guard` で Whitehead product の symbolic index が同じ `n` に対応することを確認する。

generic matcher の recursive dataclass decomposition は追加しない。

---

# 15. Toda Lemma 4.1 even / Whitehead zero case

premises:

```text
EvenScalarStatement(n)
[ι_{n-1},ι_{n-1}] = 0
```

group conclusion:

```text
π_{2n-1}^n
=
Z{α}
⊕
π_{2n-1}(S^n;2)
```

rule:

```text
toda_lemma41_even_zero_case_inference_rule()
```

α は structural `HomotopyElement(name="α", dimension=2n-1)` として生成する。

---

# 16. α Hopf condition

同じ zero-case premises から:

```text
H(α)=ι_{2n-1}
```

を導出する。

rule:

```text
toda_lemma41_even_zero_h_alpha_inference_rule()
```

canonical actual `H` として `EHP_H_MAP` を使用する。

---

# 17. α suspension-primary condition

同じ zero-case premises から:

```text
Eα ∈ π_{2n}(S^{n+1};2)
```

を導出する。

rule:

```text
toda_lemma41_even_zero_suspension_primary_inference_rule()
```

conclusion は `PrimaryComponentMembershipStatement`。

---

# 18. Multi-result theorem policy

generic `InferenceRule` は 1 rule = 1 conclusion を維持する。

Toda Lemma 4.1 zero case では:

```text
same premises
├── group structure rule
├── H(α) rule
└── Eα primary-membership rule
```

Toda Proposition 4.2 では:

```text
E-H window
→ E-H exactness rule

H-Δ window
→ H-Δ exactness rule

Δ-E window
→ Δ-E exactness rule
```

と domain rule を分ける。

重要:

```text
multi-result mathematical theorem
!=
generic multi-conclusion inference-rule extension
```

---

# 19. Canonical symbolic EHP maps

Phase 45 で symbolic map terms を揃えた。

```text
EHP_E_MAP
→ E

EHP_H_MAP
→ H

EHP_DELTA_MAP
→ Δ
```

これらは `MapSymbol`。

symbolic source / target typing はまだ持たない。

既存 `MapTypingFact` の concrete integer dimensions を Phase 45 では拡張しない。

---

# 20. TodaEHPSequence

Phase 45 の long structural sequence 用。

```text
TodaEHPSequence
├── terms: tuple[TodaPrimaryGroup,...]
└── maps: tuple[MapSymbol,...]
```

invariant:

```text
len(terms) = len(maps) + 1
```

representative:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
```

重要:

```text
TodaEHPSequence
!= EHPSegment
```

`EHPSegment` は repository-backed concrete `AbelianGroup` / `GroupMap` calculation layer。

`TodaEHPSequence` は symbolic theorem representation layer。

また:

```text
TodaEHPSequence
!= exactness theorem
```

sequence object に `is_exact` は置かない。

---

# 21. TodaEHPExactnessWindow

Phase 45-4 で導入。

```text
TodaEHPExactnessWindow
├── source_term: TodaPrimaryGroup
├── middle_term: TodaPrimaryGroup
├── target_term: TodaPrimaryGroup
├── first_map: MapSymbol
└── second_map: MapSymbol
```

目的:

```text
A --f→ B --g→ C
```

を instance-aware に保持する。

representative:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
```

同じ `E-H` map pair でも group terms が異なれば別 structural instance として区別できる。

重要:

```text
TodaEHPExactnessWindow
!= ExactnessStatement
```

and:

```text
window representation
!= exactness theorem
```

---

# 22. Toda Proposition 4.2 E-H exactness

window:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
```

rule:

```text
toda_prop42_e_h_exactness_inference_rule()
```

`match_guard` が:

```text
first_map = E
second_map = H
middle = π_{i+1}^{n+1}
target = π_{i+1}^{2n+1}
```

を確認する。

conclusion:

```text
TodaProp42ExactnessStatement(window)
```

---

# 23. Toda Proposition 4.2 H-Δ exactness

window:

```text
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
```

rule:

```text
toda_prop42_h_delta_exactness_inference_rule()
```

`match_guard` が map order と symbolic dimension structure を確認する。

conclusion:

```text
TodaProp42ExactnessStatement(window)
```

---

# 24. Toda Proposition 4.2 Δ-E exactness

window:

```text
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
```

rule:

```text
toda_prop42_delta_e_exactness_inference_rule()
```

`match_guard` が map order と symbolic dimension structure を確認する。

conclusion:

```text
TodaProp42ExactnessStatement(window)
```

---

# 25. TodaProp42ExactnessStatement

production statement:

```text
TodaProp42ExactnessStatement
└── window: TodaEHPExactnessWindow
```

意味:

```text
the supplied TodaEHPExactnessWindow
is exact by Toda Proposition 4.2
```

重要:

```text
TodaProp42ExactnessStatement
=
instance-aware theorem result
```

異なる `(i,n)` から作られた E-H window は theorem statement として distinct。

`is_exact: bool` は持たない。

statement type 自体が theorem exactness を表す。

---

# 26. Generic ExactnessStatement compatibility

既存 generic:

```text
ExactnessStatement
├── first_map
├── second_map
└── is_exact
```

は map pair の generic exactness を表す。

Phase 45-3 で確認:

```text
E-H
H-Δ
Δ-E
```

の position は区別できる。

しかし:

```text
(i,n) E-H
(j,m) E-H
```

は canonical map pair が同じため、generic `ExactnessStatement` 単体では区別できない。

したがって:

```text
ExactnessStatement
!=
instance-aware Toda theorem result
```

---

# 27. Toda exactness → generic exactness bridge

Phase 45-6 で追加:

```text
toda_prop42_exactness_to_generic_inference_rule()
```

premise:

```text
TodaProp42ExactnessStatement(window)
```

conclusion:

```text
ExactnessStatement(
  first_map=window.first_map,
  second_map=window.second_map,
  is_exact=True,
)
```

bridge は theorem validity を再検査しない。

theorem-specific map / dimension guards は Phase 45-5 の3 rules が担当済み。

重要:

```text
TodaProp42ExactnessStatement
=
authoritative instance-aware theorem knowledge
```

```text
ExactnessStatement
=
generic inference projection
```

generic projection は intentionally instance-lossy。

---

# 28. Existing generic exactness reuse

Phase 45 は generic exactness engine を変更しない。

既存 EHP exactness consequence を bridge 後に再利用する。

代表:

```text
ExactnessStatement(E,H)
→ H∘E = 0

ExactnessStatement(H,Δ)
→ Δ∘H = 0

ExactnessStatement(Δ,E)
→ E∘Δ = 0
```

Phase 45 representative path:

```text
TodaEHPExactnessWindow
↓
TodaProp42ExactnessStatement
↓
ExactnessStatement
↓
EHPZeroCompositionStatement
```

---

# 29. Applicability semantics

Phase 45 の3 theorem rules は同じ premise pattern:

```text
statement_type = TodaEHPExactnessWindow
```

を持つ。

そのため pattern-level candidate search:

```text
find_applicable_inference_rules()
```

では3 rules が候補になり得る。

実際の theorem match は:

```text
find_inference_match()
```

が `match_guard` まで評価して決定する。

したがって:

```text
pattern-level candidate
!=
guard-aware inference match
```

valid E-H / H-Δ / Δ-E window では guard-aware match はそれぞれ1 ruleのみ。

generic candidate search の semantics は変更しない。

---

# 30. Provenance

Toda theorem-derived `ProofStep` は:

```text
rule=ProofRule.INFERENCE
premises=(TodaEHPExactnessWindow step,)
inference_rule=<Toda Prop.4.2 domain rule>
```

を保持する。

generic bridge-derived step は:

```text
premises=(TodaProp42ExactnessStatement step,)
inference_rule=toda_prop42_exactness_to_generic_inference_rule()
```

を保持する。

instance-aware theorem provenance の正本は `ProofStep` graph と `TodaProp42ExactnessStatement`。

---

# 31. Fixed-point behavior

Phase 45 representative:

```text
round 1
3 × TodaProp42ExactnessStatement

round 2
3 × ExactnessStatement

round 3
3 × EHPZeroCompositionStatement

fixed point
```

representative result:

```text
theorem exactness count = 3
generic exactness count = 3
zero composition count = 3
round_count = 3
termination_reason = FIXED_POINT
```

---

# 32. Phase 45 representative probe

```powershell
python -m probes.probe_phase45_capabilities
```

表示:

```text
π_i^n -E→ π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1}
π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1} -Δ→ π_{i-1}^n
π_{i+1}^{2n+1} -Δ→ π_{i-1}^n -E→ π_i^{n+1}
```

Toda theorem exactness:

```text
each of the three windows is exact
```

generic bridge:

```text
E-H exact
H-Δ exact
Δ-E exact
```

existing generic consequences:

```text
H∘E = 0
Δ∘H = 0
E∘Δ = 0
```

---

# 33. Phase 45 testing

focused:

```text
tests/test_phase45_toda_prop42_compatibility.py
17 passed

tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_exactness_compatibility.py
17 passed

tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed

tests/test_phase45_toda_prop42_bridge.py
16 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_ehp_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed
```

full:

```text
2060 passed in 70.48s
```

---

# 34. Phase 45 scope boundary

実装済み:

```text
canonical symbolic E
canonical symbolic H
canonical symbolic Δ
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
E-H exactness rule
H-Δ exactness rule
Δ-E exactness rule
instance-aware exactness
guard-aware applicability
theorem provenance
Toda exactness → generic ExactnessStatement bridge
existing generic zero-composition reuse
three-round fixed-point representative integration
executable probe
full regression
```

未実装:

```text
symbolic map typing solver
general symbolic dimension solver
automatic symbolic image/kernel group construction
instance-aware generic ExactnessStatement
Toda (4.5)
Toda Prop.4.4
Toda Prop.4.4 E injectivity consequence
stable homotopy
general Whitehead algebra
automatic Whitehead zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

---

# 35. ScalarGreaterEqualStatement

Phase 46-2 で追加。

```text
ScalarGreaterEqualStatement
├── left: ScalarValue
└── right: ScalarValue
```

representative:

```text
n ≥ k+2
m ≥ n
```

目的は symbolic inequality premise の structural representation。

重要:

```text
ScalarGreaterEqualStatement
!= inequality solver
```

statement 自体は:

```text
evaluate
is_true
solve
```

を持たない。

numeric truth verification、transitivity、normalization は Phase 46 では導入しない。

---

# 36. TodaIteratedSuspensionMap

Phase 46-3 で追加。

```text
TodaIteratedSuspensionMap
├── exponent: ScalarValue
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

representative:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

structural instance:

```text
exponent = m-n
source_group = π_{n+k}^n
target_group = π_{m+k}^m
```

重要:

```text
TodaIteratedSuspensionMap
!= IteratedSuspension
```

`IteratedSuspension` は element-level expression。

また:

```text
TodaIteratedSuspensionMap
!= MapSymbol
```

constructor は source / target / exponent を保持するだけで、dimension compatibility を判定しない。

---

# 37. Toda45IsomorphismStatement

Phase 46-4 で追加。

```text
Toda45IsomorphismStatement
└── map: TodaIteratedSuspensionMap
```

意味:

```text
the supplied specific iterated-suspension map
is an isomorphism by Toda (4.5)
```

instance-aware theorem result であり、source / target / exponent の異なる map は distinct theorem statement になる。

重要:

```text
TodaIteratedSuspensionMap
!= theorem truth
```

and:

```text
Toda45IsomorphismStatement
!= generic IsomorphismStatement
```

---

# 38. Toda (4.5) theorem rule

rule:

```text
toda_45_isomorphism_inference_rule()
```

premises:

```text
ScalarGreaterEqualStatement(
  left=n,
  right=k+2,
)

ScalarGreaterEqualStatement(
  left=m,
  right=n,
)

TodaIteratedSuspensionMap(
  exponent=m-n,
  source_group=π_{n+k}^n,
  target_group=π_{m+k}^m,
)
```

conclusion:

```text
Toda45IsomorphismStatement(map)
```

`match_guard` で同じ symbolic `n,k,m` が3 premises に接続されていることを確認する。

確認対象:

```text
stable-range rhs = k+2
second inequality rhs = n
source group dimension = n+k
source sphere dimension = n
target group dimension = m+k
target sphere dimension = m
exponent = m-n
```

generic inference engine は変更しない。

---

# 39. Inequality-premise semantics

Toda (4.5) rule は supplied inequality statement の numeric truth を計算しない。

したがって:

```text
ScalarGreaterEqualStatement
=
available theorem/fact premise
```

であり:

```text
Toda applicability guard
!= inequality theorem prover
```

Phase 46 の rule が確認するのは structural correspondence。

general symbolic inequality solver は deferred。

---

# 40. Toda (4.5) applicability / invalid cases

valid instance:

```text
n ≥ k+2
m ≥ n
E^(m-n): π_{n+k}^n → π_{m+k}^m
```

から exactly one:

```text
Toda45IsomorphismStatement
```

を導出。

reject:

```text
missing stable-range premise
missing m ≥ n premise
missing map premise
different n instance
different k instance
different m instance
wrong source shape
wrong target shape
wrong exponent
```

cross-instance mixing を theorem application として許可しない。

---

# 41. Phase 46 provenance and fixed point

derived theorem step:

```text
rule = ProofRule.INFERENCE
premises = (
  n ≥ k+2 step,
  m ≥ n step,
  TodaIteratedSuspensionMap step,
)
inference_rule = toda_45_isomorphism_inference_rule()
```

representative inference:

```text
round 1
1 × Toda45IsomorphismStatement

fixed point
```

result:

```text
theorem isomorphism count = 1
premise count = 3
round_count = 1
termination_reason = FIXED_POINT
```

---

# 42. Generic isomorphism compatibility boundary

existing generic statements:

```text
IsomorphismStatement
└── map: MapSymbol

InjectiveMapStatement
└── map: MapSymbol
```

Phase 46 map:

```text
TodaIteratedSuspensionMap
!= MapSymbol
```

したがって current type boundary では:

```text
Toda45IsomorphismStatement
→ IsomorphismStatement
```

の generic bridge は追加しない。

また:

```text
Toda45IsomorphismStatement
→ InjectiveMapStatement
```

も Phase 46 では追加しない。

重要:

```text
instance-aware Toda theorem
!=
generic MapSymbol property
```

Phase 46 のためだけに generic map-property API を generalize しない。

---

# 43. Phase 46 representative probe

```powershell
python -m probes.probe_phase46_capabilities
```

representative:

```text
n ≥ k+2
m ≥ n

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m}

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m} is isomorphism
```

reports:

```text
theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

---

# 44. Phase 46 testing

focused:

```text
tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_phase46_toda_45_theorem_semantics.py
14 passed

tests/test_phase46_toda_45_applicability_compatibility.py
16 passed

tests/test_phase46_toda_45_probe.py
10 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_map_property_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed
```

full:

```text
2143 passed in 64.31s
```

---

# 45. Phase 46 scope boundary

実装済み:

```text
ScalarGreaterEqualStatement
symbolic n ≥ k+2
symbolic m ≥ n
TodaIteratedSuspensionMap
symbolic m-n exponent
source π_{n+k}^n
target π_{m+k}^m
Toda45IsomorphismStatement
Toda (4.5) theorem rule
guard-aware applicability
invalid-case rejection
cross-instance rejection
theorem provenance
one-round fixed point
representative executable probe
full regression
```

未実装:

```text
general symbolic inequality solver
automatic numeric inequality validation
general symbolic dimension solver
symbolic map typing solver
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
generic injectivity consequence
Toda Proposition 4.4
Toda Proposition 4.4 E injectivity consequence
stable homotopy
general Whitehead algebra
automatic Whitehead zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

---

# 46. 次の設計境界

次は Phase 47 candidate。

対象:

```text
Toda Proposition 4.4
decomposition-isomorphism branch
```

最初に compatibility check を行う。

確認対象:

```text
Toda Prop.4.4 の正確な decomposition statement
TodaPrimaryGroup
PrimaryComponent
PreimageSubgroup
既存 direct-sum representation
必要な instance-aware isomorphism representation
Toda (4.5) との依存関係
後続の E injectivity consequence への境界
```

Phase 47 でも:

```text
actual mathematical need
↓
compatibility check
↓
minimum representation
↓
theorem semantics
↓
existing generic inference where type-compatible
```

を維持する。

Phase 46 の `Toda45IsomorphismStatement` を無理に generic `IsomorphismStatement` へ落とすことは Phase 47 compatibility check より前には行わない。
