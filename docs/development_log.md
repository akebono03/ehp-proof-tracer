# ehp_proof 開発記録

この文書は Phase 22 完了時点までの開発履歴を、現在の実装と矛盾しない
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

追加:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
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

Boundary:

```text
IteratedSuspension
!=
ordinary Suspension normalization
```

```text
suspension exponent
!=
bracket index
```

```text
is_consistent()
!=
theorem applicability
```

Verified Phase 20 completion:

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

# Phase 21：Typed homotopy elements / source-target context

Phase 21 は actual composition / Toda validity に必要な最小 typing として
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

### 状態

完了

---

## Phase 21-2：typed structural equality

`source` / `target` を structural equality に参加させた。

```text
α : S^5 → S^3
!=structural
α : S^6 → S^3
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

```text
α : S^m → S^n
↓
Eα : S^(m+1) → S^(n+1)
```

### 状態

完了

---

## Phase 21-4：concrete IteratedSuspension shift

Concrete non-negative:

```text
E^r α : S^(m+r) → S^(n+r)
```

Symbolic exponent does not create symbolic sphere dimensions.

Negative exponent remains constructible but has no concrete typing.

### 状態

完了

---

## Phase 21-5：Composition type compatibility predicate

追加:

```text
Composition.is_type_compatible()
```

Checks:

```text
left.source == right.target
```

No constructor rejection.

### 状態

完了

---

## Phase 21-6：mismatch boundary

Known mismatch:

```text
False
```

but mismatched Composition remains constructible.

Unknown typing and known mismatch both use the current boolean `False`.

### 状態

完了

---

## Phase 21-7：Toda entry composition compatibility

追加:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

Checks:

```text
first∘second
second∘third
```

No Toda definedness rule change.

### 状態

完了

---

## Phase 21-8：representative scenario

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

### 状態

完了

---

## Phase 21-9：final regression / boundary

Final regression fixed:

```text
typed != untyped
symbolic E^t → no concrete dimensions
negative exponent → no concrete dimensions
known mismatch → False
unknown typing → False
mismatch remains constructible
Toda mismatch boundaries
indexed / unindexed structural distinction
```

Verified Phase 21 completion:

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

# Phase 22：Structured Generator Representation

Phase 22 は、actual tables / literature notation に現れる generator identity を
単なる `HomotopyElement.name: str` よりも構造的に保持するための最小 layer
を追加した。

Target examples:

```text
ν
ν′
decorated ν
η_n
μ_n
ι_n
```

Stable / unstable classification、generator table、automatic typing、
indexed Toda theorem applicability は先取りしない。

---

## Phase 22-1：GeneratorSymbol の最小表現

追加:

```text
GeneratorSymbol
  family: str
  index: int | None
  decoration: str | None
```

`GeneratorSymbol` は `Expression` ではない。

Representative storage:

```text
family
index
decoration
```

のみ。

Verified:

```text
tests/test_expression.py
92 passed in 0.36s
```

```text
full suite
1127 passed in 22.62s
```

### 状態

完了

---

## Phase 22-2：family / index の structural equality

Production code は変更せず regression を追加。

Fixed:

```text
η₃ == η₃
η₃ != μ₃
η₃ != η₄
η != η₃
```

`index=None` は wildcard ではない。

Verified:

```text
tests/test_expression.py
96 passed in 0.33s
```

```text
full suite
1131 passed in 22.66s
```

### 状態

完了

---

## Phase 22-3：decoration の最小表現

Production code は変更せず decoration identity を regression で固定。

Fixed:

```text
ν′ == ν′
ν != ν′
ν′ != barν
```

`decoration=None` は wildcard ではない。

No decoration normalization.

Verified:

```text
tests/test_expression.py
100 passed in 0.33s
```

```text
full suite
1135 passed in 22.53s
```

### 状態

完了

---

## Phase 22-4：ν / ν′ / decorated ν の区別

Representative / boundary regression。

Fixed:

```text
ν
ν′
barν
```

as distinct structured generators.

Also fixed:

```text
decoration role
!=
index role
```

Example:

```text
ν′ != ν′₇
```

Verified:

```text
tests/test_expression.py
103 passed in 0.33s
```

```text
full suite
1138 passed in 22.95s
```

### 状態

完了

---

## Phase 22-5：η_n / μ_n / ι_n の indexed generator 表現

Representative indexed forms:

```text
η₃
μ₃
ι₇
```

represented by shared `GeneratorSymbol(family,index)` structure.

Fixed:

```text
η₃ != μ₃
ι₇ != ι₈
```

No indexed-generator subclass.

Verified:

```text
tests/test_expression.py
108 passed in 0.34s
```

```text
full suite
1143 passed in 22.57s
```

### 状態

完了

---

## Phase 22-6：source / target context との接続

`HomotopyElement` に optional:

```text
generator: GeneratorSymbol | None
```

を追加。

Current shape:

```text
HomotopyElement
  name
  dimension
  source
  target
  generator
```

Role separation:

```text
GeneratorSymbol
=
generator identity / notation

HomotopyElement
=
expression + dimension / source / target context
```

Critical boundary:

```text
generator notation
↛
automatic source / target typing
```

Verified:

```text
tests/test_expression.py
111 passed in 0.50s
```

```text
full suite
1146 passed in 22.59s
```

### 状態

完了

---

## Phase 22-7：HomotopyElement との backward compatibility

Production code は変更せず regression を追加。

Fixed:

```text
HomotopyElement(name,dimension)
```

remains supported.

Omitted generator equals:

```text
generator=None
```

Existing helpers remain unchanged:

```text
eta()
nu()
sigma()
```

When present, `generator` participates in structural equality.

Verified:

```text
tests/test_expression.py
116 passed in 0.38s
```

```text
full suite
1151 passed in 22.39s
```

### 状態

完了

---

## Phase 22-8：representative literature scenario

Production code は変更せず actual literature notation に近い integration
regression を追加。

Representative:

```text
{η₃,Eν′,ν₇}_1
```

Storage:

```text
η₃
=
GeneratorSymbol(family="η",index=3)

ν′
=
GeneratorSymbol(family="ν",decoration="′")

Eν′
=
Suspension(ν′)

ν₇
=
GeneratorSymbol(family="ν",index=7)

_1
=
TodaBracket.index
```

No membership inference.

No automatic typing.

Verified:

```text
tests/test_expression.py
117 passed in 0.39s
```

```text
full suite
1152 passed in 22.56s
```

### 状態

完了

---

## Phase 22-9：regression / boundary

Final regression fixed the full Phase 22 boundary.

Checks include:

```text
GeneratorSymbol is not Expression
ν / ν′ / barν distinct
η₃ / μ₃ distinct
ι₇ / ι₈ distinct
generator + source / target coexist
generator does not derive typing
name / generator mismatch remains constructible
legacy eta()/nu()/sigma() unchanged
Suspension preserves underlying generator identity
{η₃,Eν′,ν₇}_1 remains lossless
```

Verified:

```text
tests/test_expression.py
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

### 状態

完了

---

# Phase 22 completion boundary

Implemented:

```text
GeneratorSymbol
GeneratorSymbol.family
GeneratorSymbol.index
GeneratorSymbol.decoration
HomotopyElement.generator
```

Representative:

```text
ν
ν′
barν
η₃
μ₃
ι₇
{η₃,Eν′,ν₇}_1
```

Important boundaries:

```text
GeneratorSymbol
!=
Expression
```

```text
family / index / decoration
=
structural identity
```

```text
generator notation
!=
automatic typing
```

```text
generator identity
!=
homotopy operation
```

```text
Eν′
=
Suspension(ν′)
```

```text
constructible
!=
validated
```

```text
legacy HomotopyElement API
=
preserved
```

Not implemented:

```text
decoration normalization
generator parser / registry
generator table lookup
automatic source / target derivation
name / generator validation
generator / dimension validation
ambient homotopy-group validation
stem validation
stable / unstable generator classification
automatic migration of eta()/nu()/sigma()
Toda definedness typing guard
indexed Toda theorem applicability
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
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

---

# Current verified status

```powershell
python -m pytest tests/test_expression.py -q
```

```text
118 passed in 0.44s
```

```powershell
python -m pytest -q
```

```text
1153 passed in 24.83s
```

No failures.

---

# Next boundary

Natural next candidate:

```text
Phase 23
Indexed Toda theorem / validity connection
```

Potential direction:

```text
indexed theorem fact
+
matching indexed bracket
+
required bracket definedness
+
explicit structural / typing side conditions
↓
indexed Toda membership
```

Use actual literature-backed facts.

Do not infer theorem applicability merely from:

```text
IndexedTodaBracketData.is_consistent() == True
```

or:

```text
TodaBracket.are_defining_compositions_type_compatible() == True
```

Stable homotopy representation and stable Toda notation remain later layers.

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
