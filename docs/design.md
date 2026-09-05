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

Phase 45 でも generic inference engine は変更していない。

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

# 35. 次の設計境界

次は Toda (4.5)。

対象:

```text
n ≥ k+2
のとき

E^(m-n):
π_{n+k}^n
→
π_{m+k}^m

(m ≥ n)
isomorphism
```

実装前に確認する対象:

```text
IteratedSuspension
existing map isomorphism statement
symbolic scalar inequalities
symbolic source / target representation
TodaPrimaryGroup
Toda (4.5) exact statement
```

Phase 46 でも:

```text
actual mathematical need
↓
compatibility check
↓
minimum representation
↓
theorem rule
↓
existing generic inference engine
```

を維持する。

Toda Prop.4.4 は先取りしない。
