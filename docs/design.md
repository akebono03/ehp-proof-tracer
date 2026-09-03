# EHP Proof Tracer Design

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

# 4. Phase 33 scalar-expression layer

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

Phase 33 は general-purpose CAS ではない。

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

Phase 16 由来の:

```text
OddScalarStatement
EvenScalarStatement
```

は Phase 33 で compound `ScalarValue` を保持できる。

追加:

```text
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

また sign evaluation は proof-level knowledge であり、元の `ScalarPower` を破壊的に整数へ正規化しない。

---

# 6. Multiple with symbolic coefficient

`Multiple.coefficient` は `ScalarValue` を受ける。

```text
(-1)^n a
```

を structural に保持可能。

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

既存 additive inverse representation:

```text
-a = Multiple(-1,a)
```

を再利用する。

---

# 7. IteratedSuspension

Phase 33 では symbolic scalar exponent を保持できる。

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

symbolic source / target arithmetic は Phase 33 の scope 外。

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
composition expression
```

---

# 9. Barratt–Hilton formula structural representation

Phase 33 で Toda Prop.3.1 の2式を structural `RelationType.EQUALITY` として表現可能になった。

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

重要:

```text
structural Relation
!=
theorem-derived ProofStep
```

専用 `BarrattHiltonStatement` は追加しない。既存 `RelationType.EQUALITY` で conclusion shape を十分表現できるため。

---

# 10. Phase 34 boundary

Phase 33 は prerequisite layer。

未実装:

```text
a,b,p,q,k,h
↓ Toda Prop.3.1
Barratt–Hilton equality
```

これは Phase 34 で explicit literature-backed theorem rule として追加する。

Phase 34 でも:

```text
Barratt–Hilton
!=
general smash-product normalization
```

を維持する。

---

# 11. Toda Prop.2.2 integration

既存:

```text
H(a∘Eb)=H(a)∘Eb
```

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

Phase 33 の追加はこれらを変更しない。

generic inference engine も変更していない。

---

# 12. Representative Phase 33 inference

```text
GIVEN
(p+k)h is even

↓
Even exponent evaluates minus-one power to one

(-1)^((p+k)h)=1

↓
Evaluated symbolic sign applies to multiple

(-1)^((p+k)h)(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b
```

provenance は `ProofStep.premises` に保持する。

---

# 13. Scope regression

Phase 33 では次を固定する:

```text
ScalarSum not implicitly commutative
ScalarProduct not implicitly commutative
no distributive normalization
no constant folding
no automatic compound parity
no automatic sign evaluation without parity fact
no automatic signed-sum simplification
SmashProduct not implicitly commutative
no SmashProduct typing
no SmashProduct → Barratt–Hilton conversion
no symbolic suspension typing
Relation object is not itself a ProofStep
```

これらは mathematical impossibility ではなく implementation scope の明示である。

---

# 14. Toda (2.1) boundary

将来候補:

```text
a∘(b₁±b₂)=a∘b₁±a∘b₂
```

```text
(a₁±a₂)∘Eb=a₁∘Eb±a₂∘Eb
```

```text
k(a∘b)=a∘(kb)
```

```text
k(a∘Eb)=(ka)∘Eb
```

Phase 33 では未導入。actual proof need が現れた時点で staged / directed rule として検討する。

---

# 15. Testing principle

各 layer で:

1. representation
2. structural distinction
3. validity / applicability
4. invalid case
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. termination / scope
10. full regression
11. human-readable executable probe

を確認する。

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

# 16. Phase 33 verified status

```text
tests/test_phase33_barratt_hilton.py
73 passed in 0.31s
```

```text
full suite
1585 passed in 23.09s
```

No failures.

---

# 17. Next design boundary

```text
Phase 34
Toda Prop.3.1 Barratt–Hilton theorem rule
```

Phase 34 should reuse Phase 33 syntax and add only theorem applicability / theorem-derived equality needed by the literature-backed result.

Do not pre-add general scalar CAS, general smash algebra, symbolic typing solvers, or actual `H((2ι₂)η₂)` evaluation unless a concrete Phase 34 requirement proves them necessary.
