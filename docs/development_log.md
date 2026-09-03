# ehp_proof 開発記録

current specification は README.md / docs/design.md を優先する。

---

# Phase 1–27 概要

Phase 1–17 で abelian-group calculation、generic inference、EHP、ORDER、Suspension、Freudenthal、Composition、Hopf invariant、additive / homomorphism / subgroup / modulo / symbolic scalar / indeterminacy reasoning を整備。

Phase 18–27 で unstable Toda bracket、indexed notation、typed homotopy elements、structured generators、theorem / generator facts、actual η₃ / ν′ / ν₇ typing、および actual ε₃ Toda chain を実装。

代表:

```text
η₃∘Eν′=0
ν′∘ν₆=0
Eν₆=ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
↓
ε₃∈{η₃,Eν′,ν₇}_1
```

### 状態

完了

---

# Phase 28：map-property equality reflection

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

# Phase 29：actual H facts / typing

production `H` identity、typing、isomorphism fact を既存 map-property machinery に接続。

```text
actual Isomorphism(H)
↓
Injective(H)
```

### 状態

完了

---

# Phase 30：Toda Prop.2.2 right

```text
H(a∘Eb)=H(a)∘Eb
```

を direct theorem rule として実装。

### 状態

完了

---

# Phase 31：SmashProduct minimum representation

```text
a∧b
c∧c
E(c∧c)
```

を structural に表現可能にした。

```text
representation
!=
typing
!=
Barratt–Hilton theorem knowledge
```

### 状態

完了

---

# Phase 32：Toda Prop.2.2 left

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

を direct theorem rule として実装。

Phase 32 completion:

```text
1512 passed in 63.58s
```

### 状態

完了

---

# Phase 33：Barratt–Hilton prerequisite minimum representation

目的:

Toda Prop.3.1 を theorem rule として導入する前に、formula を lossless に保持する syntax と minimum sign machinery を整える。

---

## Phase 33-1：representability check

不足を確認:

```text
p+k
q+h
(p+k)h
ph
(-1)^((p+k)h)
(-1)^(ph)
```

`ScalarSymbol("p+k")` では構造を失うため不可。

### 状態

完了

---

## Phase 33-2：minimum scalar-expression representation

追加:

```text
ScalarExpression
ScalarValue
ScalarSum
ScalarProduct
ScalarPower
```

`IteratedSuspension.exponent` を symbolic scalar expression 対応へ拡張。

### 状態

完了

---

## Phase 33-3：parity fact / sign evaluation

追加:

```text
ScalarSignEvaluationStatement
```

```text
n even → (-1)^n=1
n odd  → (-1)^n=-1
```

compound scalar を parity statement に保持できるが、automatic parity solver は追加しない。

### 状態

完了

---

## Phase 33-4：symbolic sign → Multiple

`Multiple.coefficient` を symbolic scalar 対応へ拡張。

bridge:

```text
(-1)^n=1 → (-1)^n a=a
(-1)^n=-1 → (-1)^n a=-a
```

### 状態

完了

---

## Phase 33-5：IteratedSuspension compatibility regression

production code 変更なし。

固定:

```text
E^q a
E^(p+k)b
E^p b
E^(q+h)a
```

symbolic exponent typing boundary:

```text
source=None
target=None
```

### 状態

完了

---

## Phase 33-6：Barratt–Hilton formula minimum statement representation

production code 変更なし。

```text
a∧b=(-1)^((p+k)h)(E^q a∘E^(p+k)b)
```

```text
a∧b=(-1)^(ph)(E^p b∘E^(q+h)a)
```

を structural `Relation` として保持。

```text
formula representation
!=
theorem inference
```

### 状態

完了

---

## Phase 33-7：scope / non-goal regression

固定:

```text
no scalar automatic commutativity
no distributivity
no constant folding
no automatic compound parity
no automatic SmashProduct conversion
no SmashProduct typing
no symbolic suspension typing
Relation != ProofStep
```

### 状態

完了

---

## Phase 33-8：representative probe

追加:

```text
probes/probe_phase33_capabilities.py
```

代表 proof fragment:

```text
((p+k)h) is even
↓
(-1)^((p+k)h)=1
↓
(-1)^((p+k)h)(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b
```

### 状態

完了

---

## Phase 33-9：final regression

代表仕様を1本で統合確認。

### 状態

完了

---

## Phase 33-10：Phase 33 完了整理

final verified status:

```text
73 passed Phase 33 focused suite
1585 passed full suite
```

### 状態

完了

---

# Phase 34：Toda Prop.3.1 Barratt–Hilton theorem rule

目的:

Phase 33 で表現可能になった Barratt–Hilton 2 formula を、Toda Prop.3.1 の literature-backed theorem knowledge から `ProofStep` として導出できるようにする。

目標:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓
Toda Prop.3.1
↓
Barratt–Hilton equality
```

---

## Phase 34-1：applicability representation check

既存 representation を確認。

確認結果:

```text
concrete a ∈ π_m(S^n)
→ HomotopyElement source / target で表現可能
```

```text
p+k, q+h
→ ScalarSum で表現可能
```

一方:

```text
symbolic
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

を theorem applicability premise として lossless に保持する専用構造は未実装だった。

既存 `MembershipStatement` は:

```text
Subgroup
ImageSubgroupReference
KernelSubgroupReference
```

への membership であり、homotopy-group membership ではないことも確認。

production code 変更なし。

結果:

```text
9 passed Phase 34 focused
1594 passed full suite
```

### 状態

完了

---

## Phase 34-2：Barratt–Hilton first theorem rule

追加:

```text
HomotopyGroupMembershipStatement
```

representable:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

追加:

```text
barratt_hilton_first_inference_rule()
```

conclusion:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

Phase 33 では structural `Relation` だった formula が、この Phase で theorem-derived `ProofStep` になった。

結果:

```text
12 passed Phase 34 focused
1597 passed full suite
```

### 状態

完了

---

## Phase 34-3：first rule applicability / invalid cases

production code 変更なし。

固定:

```text
missing a membership
→ reject

missing b membership
→ reject

wrong a group dimension
→ reject

wrong a sphere dimension
→ reject

wrong b group dimension
→ reject

wrong b sphere dimension
→ reject

wrong element
→ reject
```

generic matcher の仕様として:

```text
correct a membership
correct b membership
unrelated knowledge
→ required 2 premises を選択して accept
```

を確認。

結果:

```text
19 passed Phase 34 focused
1604 passed full suite
```

### 状態

完了

---

## Phase 34-4：second theorem rule

追加:

```text
barratt_hilton_second_inference_rule()
```

同じ applicability premises:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

から:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

を theorem-derived `ProofStep` として導出。

first / second は別 rule、別 conclusion として共存。

結果:

```text
22 passed Phase 34 focused
1607 passed full suite
```

### 状態

完了

---

## Phase 34-5：provenance / theorem reference

structured literature provenance を追加。

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

first / second の derived `Relation.source` に共通 reference を保持。

proof trace:

```text
ProofStep.premises
→ applicability premises

ProofStep.inference_rule
→ theorem rule identity

Relation.source
→ literature source

Relation.note
→ first / second formula
```

既存 theorem repository は generalize せず、Barratt–Hilton rule 内で `Relation.source` を利用。

結果:

```text
1610 passed full suite
```

### 状態

完了

---

## Phase 34-6：sign evaluation connection

production code 変更なし。

Phase 34 theorem RHS と Phase 33 sign machinery が structural に直接接続できることを確認。

代表:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)

+

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

odd parity では additive inverse へ reduction。

Barratt–Hilton 専用 sign bridge は追加しなかった。

結果:

```text
29 passed Phase 34 focused
1614 passed full suite
```

### 状態

完了

---

## Phase 34-7：scope / non-goal regression

production code 変更なし。

固定:

```text
SmashProduct syntax alone
↛ Barratt–Hilton theorem equality
```

```text
Barratt–Hilton equality itself
↛ theorem applicability
```

```text
Toda Prop.3.1 theorem derivation
↛ automatic parity fact
```

```text
symbolic sign
↛ ±1 without explicit parity
```

```text
symbolic homotopy membership
↛ symbolic source / target solver
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

結果:

```text
34 passed Phase 34 focused
1619 passed full suite
```

### 状態

完了

---

## Phase 34-8：representative probe

追加:

```text
probes/probe_phase34_capabilities.py
```

表示 chain:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓
Toda Prop.3.1
↓
a∧b=(-1)^((p+k)h)(E^q a∘E^(p+k)b)
↓
((p+k)h) is even
↓
(-1)^((p+k)h)=1
↓
signed Multiple reduction
↓
equality transitivity
↓
a∧b=E^q a∘E^(p+k)b
```

さらに表示:

```text
source = Toda Prop.3.1
locator = Proposition 3.1
theorem result is ProofStep = True
final result is ProofStep = True
symbolic suspension source/target = None
actual H calculation = outside Phase 34
```

結果:

```text
34 passed Phase 34 focused
1619 passed full suite
```

### 状態

完了

---

## Phase 34-9：final regression

production code 変更なし。

Phase 34 全体を1本で統合確認:

```text
membership
→ first theorem
→ second theorem
→ literature provenance
→ explicit parity
→ sign evaluation
→ Multiple reduction
→ equality transitivity
→ reduced equality
→ scope boundary
```

結果:

```text
35 passed Phase 34 focused
1620 passed full suite
```

### 状態

完了

---

## Phase 34-10：Phase 34 完了整理

Phase 34 で完成:

```text
HomotopyGroupMembershipStatement
first Toda Prop.3.1 theorem rule
second Toda Prop.3.1 theorem rule
strict applicability
invalid-case rejection
unrelated-premise tolerance
structured Toda Prop.3.1 provenance
Phase 33 sign machinery connection
generic equality transitivity closure
scope / non-goal regression
representative executable probe
final representative regression
```

generic inference engine:

```text
変更なし
```

Phase 34 completion status:

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

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

```text
full suite
1620 passed in 23.32s
```

No failures.

### 状態

完了

---

# Phase 34 completion boundary

実装済み:

```text
symbolic homotopy-group membership
Toda Prop.3.1 first / second theorem rules
theorem applicability
literature provenance
sign evaluation connection
generic equality closure
scope boundary
representative probe
final regression
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
```

---

# 次の Phase

```text
Phase 35+
actual H((2ι₂)η₂) calculation
```

想定:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / concrete reasoning
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

よって:

```text
H((2ι₂)η₂)=H(4η₂)
↓
existing Injective(H)
↓
(2ι₂)η₂=4η₂
```

Phase 35+ では、この actual calculation に必要な concrete facts / typing / directed algebra rules だけを追加する。
