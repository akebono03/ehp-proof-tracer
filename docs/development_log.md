# ehp_proof 開発記録

この文書は Phase 9 完了時点までの開発履歴を、現在の実装と矛盾しない
形で整理した改訂版である。

```text
各 Phase の「未実装」「次の課題」
=
その Phase 時点の historical statement
```

current specification は README.md / docs/design.md を優先する。

---

# Phase 1：有限群計算の安定化

- `GroupElement`
- `GroupMap.apply()`
- kernel / image
- finite EHP exactness

### 状態

完了

---

# Phase 2：structured subgroup

- `Subgroup`
- kernel / image subgroup
- subgroup equality
- subgroup generators / abstract structure

```text
Im(f)=Ker(g)
```

を subgroup equality として扱えるようにした。

### 状態

完了

---

# Phase 3：quotient / exact sequence / extension

- `QuotientGroup`
- induced quotient map
- first-isomorphism checks
- `ExactSequenceStep`
- finite extension candidates
- EHP integration

### 状態

完了

---

# Phase 4：presentation-based finitely generated abelian groups

```text
Z^r ⊕ finite torsion
```

へ一般化。

- relation matrix
- integer lattice
- HNF / SNF
- general kernel / image / cokernel
- free / torsion / mixed maps
- presentation-based exactness
- finite-enumeration cross-check

### 状態

完了

---

# Phase 5：Proof / Generic Inference Engine

Phase 5-65 を foundation completion point とする。

主な model:

- `Relation`
- `ProofStep`
- `Proof`
- `LiteratureReference`
- `InferenceRule`
- `PremisePattern`
- `InferenceMatch`
- `PatternVariable`
- `VariableBinding`

推論 engine:

- multiple premises
- exhaustive deterministic matching
- shared bindings
- conclusion builders / patterns
- one-round execution
- duplicate rejection
- fixed-point execution
- bounded execution
- per-round tracing
- branch / merge

### 状態

完了

---

# Phase 6：EHP domain inference foundation

Representative chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
↓
equality closure
↓
ZERO propagation
↓
traceable target relation
↓
FIXED_POINT
```

Generic engine に EHP-specific branch を追加しなかった。

### 状態

完了

---

# Phase 7：Element-order reasoning

```text
ord(α)=n
↓
nα=0
↓
generic equality / ZERO reasoning
```

EHP / ORDER branches が同一 knowledge state で coexist し、provenance が
混線しないことを確認。

Phase 7 completion full suite:

```text
706 passed in 60.22s
```

### 状態

完了

---

# Phase 8：Suspension reasoning

## Phase 8-1

`Suspension(expression)` を導入。

## Phase 8-2

```text
x=y → E(x)=E(y)
```

## Phase 8-3

```text
x=0 → E(x)=0
```

## Phase 8-4

```text
nα=0 → nE(α)=0
```

## Phase 8-5〜8-9

ORDER / EHP branches と Suspension を統合し、generic reasoning への
reconnection と provenance を固定。

## Phase 8-10

Repeated Suspension:

```text
x=0
↓
E(x)=0
↓
E²(x)=0
↓
...
```

により unrestricted fixed-point termination を仮定できないことを仕様化。

Phase 8 completion:

```text
721 passed in 22.16s
```

### 状態

完了

---

# Phase 9：Freudenthal / stable-range reasoning

Phase 9 は actual theorem family として Freudenthal reasoning を追加。

主目的:

```text
suspension-map metadata
↓
range judgement
↓
theorem conclusion
↓
injectivity
↓
reflection
↓
generic relation reasoning
```

Generic engine に Freudenthal-specific branch は追加しない。

---

# Phase 9-1：SuspensionMapStatement

```text
SuspensionMapStatement(
  sphere_dimension,
  stem,
)
```

を導入。

Phase 8 `Suspension(expression)` とは責務を分離。

```text
Suspension(expression)
=
expression structure

SuspensionMapStatement
=
theorem applicability metadata
```

Structural equality / distinct map identity を regression で固定。

### 状態

完了

---

# Phase 9-2：stable / boundary range judgement

Stable:

```text
stem <= sphere_dimension - 2
```

Boundary:

```text
stem == sphere_dimension - 1
```

Outside:

```text
stem >= sphere_dimension
```

を区別。

### 状態

完了

---

# Phase 9-3：stable range → suspension isomorphism

Rule:

```text
freudenthal_stable_isomorphism_inference_rule()
```

```text
stable SuspensionMapStatement
↓
SuspensionIsomorphismStatement
```

Boundary / outside は reject。

Provenance を保持。

### 状態

完了

---

# Phase 9-4：boundary range → suspension epimorphism

Rule:

```text
freudenthal_boundary_epimorphism_inference_rule()
```

```text
boundary SuspensionMapStatement
↓
SuspensionEpimorphismStatement
```

確認:

- boundary → epimorphism
- stable に boundary rule を誤適用しない
- outside → no epimorphism
- stable isomorphism rule と非重複
- provenance 保持

### 状態

完了

---

# Phase 9-5：isomorphism → injectivity → equality reflection

Explicit theorem consequence:

```text
SuspensionIsomorphismStatement(E)
↓
SuspensionInjectiveStatement(E)
```

その後:

```text
Injective(E)
+
SuspensionMapEqualityStatement(E,x,y)
↓
Relation(x,y,EQUALITY)
```

重要な設計:

```text
isomorphism を reflection に直接使わず
一旦 injectivity を導出してから使う
```

Different map は reject。

Two-round chain:

```text
map
↓
isomorphism
↓
injectivity
```

も regression 固定。

### 状態

完了

---

# Phase 9-6：injectivity → ZERO reflection

```text
Injective(E)
+
SuspensionMapZeroStatement(E,x)
↓
Relation(x,Zero(),ZERO)
```

Different map は reject。

Conclusion は generic ZERO Relation。

Completion:

```text
tests/test_stable_rules.py: 26 passed
full suite: 747 passed
```

### 状態

完了

---

# Phase 9-7：stable range → ZERO reflection fixed-point integration

Initial:

```text
SuspensionMapStatement(E)
SuspensionMapZeroStatement(E,x)
```

Rules:

```text
stable → isomorphism
isomorphism → injectivity
injectivity + E(x)=0 → x=0
```

Productive rounds:

```text
Round 1: isomorphism
Round 2: injectivity
Round 3: x=0
```

その後 genuine:

```text
FIXED_POINT
```

Provenance chain を同時に確認。

Completion:

```text
27 stable-rule tests
748 passed in 22.21s
```

### 状態

完了

---

# Phase 9-8：representative scenario + generic reasoning + provenance

Initial:

```text
stable map E
E(x)=E(y)
E(x)=0
```

Freudenthal:

```text
stable
↓
isomorphism
↓
injectivity
```

Reflection:

```text
injectivity + E(x)=E(y)
↓
x=y
```

```text
injectivity + E(x)=0
↓
x=0
```

Generic reasoning:

```text
x=y
↓
y=x
```

```text
x=0
+
y=x
↓
y=0
```

Phase 9 theorem facts が generic Relation に戻り、既存 equality symmetry /
transitivity / ZERO propagation と同一 fixed-point run で動くことを確認。

Provenance:

```text
map
↓
isomorphism
↓
injectivity
├───────────────┐
↓               ↓
x=y             x=0
↓
y=x
└───────┬───────┘
        ↓
       y=0
```

Completion:

```text
28 stable-rule tests
749 passed in 22.47s
```

### 状態

完了

---

# Phase 9-9：inference-scope / termination / theorem-boundary

Stable / boundary / outside maps を同一 run に投入。

Stable:

```text
stem <= sphere_dimension - 2
→ isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary:

```text
stem == sphere_dimension - 1
→ epimorphism only
```

Boundary から isomorphism / injectivity / reflection を導出しない。

Outside:

```text
stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

Different maps の premises を混同しない。

Termination:

```text
3 productive rounds
↓
FIXED_POINT
```

Phase 9-9 focused test:

```text
1 passed in 0.13s
```

Phase 9 suite:

```text
29 passed in 0.11s
```

Full suite:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 9 completion summary

Architecture progression:

```text
Phase 5
Generic inference engine
        ↓
Phase 6
EHP-derived generic relations
        ↓
Phase 7
ORDER-derived generic relations
        ↓
Phase 8
Suspension transformation
        ↓
Phase 9
Freudenthal theorem reasoning
        ↓
injectivity reflection
        ↓
generic equality / ZERO reasoning
        ↓
traceable fixed-point conclusion
```

Phase 9 principal vertical slice:

```text
SuspensionMapStatement
↓
stable-range theorem
↓
SuspensionIsomorphismStatement
↓
SuspensionInjectiveStatement
↓
SuspensionMapEquality / SuspensionMapZero
↓
generic EQUALITY / ZERO
↓
generic relation reasoning
↓
derived relation
```

成果:

1. theorem metadata と expression representation を分離。
2. stable / boundary / outside を明示。
3. stable → isomorphism。
4. boundary → epimorphism。
5. isomorphism → explicit injectivity。
6. injectivity → equality reflection。
7. injectivity → ZERO reflection。
8. reflection conclusions は generic Relation。
9. generic equality / ZERO reasoning へ再接続。
10. representative branch / merge scenario。
11. end-to-end provenance。
12. map premise cross-contamination 防止。
13. theorem boundary regression。
14. genuine FIXED_POINT。
15. generic engine 無改変。

### 状態

完了

---

# Phase 9 completion tests

```powershell
python -m pytest tests/test_stable_rules.py::test_phase9_inference_scope_termination_and_theorem_boundary -v
```

```text
1 passed in 0.13s
```

```powershell
python -m pytest tests/test_stable_rules.py -v
```

```text
29 passed in 0.11s
```

```powershell
python -m pytest -v
```

```text
750 passed in 22.66s
```

No failures.

---

# Phase 9 completion boundary

Phase 9 で実装しないもの:

```text
automatic suspension-map discovery
automatic sphere-dimension / stem extraction
general dimension validation
epimorphism → preimage / lifting reasoning
surjectivity witnesses
inverse-map construction
general desuspension
canonical E^n normalization
theorem-aware expression equality
Hopf invariant theorem family
Toda composition relations
Toda brackets
Steenrod operations
double EHP
odd-primary-specific theorem families
```

Boundary epimorphism は current theorem conclusion として保持するだけで、
element-level lifting / preimage reasoning へはまだ接続しない。

---

# Phase 10 boundary

Phase 10 も speculative generic-engine work から開始しない。

候補:

- Hopf invariant relations
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- future epimorphism / preimage reasoning

基本原則:

```text
new mathematical theorem
=
new domain InferenceRule
```

actual theorem が current rule language で正しく表現できないと実証された
場合のみ generic engine を変更する。

---

# Current verified status

At Phase 9 completion:

```text
full suite: 750 passed in 22.66s
Phase 9 suite: 29 passed
Phase 9 boundary focused test: 1 passed
```

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
```

今後も historical limitation と current limitation を混同しない。
