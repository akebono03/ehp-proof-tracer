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

Phase 44 でも generic inference engine は変更していない。

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

必要な数学的同値は proof-level `Relation` として導出する。

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

Phase 44 では:

```text
n-1
2n-1
2n
2n+1
n+1
```

を structural scalar expression として保持する。

general-purpose CAS は導入しない。

---

# 5. Symbolic generator index

Phase 44 では Toda Lemma 4.1 の symbolic Whitehead premise が必要になったため `GeneratorSymbol.index` は `ScalarValue | None` を受ける。

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
π_{2n-1}^n
```

重要:

```text
TodaPrimaryGroup
!= PrimaryComponent
```

Toda notation を ordinary p-primary group term に constructor-level で変換しない。

---

# 10. FreeCyclicGroup

Phase 44 の group decomposition に必要な structural free summand。

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

Phase 44 の symbolic group decomposition 用。

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

これは symbolic theorem conclusion 用 structural group term であり、concrete computation を担わない。

---

# 12. PrimaryComponentMembershipStatement

Phase 44-6b で導入。

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

という3本の domain rule で表現する。

重要:

```text
multi-result mathematical theorem
!=
generic multi-conclusion inference-rule extension
```

---

# 19. Structural α identity

group rule、Hopf rule、suspension-primary rule の `α` は同じ structural value として生成する。

test では Python object identity `is` ではなく structural equality `==` を要求する。

これは same structural witness syntax を意味するが、general existential witness engine を意味しない。

---

# 20. Applicability policy

```text
n odd
→ odd rule only
```

```text
n even
+
matching [ι_{n-1},ι_{n-1}] != 0
→ nonzero rule only
```

```text
n even
+
matching [ι_{n-1},ι_{n-1}] = 0
→ zero group rule
```

zero theorem bundle は同じ premises から3 rule が applicable。

異なる symbolic index や arbitrary ZERO / INEQUALITY relation は match しない。

---

# 21. Provenance

derived `ProofStep` は:

```text
rule=ProofRule.INFERENCE
premises=(...)
inference_rule=<domain rule>
```

を保持する。

group conclusion と α conditions の provenance の正本は `ProofStep` graph。

---

# 22. Fixed-point behavior

```text
odd
→ 1 new group conclusion
→ fixed point
```

```text
even nonzero
→ 1 new group conclusion
→ fixed point
```

```text
even zero primary group case
→ 1 new group conclusion
→ fixed point
```

zero theorem bundle:

```text
group rule
Hopf rule
suspension-primary rule
↓
1 round
↓
3 new steps
↓
fixed point
```

---

# 23. Phase 44 representative probe

```powershell
python -m probes.probe_phase44_capabilities
```

表示:

```text
n odd
→ π_{2n-1}^n = π_{2n-1}(S^n;2)
```

```text
n even + Whitehead nonzero
→ π_{2n-1}^n = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^n;2)
```

```text
n even + Whitehead zero
→ π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)

H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

---

# 24. Phase 44 testing

focused:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_phase43_toda_lemma41_premise.py
32 passed

tests/test_phase39_primary_component.py
24 passed

tests/test_hopf_rules.py
31 passed

tests/test_expression.py
145 passed
```

full:

```text
1957 passed in 75.54s
```

---

# 25. Phase 44 scope boundary

実装済み:

```text
symbolic generator index
symbolic HomotopyElement dimension
FreeCyclicGroup
DirectSumGroup
PrimaryComponentMembershipStatement
Toda Lemma 4.1 odd case
Toda Lemma 4.1 even/nonzero case
Toda Lemma 4.1 even/zero group case
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
case applicability
provenance
fixed-point representative integration
executable probe
```

未実装:

```text
automatic Whitehead-product zero inference
automatic Whitehead-product nonzero inference
ZERO / INEQUALITY contradiction detection
Whitehead-product bilinearity
Whitehead-product antisymmetry
automatic α existence
automatic α uniqueness
general existential quantification / witness objects
PrimaryComponent membership → ordinary membership bridge
Toda Prop.4.2
Toda (4.5)
Toda Prop.4.4
stable homotopy
higher Toda brackets
```

---

# 26. 次の設計境界

次は Toda Proposition 4.2。

実装前に確認する対象:

```text
current EHP exactness representation
PrimaryComponent
TodaPrimaryGroup
existing E / H / P map symbols
Toda Prop.4.2 exact statement
```

次 Phase でも actual mathematical need → minimum representation → explicit theorem rule → existing generic engine を維持する。

Toda (4.5)、Toda Prop.4.4、general Whitehead algebra は先取りしない。
