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

結果:

```text
6 passed
1518 passed full suite
```

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

結果:

```text
18 passed Phase 33
1530 passed full suite
```

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

結果:

```text
30 passed Phase 33
1542 passed full suite
```

### 状態

完了

---

## Phase 33-4：symbolic sign → Multiple / Sum

`Multiple.coefficient` を symbolic scalar 対応へ拡張。

bridge:

```text
(-1)^n=1 → (-1)^n a=a
(-1)^n=-1 → (-1)^n a=-a
```

結果:

```text
1552 passed full suite
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

結果:

```text
48 passed Phase 33
1560 passed full suite
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

結果:

```text
58 passed Phase 33
1570 passed full suite
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

結果:

```text
72 passed Phase 33
1584 passed full suite
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

probe で確認:

```text
formula is Relation: True
formula is ProofStep: False
symbolic exponent source = None
symbolic exponent target = None
```

結果:

```text
72 passed Phase 33
1584 passed full suite
```

### 状態

完了

---

## Phase 33-9：final regression

代表仕様を1本で統合確認。

```text
Barratt–Hilton 2 formula structure
symbolic scalar tree
symbolic IteratedSuspension
explicit parity fact
sign evaluation
Multiple bridge
provenance
scope boundary
```

最終結果:

```text
tests/test_phase33_barratt_hilton.py
73 passed in 0.31s
```

```text
full suite
1585 passed in 23.09s
```

No failures.

### 状態

完了

---

## Phase 33-10：Phase 33 完了整理

Phase 33 で完成:

```text
minimum symbolic scalar-expression tree
symbolic IteratedSuspension exponents
explicit parity → sign evaluation
sign evaluation → Multiple bridge
Barratt–Hilton 2 formula structural representation
scope / non-goal regression
human-readable representative probe
```

generic inference engine:

```text
変更なし
```

final verified status:

```text
73 passed Phase 33 focused suite
1585 passed full suite
```

### 状態

完了

---

# Phase 33 completion boundary

実装済み:

```text
ScalarExpression / ScalarValue
ScalarSum / ScalarProduct / ScalarPower
compound parity statements
ScalarSignEvaluationStatement
parity → sign evaluation
symbolic Multiple coefficient
sign evaluation → Multiple equality
symbolic IteratedSuspension exponent
Barratt–Hilton 2 formula structural Relation
representative probe
```

未実装:

```text
automatic compound parity inference
general symbolic scalar algebra
scalar normalization
SmashProduct typing
SmashProduct algebra / normalization
symbolic suspension source / target arithmetic
Toda (2.1)
Toda Prop.3.1 theorem inference
actual H((2ι₂)η₂) calculation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

---

# 次の Phase

```text
Phase 34
Toda Prop.3.1 Barratt–Hilton theorem rule
```

Phase 34 では Phase 33 の syntax を再利用し、literature-backed theorem inference のみを必要最小限で追加する。

目標 conclusion:

```text
a∧b=(-1)^((p+k)h)(E^q a∘E^(p+k)b)
```

```text
a∧b=(-1)^(ph)(E^p b∘E^(q+h)a)
```

Phase 34 では general smash-product algebra や actual H calculation を先取りしない。
