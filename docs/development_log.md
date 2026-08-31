# ehp_proof 開発記録

この文書は Phase 21 完了時点までの開発履歴を、現在の実装と矛盾しない
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
- duplicate rejection
- fixed-point execution
- bounded execution
- per-round tracing
- branch / merge

### 状態

完了

---

# Phase 6：EHP domain inference foundation

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
↓
equality closure / ZERO propagation
↓
FIXED_POINT
```

Phase 6 completion:

```text
691 passed in 22.77s
```

### 状態

完了

---

# Phase 7：Element-order reasoning

```text
ord(α)=n
↓
nα=0
```

Phase 7 completion:

```text
706 passed in 60.22s
```

### 状態

完了

---

# Phase 8：Suspension reasoning

追加:

```text
Suspension(expression)
```

Rules:

```text
x=y → E(x)=E(y)
x=0 → E(x)=0
nα=0 → nE(α)=0
```

Phase 8 completion:

```text
721 passed in 22.16s
```

### 状態

完了

---

# Phase 9：Freudenthal / stable-range reasoning

```text
stable range
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary は epimorphism only。

Phase 9 completion:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 10：Composition reasoning

```text
α∘β=γ
```

を structured equality として扱い、
Suspension-composition functoriality と接続。

Phase 10 completion:

```text
763 passed in 22.32s
```

### 状態

完了

---

# Phase 11：Generalized Hopf-invariant reasoning

```text
H(α)=β
```

の `β` は `Expression`。

Boundary:

```text
H(x)=0
↛
x=0
```

Phase 11 completion:

```text
791 passed in 23.41s
```

### 状態

完了

---

# Phase 12：Additive expression / reasoning

追加:

```text
Sum(left,right)
```

Inverse:

```text
-α = Multiple(-1,α)
```

Phase 12 completion:

```text
809 passed in 62.32s
```

### 状態

完了

---

# Phase 13：Homomorphism reasoning

追加:

```text
MapSymbol
MapApplication
HomomorphismStatement
```

Phase 13 completion:

```text
856 passed in 62.31s
```

### 状態

完了

---

# Phase 14：Set / subgroup reasoning

追加:

```text
MembershipStatement
SubsetStatement
SubgroupEqualityStatement
ImageSubgroupReference
KernelSubgroupReference
```

Phase 14 completion:

```text
921 passed in 62.89s
```

### 状態

完了

---

# Phase 15：Coset / modulo reasoning

追加:

```text
Coset
ModuloStatement
CosetEqualityStatement
```

Phase 15 completion:

```text
956 passed in 64.09s
```

### 状態

完了

---

# Phase 16：Symbolic scalar constraints

追加:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

Representative:

```text
k odd
↓
k≡1 mod 2

ord(β)=2
+
k≡1 mod 2
↓
kβ=β
```

Phase 16 completion:

```text
988 passed in 61.87s
```

### 状態

完了

---

# Phase 17：Indeterminacy

追加:

```text
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

Examples:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Candidate enumeration は行わない。

Phase 17 completion:

```text
tests/test_indeterminacy_rules.py
36 passed
```

```text
full suite
1024 passed in 66.01s
```

### 状態

完了

---

# Phase 18：Toda bracket minimum representation

追加:

```text
TodaBracket
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Bridge:

```text
a∘b=0
b∘c=0
↓
ZERO
↓
{a,b,c} defined
```

Boundary:

```text
definedness
↛
membership
```

```text
membership
↛
exact value
```

Verified:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

### 状態

完了

---

# Phase 19：Toda bracket membership / first theorem bridge

Actual literature-backed notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Phase 19 では bracket index を保持できなかったため:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

を unindexed projection として使用。

追加:

```text
TodaBracketMembershipTheoremStatement
```

Bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

Representative chain:

```text
round 1: defining equalities → ZERO
round 2: ZERO + ZERO → definedness
round 3: theorem fact + definedness → membership
```

Verified:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

```text
full suite
1064 passed in 61.64s
```

### 状態

完了

---

# Phase 20：Indexed unstable Toda notation

Phase 20 は Phase 19 の representation gap:

```text
{η₃,Eν′,ν₇}_1
```

と一般形:

```text
{a,E^t b,E^t c}_t
```

を structural に保持するための最小 extension を実装した。

Phase 20 は基本的に expression / representation layer の Phase。

Toda theorem inference や generic engine は変更しない。

---

## Phase 20 前半：index / indexed data / iterated suspension

既存 `TodaBracket` に optional index を追加し、unindexed API を維持した。

```text
TodaBracket.index
```

により:

```text
{a,b,c}
{a,b,c}_1
{a,b,c}_2
```

を structural に区別可能にした。

Indexed notation の base と exponent を保持するため:

```text
IndexedTodaBracketData
```

を導入。

Fields:

```text
bracket
second_base
third_base
suspension_exponent
```

General iterated suspension のため:

```text
IteratedSuspension
```

を導入。

Concrete / symbolic exponent を同じ structure で扱う。

```text
E^2 α
E^t α
```

No normalization:

```text
IteratedSuspension(α,1)
!=
Suspension(α)
```

```text
IteratedSuspension(α,2)
!=
Suspension(Suspension(α))
```

---

## Phase 20-7：suspension_exponent symbolic extension

`IndexedTodaBracketData.suspension_exponent`:

```text
int
↓
int | ScalarSymbol
```

これにより:

```text
second = E^t b
third  = E^t c
suspension_exponent=t
```

を同じ symbolic scalar で保持可能になった。

Verified:

```text
tests/test_expression.py
53 passed in 1.99s
```

```text
full suite
1087 passed in 68.87s
```

### 状態

完了

---

## Phase 20-8：TodaBracket.index symbolic extension

`TodaBracket.index`:

```text
int | None
↓
int | ScalarSymbol | None
```

これにより:

```text
{a,E^t b,E^t c}_t
```

の末尾 index `t` まで structural に保持可能になった。

Verified:

```text
tests/test_expression.py
57 passed in 1.97s
```

```text
full suite
1091 passed in 71.44s
```

### 状態

完了

---

## Phase 20-9：correspondence representative

Production code は変更せず:

```text
second = E^t(second_base)
third  = E^t(third_base)
bracket.index = suspension_exponent = t
```

を representative regression で固定。

Verified:

```text
tests/test_expression.py
58 passed in 2.19s
```

```text
full suite
1092 passed in 62.37s
```

### 状態

完了

---

## Phase 20-10：is_consistent()

`IndexedTodaBracketData` に:

```text
is_consistent() -> bool
```

を追加。

Checks:

```text
bracket.second
==
IteratedSuspension(second_base,suspension_exponent)

bracket.third
==
IteratedSuspension(third_base,suspension_exponent)

bracket.index
==
suspension_exponent
```

Boundary:

```text
inconsistent data
=
constructible
```

and:

```text
inconsistent data
→
is_consistent() == False
```

Constructor validation は導入しない。

Verified:

```text
tests/test_expression.py
62 passed in 2.57s
```

```text
full suite
1096 passed in 61.37s
```

### 状態

完了

---

## Phase 20-11：concrete consistency representative

Symbolic case と同じ predicate が:

```text
{a,E^2 b,E^2 c}_2
```

でも機能することを固定。

Verified:

```text
tests/test_expression.py
63 passed in 2.24s
```

```text
full suite
1097 passed in 61.99s
```

### 状態

完了

---

## Phase 20-12：representative / boundary regression

Phase 20 全体を final regression で固定。

Representative:

```text
{a,E^t b,E^t c}_t
```

Checks:

```text
second exponent = t
third exponent = t
suspension_exponent = t
bracket.index = t
is_consistent() == True
```

Structural boundary:

```text
E^1 b !=structural E b
E^2 b !=structural E(Eb)
E^t b !=structural E^2 b
```

```text
{a,E^t b,E^t c}_t
!=structural
{a,E^t b,E^t c}_2
```

Inconsistent data:

```text
constructible
+
is_consistent() == False
```

Verified:

```text
tests/test_expression.py
64 passed in 1.46s
```

```text
full suite
1098 passed in 61.30s
```

### 状態

完了

---

# Phase 20 completion boundary

Implemented:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
symbolic iterated exponent
symbolic bracket index
IndexedTodaBracketData.is_consistent()
```

Types:

```text
TodaBracket.index
=
int | ScalarSymbol | None
```

```text
IteratedSuspension.exponent
=
int | ScalarSymbol
```

```text
IndexedTodaBracketData.suspension_exponent
=
int | ScalarSymbol
```

Representative:

```text
{a,E^t b,E^t c}_t
```

Not implemented:

```text
constructor validation
automatic normalization
Suspension ↔ IteratedSuspension auto conversion
general symbolic exponent arithmetic
is_consistent() → theorem applicability
is_consistent() → inference rule
full source / target typing
ambient homotopy-group validation
stable Toda bracket
higher Toda bracket
general theorem quantification
candidate-set algebra
```

Generic inference engine:

```text
unchanged
```

---


# Phase 21：Typed homotopy elements / source-target context

Phase 21 は、actual composition / Toda validity に必要な最小 typing として
source / target context を導入した。

Universal type system、ambient homotopy group、stem、stable context は
先取りしない。

---

## Phase 21-1：source / target minimum representation

`HomotopyElement` に optional fields:

```text
source
target
```

を追加。

Legacy:

```text
HomotopyElement(name, dimension)
```

は維持。

この段階では source / target を structural equality にまだ参加させず、
storage-only boundary を一度固定した。

Verified:

```text
full suite
1101 passed in 27.22s
```

### 状態

完了

---

## Phase 21-2：typed structural equality

`source` / `target` を ordinary dataclass fields として structural equality に参加させた。

Therefore:

```text
α : S^5 → S^3
!=structural
α : S^6 → S^3
```

and:

```text
typed α
!=structural
untyped α
```

Verified:

```text
full suite
1103 passed in 25.61s
```

### 状態

完了

---

## Phase 21-3：Suspension source / target shift

`Suspension` に derived properties:

```text
source
target
```

を追加。

For:

```text
α : S^m → S^n
```

derive:

```text
Eα : S^(m+1) → S^(n+1)
```

Unknown information remains `None`.

Nested ordinary Suspension repeats the shift.

Verified:

```text
full suite
1106 passed in 23.15s
```

### 状態

完了

---

## Phase 21-4：concrete IteratedSuspension shift

`IteratedSuspension` に derived typing を追加。

Concrete non-negative:

```text
E^r α : S^(m+r) → S^(n+r)
```

Symbolic:

```text
E^t α
```

does not create symbolic sphere dimensions.

Negative exponent remains constructible but does not produce concrete typing.

Verified:

```text
full suite
1111 passed in 23.41s
```

### 状態

完了

---

## Phase 21-5：Composition type compatibility predicate

`Composition` に:

```text
is_type_compatible() -> bool
```

を追加。

For:

```text
α : S^m → S^n
β : S^p → S^m
```

checks:

```text
α.source == β.target
```

Supported current typed operands:

```text
HomotopyElement
Suspension
IteratedSuspension
```

No constructor rejection.

Verified:

```text
full suite
1115 passed in 22.76s
```

### 状態

完了

---

## Phase 21-6：mismatch boundary

Production code は変更せず、known mismatch regression を固定。

```text
left.source != right.target
→
is_type_compatible() == False
```

while:

```text
mismatched Composition
=
constructible
```

Unknown typing and known mismatch both remain `False` in the current boolean API.

No three-valued compatibility model.

Verified:

```text
full suite
1117 passed in 24.13s
```

### 状態

完了

---

## Phase 21-7：Toda entry composition compatibility

`TodaBracket` に:

```text
are_defining_compositions_type_compatible()
```

を追加。

Checks displayed compositions:

```text
first∘second
second∘third
```

by reusing `Composition.is_type_compatible()`.

Both must be confirmed compatible.

No Toda definedness rule change.

Verified:

```text
full suite
1121 passed in 23.02s
```

### 状態

完了

---

## Phase 21-8：representative scenario

Production code は変更せず、typed expression chain を integration regression で固定。

Representative dependency:

```text
typed HomotopyElement
↓
Suspension shift
↓
concrete IteratedSuspension shift
↓
Composition compatibility
↓
Toda entry compatibility
```

Separate inference boundary:

```text
type compatibility
↛
ZERO
↛
Toda definedness
```

Verified:

```text
full suite
1123 passed in 22.64s
```

### 状態

完了

---

## Phase 21-9：final regression / boundary

Production code は変更せず、Phase 21 全体の boundary を final regression で固定。

Checks include:

```text
typed structural equality
typed / untyped distinction
Suspension shift
concrete IteratedSuspension shift
symbolic exponent boundary
negative exponent boundary
Composition compatibility
known mismatch
unknown typing
constructible != compatible
Toda both-compatible case
Toda first mismatch
Toda second mismatch
Toda unknown typing
indexed / unindexed structural distinction
```

Verified:

```text
tests/test_expression.py
90 passed in 0.33s
```

```text
tests/test_toda_rules.py
44 passed in 0.73s
```

```text
full suite
1125 passed in 22.75s
```

### 状態

完了

---

# Phase 21 completion boundary

Implemented:

```text
HomotopyElement.source
HomotopyElement.target
typed HomotopyElement structural equality
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Important boundaries:

```text
typed
!=
untyped
```

```text
constructible
!=
type-compatible
```

```text
symbolic E^t
!=
symbolic dimension arithmetic
```

```text
type-compatible
!=
ZERO
```

```text
type-compatible
!=
Toda definedness
```

Not implemented:

```text
constructor typing validation
three-valued compatibility
Composition source / target
symbolic dimension expressions
ambient homotopy-group validation
stem validation
stable / unstable context
Toda definedness typing guard
indexed Toda theorem applicability from typing
structured generator representation
stable homotopy groups
stable Toda brackets
higher Toda brackets
```

Generic inference engine:

```text
unchanged
```

Current verified status:

```text
tests/test_expression.py
90 passed in 0.33s
```

```text
tests/test_toda_rules.py
44 passed in 0.73s
```

```text
full suite
1125 passed in 22.75s
```

---

# Current verified status

```powershell
python -m pytest tests/test_expression.py -q
```

```text
90 passed in 0.33s
```

```powershell
python -m pytest -q
```

```text
1125 passed in 22.75s
```

No failures.

---

# Phase 22 boundary

Natural next candidate:

```text
Phase 22
structured generator representation
```

Purpose:

```text
actual tables / literature notation
```

に必要な generator identity を lossless に保持する。

Potential information:

```text
family
index
decoration
source
target
stable / unstable role
```

Actual source need のない field は先取りしない。

Indexed Toda theorem applicability、stable homotopy、stable Toda notation は後続 layer。

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
chronological history

docs/roadmap.md
=
future capability dependency
```

今後も historical limitation と current limitation を混同しない。
