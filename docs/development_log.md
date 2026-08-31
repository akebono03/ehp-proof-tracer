# ehp_proof 開発記録

この文書は Phase 23 完了時点までの開発履歴を、現在の実装と矛盾しない
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

# Phase 21：Typed homotopy elements / source-target context

Phase 21 は actual composition / Toda validity に必要な最小 typing として
source / target context を導入した。

Universal type system、ambient homotopy group、stem、stable context は
先取りしない。

実装:

```text
HomotopyElement.source
HomotopyElement.target
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Boundary:

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
type compatibility
!=
ZERO
!=
Toda definedness
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

# Phase 22：Structured Generator Representation

Phase 22 は、actual tables / literature notation に現れる generator identity を
単なる `HomotopyElement.name: str` よりも構造的に保持するための最小 layer
を追加した。

追加:

```text
GeneratorSymbol
  family
  index
  decoration
```

Examples:

```text
ν
ν′
barν
η₃
μ₃
ι₇
```

`HomotopyElement` に optional:

```text
generator: GeneratorSymbol | None
```

を追加。

Critical:

```text
generator notation
↛
automatic source / target typing
```

Representative:

```text
{η₃,Eν′,ν₇}_1
```

を generator structure 込みで lossless に保持。

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

# Phase 23：Indexed Toda theorem / validity connection

Phase 23 は Phase 20〜22 で揃えた:

```text
indexed Toda structure
typed entries
structured generator identity
```

を、actual theorem fact と Toda membership inference に接続した。

---

## Phase 23-1：indexed Toda theorem fact の最小表現

既存:

```text
TodaBracketMembershipTheoremStatement
```

をそのまま再利用。

新しい indexed theorem class は追加しない。

Representative:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

を theorem fact として:

```text
element
bracket
index
generator structure
source
note
```

まで lossless に保持できることを regression で固定。

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
45 passed in 1.09s
```

```text
full suite
1154 passed in 24.37s
```

### 状態

完了

---

## Phase 23-2：bracket index match

Theorem bridge が whole-bracket structural equality により:

```text
{η₃,Eν′,ν₇}_1
==
{η₃,Eν′,ν₇}_1
```

を match し、

```text
{η₃,Eν′,ν₇}_1
!=
{η₃,Eν′,ν₇}_2
```

および:

```text
{η₃,Eν′,ν₇}_1
!=
{η₃,Eν′,ν₇}
```

を reject することを固定。

```text
index=None
```

は wildcard ではない。

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
48 passed in 0.82s
```

```text
full suite
1157 passed in 22.39s
```

### 状態

完了

---

## Phase 23-3：generator structure match

Same display name でも `GeneratorSymbol` の:

```text
family
index
decoration
```

が違えば theorem bridge が reject することを固定。

Representative mismatches:

```text
η₃ family mismatch
ν′ decoration mismatch
ν₇ generator-index mismatch
```

Generator-specific manual matcher は追加せず、既存 structural equality を再利用。

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
52 passed in 0.93s
```

```text
full suite
1161 passed in 23.21s
```

### 状態

完了

---

## Phase 23-4：definedness との接続

Indexed theorem fact 単独:

```text
↛ membership
```

Indexed definedness 単独:

```text
↛ membership
```

一方:

```text
matching indexed theorem
+
matching indexed definedness
↓
indexed membership
```

を representative case で固定。

Theorem source / note / index / generator structure が conclusion に保持される。

Indexed definedness 自体の導出規則は追加しない。

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
55 passed in 0.82s
```

```text
full suite
1164 passed in 22.77s
```

### 状態

完了

---

## Phase 23-5：structural consistency side condition

Canonical indexed form:

```text
{a,E^t b,E^t c}_t
```

用に新しい guarded bridge:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

を追加。

Guard に:

```text
indexed_data.is_consistent()
```

を要求。

Therefore:

```text
consistent
+
matching theorem
+
matching definedness
→ membership
```

一方:

```text
bracket index / suspension exponent mismatch
```

や:

```text
displayed suspended entry / stored base mismatch
```

は reject。

Important:

```text
is_consistent() == True
↛
theorem applies by itself
```

Verified:

```text
tests/test_toda_rules.py
58 passed in 0.96s
```

```text
full suite
1167 passed in 22.84s
```

### 状態

完了

---

## Phase 23-6：typing side condition の最小 guard

Phase 23-5 guarded bridge に:

```text
indexed_data.bracket
.are_defining_compositions_type_compatible()
```

を追加。

Canonical bridge now requires:

```text
structural consistency
+
confirmed typing compatibility
+
matching theorem
+
matching definedness
↓
membership
```

Known mismatch:

```text
→ reject
```

Unknown typing:

```text
→ reject
```

ただし:

```text
type-compatible
↛
ZERO
↛
definedness
```

は維持。

Verified:

```text
tests/test_toda_rules.py
61 passed in 0.87s
```

```text
full suite
1170 passed in 22.85s
```

### 状態

完了

---

## Phase 23-7：indexed theorem → membership bridge

Phase 23-1〜23-6 の条件を1本の representative inference に統合。

Canonical representative:

```text
{a₃,E²b₅,E²c₉}_2
```

に対して:

```text
indexed theorem fact
+
matching indexed bracket
+
generator structure
+
definedness
+
structural consistency
+
typing compatibility
↓
indexed membership
```

を確認。

Provenance:

```text
membership_step.premises
=
(theorem_step, defined_step)
```

Theorem source / note を conclusion に保持。

FIXED_POINT と terminal no-new-step も固定。

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
62 passed in 0.90s
```

```text
full suite
1171 passed in 22.91s
```

### 状態

完了

---

## Phase 23-8：ε₃ actual representative scenario

Actual literature notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

を theorem fact から membership まで lossless に保持。

Storage:

```text
ε₃
η₃
ν′
Eν′ = Suspension(ν′)
ν₇
index = 1
```

Important:

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

なので actual ε₃ bracket を canonical `IndexedTodaBracketData` に無理に変換しない。

Actual ε₃ theorem は existing narrow literature bridge:

```text
specific theorem
+
exactly matching definedness
↓
membership
```

を使用。

No inverse generator lookup:

```text
ν₇ ↛ ν₆
```

No automatic typing。

Verified:

```text
tests/test_toda_rules.py
63 passed in 0.85s
```

```text
full suite
1172 passed in 22.57s
```

### 状態

完了

---

## Phase 23-9：provenance / regression / boundary

Final safety regression。

Fixed:

```text
guarded bridge provenance
=
theorem_step + defined_step
```

Unrelated fact:

```text
↛ membership provenance
```

Responsibility boundary:

```text
canonical {a,E^t b,E^t c}_t
→ guarded bridge
```

```text
actual ε₃ ∈ {η₃,Eν′,ν₇}_1
→ narrow literature bridge
```

Actual ε₃ data is intentionally not canonical `IndexedTodaBracketData`.

Also fixed:

```text
indexed membership
↛
unindexed membership projection
```

Therefore the Phase 19 `_1`-loss limitation does not return.

Production code:

```text
変更なし
```

Verified:

```text
tests/test_toda_rules.py
66 passed in 1.01s
```

```text
full suite
1175 passed in 22.96s
```

### 状態

完了

---

# Phase 23 completion boundary

Implemented:

```text
indexed theorem fact preservation
bracket-index structural matching
structured-generator theorem matching
definedness dependency
canonical indexed consistency guard
canonical indexed typing guard
indexed guarded theorem bridge
canonical end-to-end representative
actual ε₃ literature representative
provenance / boundary regressions
```

New production rule:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

General canonical bridge:

```text
matching theorem
+
matching definedness
+
structural consistency
+
typing compatibility
↓
membership
```

Specific actual bridge:

```text
ε₃ theorem fact
+
exactly matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Important boundaries:

```text
index=None
!=
wildcard
```

```text
generator identity
=
structural theorem identity
```

```text
consistency
!=
theorem applicability
```

```text
typing
!=
definedness
```

```text
Suspension(α)
!=
IteratedSuspension(α,1)
```

```text
canonical indexed bridge
!=
specific literature bridge
```

```text
indexed membership
!=
unindexed membership
```

No generator lookup.

No automatic typing.

No indexed Toda definedness theorem system.

No universal theorem prover.

Generic inference engine unchanged.

Current verified status:

```text
tests/test_toda_rules.py
66 passed in 1.01s
```

```text
full suite
1175 passed in 22.96s
```

---

# Current verified status

```powershell
python -m pytest tests/test_toda_rules.py -q
```

```text
66 passed in 1.01s
```

```powershell
python -m pytest -q
```

```text
1175 passed in 22.96s
```

No failures.

---

# Next boundary

Natural next candidate:

```text
Phase 24
Theorem fact / knowledge-table integration
```

Potential direction:

```text
literature-backed facts
+
source / locator
+
structured theorem / relation
↓
table / repository
↓
existing proof-step / inference infrastructure
```

Do not introduce a universal theorem prover first.

Later candidates:

```text
generator typing / ambient-group facts
stable homotopy representation
stable Toda bracket
higher Toda bracket
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
chronological history

docs/roadmap.md
=
future capability dependency
```

今後も historical limitation と current limitation を混同しない。
