# EHP Proof Tracer 設計

## 1. 基本設計原則

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule
↓
existing generic inference engine
```

generic engine に数学固有の theorem knowledge を埋め込まない。

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

---

# 3. Expression layer

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

constructors は theorem-aware normalization を行わない。

---

# 4. Scalar-expression layer

Phase 33 で Barratt–Hilton に必要な minimum scalar-expression tree を追加した。

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

`ScalarValue` は integer と symbolic scalar expression を共通に受けるための型として使う。

representable:

```text
p+k
q+h
(p+k)h
ph
(-1)^((p+k)h)
(-1)^(ph)
```

general-purpose CAS ではない。

自動では行わない:

```text
p+k = k+p
ph = hp
(p+k)h = ph+kh
(-1)^2 = 1
```

これらが必要になれば explicit rule として追加する。

---

# 5. Parity and sign semantics

既存:

```text
OddScalarStatement
EvenScalarStatement
ScalarSignEvaluationStatement
```

rules:

```text
n even
↓
(-1)^n=1
```

```text
n odd
↓
(-1)^n=-1
```

重要:

```text
scalar expression structure
↛
automatic parity
```

sign evaluation は proof-level knowledge であり、元の `ScalarPower` を破壊的に整数へ正規化しない。

---

# 6. Multiple with symbolic coefficient

`Multiple.coefficient` は symbolic scalar を保持できる。

```text
(-1)^n a
```

bridge:

```text
(-1)^n=1
↓
(-1)^n a=a
```

```text
(-1)^n=-1
↓
(-1)^n a=-a
```

additive inverse representation:

```text
-a = Multiple(-1,a)
```

を再利用する。

---

# 7. IteratedSuspension

symbolic scalar exponent を保持できる。

```text
E^q a
E^(p+k)b
E^p b
E^(q+h)a
```

current typing boundary:

```text
integer exponent
→ existing source / target shift
```

```text
symbolic exponent
→ source = None
→ target = None
```

Phase 34 で symbolic homotopy-group membership を導入したが、この typing boundary は変更していない。

---

# 8. SmashProduct boundary

`SmashProduct(left,right)` は structural syntax。

未実装:

```text
source / target typing
commutativity theorem
associativity theorem
normalization
general smash-product algebra
```

重要:

```text
SmashProduct(a,b)
↛
Barratt–Hilton RHS
```

Toda Prop.3.1 の正しい applicability premises と theorem rule がある場合にのみ equality が導出される。

---

# 9. Barratt–Hilton structural representation

Phase 33 で Toda Prop.3.1 の2式を structural `RelationType.EQUALITY` として表現可能にした。

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

使用 structures:

```text
SmashProduct
ScalarSum
ScalarProduct
ScalarPower
Multiple
IteratedSuspension
Composition
Relation
```

Phase 33 completion boundary:

```text
structural Relation
!=
theorem-derived ProofStep
```

---

# 10. Phase 34 symbolic homotopy-group membership

Toda Prop.3.1 の applicability を lossless に保持するため、Phase 34 で minimum statement を追加した。

```text
HomotopyGroupMembershipStatement
```

代表:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

conceptual fields:

```text
element
group_dimension
sphere_dimension
```

`group_dimension` / `sphere_dimension` は symbolic scalar structure を保持できる。

重要:

```text
HomotopyGroupMembershipStatement
!=
HomotopyElement.source / target
```

したがって、

```text
a ∈ π_{p+k}(S^p)
```

から自動的に symbolic `source=p+k`, `target=p` を materialize しない。

---

# 11. Toda Prop.3.1 first theorem rule

applicability:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

conclusion:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

これは direct theorem rule であり、generic engine には数学固有知識を追加していない。

strict applicability:

```text
missing a membership
→ reject

missing b membership
→ reject

wrong group dimension
→ reject

wrong sphere dimension
→ reject

wrong element
→ reject
```

available steps に unrelated knowledge があっても、generic matcher が必要な2 premise を選択できる。

---

# 12. Toda Prop.3.1 second theorem rule

同じ applicability premises から:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

を導出する。

first / second は同じ `SmashProduct(a,b)` を左辺に持つが、右辺構造は別物として保持する。

```text
first formula
!=
second formula
```

---

# 13. Literature provenance

Phase 34 では structured literature reference を Barratt–Hilton の derived `Relation.source` に保持する。

source:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

proof trace 上の役割:

```text
ProofStep.premises
=
どの前提から出たか
```

```text
ProofStep.inference_rule
=
どの rule を適用したか
```

```text
Relation.source
=
どの文献定理に基づくか
```

```text
Relation.note
=
first / second formula の識別
```

Phase 24 の Toda bracket membership repository は narrow design のまま維持し、Barratt–Hilton のために universal theorem repository へ一般化していない。

---

# 14. Phase 34 sign evaluation connection

Phase 34 theorem conclusion の RHS は Phase 33 sign machinery と structural に一致する。

first formula:

```text
a∧b
=
(-1)^((p+k)h)X
```

explicit parity:

```text
((p+k)h) is even
```

sign evaluation:

```text
(-1)^((p+k)h)=1
```

Multiple reduction:

```text
(-1)^((p+k)h)X=X
```

generic equality transitivity:

```text
a∧b=(-1)^((p+k)h)X
(-1)^((p+k)h)X=X
↓
a∧b=X
```

odd parity では:

```text
a∧b=-X
```

まで同じ既存 machinery で到達できる。

Barratt–Hilton 専用 sign bridge は追加していない。

---

# 15. Provenance through equality closure

generic equality transitivity が作る final `Relation` に literature source を直接コピーしない。

ただし proof dependency:

```text
final_step
├── theorem_step
│   ├── Toda Prop.3.1 source
│   ├── a membership
│   └── b membership
│
└── reduction_step
    └── sign_step
        └── parity_step
```

を `ProofStep.premises` で追跡できる。

したがって source metadata を conclusion へ重複コピーせず、proof graph を provenance の正本とする。

---

# 16. Phase 34 scope regression

Phase 34 で固定した boundary:

```text
theorem premises なし
↛ Barratt–Hilton equality
```

```text
structural formula itself
↛ theorem applicability
```

```text
Toda Prop.3.1 derivation
↛ automatic parity fact
```

```text
symbolic sign
↛ ±1 without explicit parity
```

```text
symbolic homotopy-group membership
↛ symbolic source / target solving
```

```text
Toda Prop.3.1
↛ actual H calculation
```

```text
Barratt–Hilton
!=
general SmashProduct normalization
```

---

# 17. Toda Prop.2.2 integration

既存:

```text
H(a∘Eb)=H(a)∘Eb
```

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

Phase 34 はこれらを変更しない。

Phase 35+ では特に左公式:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

と Phase 34 Barratt–Hilton theorem rule を actual `H((2ι₂)η₂)` 計算へ接続する予定。

---

# 18. Representative Phase 34 inference

```text
GIVEN
a ∈ π_{p+k}(S^p)

GIVEN
b ∈ π_{q+h}(S^q)

↓ Toda Prop.3.1

a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)

+

GIVEN
((p+k)h) is even

↓
(-1)^((p+k)h)=1

↓
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b

↓ equality transitivity

a∧b
=
E^q a∘E^(p+k)b
```

provenance は theorem branch と sign branch の両方を追跡できる。

---

# 19. Representative probe

```powershell
python -m probes.probe_phase34_capabilities
```

表示内容:

```text
typing premises
Toda Prop.3.1 first formula
Toda Prop.3.1 second formula
literature source
explicit parity
sign evaluation
Multiple reduction
equality transitivity
final reduced equality
full proof dependency
scope boundary
```

probe と pytest の役割:

```text
pytest
=
correctness / regression
```

```text
probe
=
人間が目で追える mathematical capability
```

---

# 20. Testing principle

各 layer で:

1. representation
2. structural distinction
3. applicability
4. invalid-case behavior
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. scope
10. full regression
11. executable probe

を確認する。

---

# 21. Phase 34 verified status

focused:

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

related:

```text
tests/test_phase33_barratt_hilton.py
73 passed
```

```text
tests/test_scalar_rules.py
18 passed
```

```text
tests/test_relation_rules.py
50 passed
```

full suite:

```text
1620 passed in 23.32s
```

No failures.

---

# 22. Phase 34 completion boundary

Phase 34 で完成:

```text
symbolic homotopy-group membership
Toda Prop.3.1 first theorem rule
Toda Prop.3.1 second theorem rule
strict applicability
invalid-case rejection
unrelated-premise tolerance
structured literature provenance
theorem RHS → sign evaluation connection
theorem equality → reduced equality closure
scope / non-goal regression
representative executable probe
final integrated regression
```

未実装:

```text
automatic compound parity inference
general symbolic scalar algebra
general SmashProduct typing / normalization
symbolic suspension source / target arithmetic
Toda (2.1)
actual H((2ι₂)η₂) calculation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 23. 次の設計境界

```text
Phase 35+
actual H((2ι₂)η₂) calculation
```

想定 dependency:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / concrete calculation
4ι₃
```

一方:

```text
H(4η₂)
↓ H homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

最終的に:

```text
H((2ι₂)η₂)=H(4η₂)
↓ existing Injective(H)
(2ι₂)η₂=4η₂
```

Phase 35+ でも actual calculation に必要な最小 representation / fact / directed rule だけを追加し、一般的 symbolic algebra を先取りしない。
