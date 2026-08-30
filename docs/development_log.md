# ehp_proof 開発記録

この文書は Phase 19 完了時点までの開発履歴を、現在の実装と矛盾しない
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

を algebra-layer subgroup equality として扱えるようにした。

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
↓
generic equality / ZERO reasoning
```

EHP / ORDER branches が同一 knowledge state で coexist し、provenance が
混線しないことを確認。

Phase 7 completion:

```text
706 passed in 60.22s
```

### 状態

完了

---

# Phase 8：Suspension reasoning

`Suspension(expression)` を導入。

```text
x=y → E(x)=E(y)
x=0 → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension により unrestricted fixed-point termination を仮定
できないことを仕様化。

Phase 8 completion:

```text
721 passed in 22.16s
```

### 状態

完了

---

# Phase 9：Freudenthal / stable-range reasoning

Stable:

```text
stem <= sphere_dimension - 2
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary:

```text
stem == sphere_dimension - 1
→ epimorphism only
```

Outside:

```text
stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

Phase 9 completion:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 10：Composition reasoning / Suspension-composition functoriality

Known:

```text
α∘β = γ
```

を structured `Composition` を含む generic equality として扱う。

Suspension-composition functoriality と equality closure を接続。

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

Theorem boundary:

```text
H(x)=0
↛
x=0
```

Representative Hopf + EHP scenario、provenance、termination boundary を固定。

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

Current inverse:

```text
-α = Multiple(-1,α)
```

Additive rules:

```text
α+(-α)=0
α+β=β+α
(α+β)+γ=α+(β+γ)
α+α=2α
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

Explicit homomorphism fact のもとで:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
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

Formalized:

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

Important:

```text
same underlying subgroup value
≠
same proof-level subgroup role
```

Exactness:

```text
Exactness(f,g)
↓
Im(f)=Ker(g)
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

Theorem bridges:

```text
α≡β mod A
↔
α-β∈A
```

```text
α≡β mod A
↔
α+A=β+A
```

```text
α=β
→
α≡β mod A
```

Role-aware modulus transport と Exactness integration を追加。

Current Phase 15 cyclic family は finite known term set 上で
`FIXED_POINT`。

Phase 15 completion:

```text
956 passed in 64.09s
```

### 状態

完了

---

# Phase 16：Symbolic scalar constraints

Phase 16 は symbolic coefficient を proof-level reasoning に接続した。

Representation:

```text
ScalarSymbol(k)
OddScalarStatement(k)
EvenScalarStatement(k)
ScalarCongruenceStatement(k,r,m)
```

Principal chain:

```text
k odd
↓
k≡1 mod 2
```

```text
ord(β)=2
+
k≡1 mod 2
↓
kβ=β
```

Integration:

```text
kβ=β
↓ existing equality→modulo
kβ≡β mod Ker(H)
```

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
↓
kβ≡β mod Im(E)
```

Important design result:

```text
symbolic scalar reasoning
≠
general arithmetic solver
```

and:

```text
scalar reasoning
≠
automatic modulo enumeration
```

Verified full suite:

```text
988 passed in 61.87s
```

### 状態

完了

---

# Phase 17：Indeterminacy

Phase 17 は「値を一つに確定できない数学的情報」を、確定値へ潰さず
proof-level knowledge として保持する最小層を追加した。

基本原則:

```text
actual mathematical example
↓
必要な最小表現
↓
共通部分が見えたら一般化
```

Universal `Indeterminacy` / `CandidateFamily` は導入しなかった。

---

## Phase 17-1：CosetMembershipStatement

追加:

```text
CosetMembershipStatement
```

Semantics:

```text
x ∈ β+A
```

Phase 15 `Coset` をそのまま再利用。

Phase 14 `MembershipStatement(x,A)` は subgroup membership であり、
coset membership へ型を広げなかった。

候補列挙は行わない。

Focused result:

```text
4 passed
```

Full suite:

```text
992 passed in 71.71s
```

### 状態

完了

---

## Phase 17-2：sign indeterminacy

追加:

```text
SignIndeterminacyStatement(
  value=x,
  representative=α,
)
```

Semantics:

```text
x = ±α
```

候補を:

```text
α
-α
```

という Python list に展開しない。

Ordinary equality ではない。

この Phase では:

```text
x=±α
↛
x=α
```

```text
x=±α
↛
x=-α
```

を維持。

Focused:

```text
8 passed
```

Full suite:

```text
996 passed in 74.70s
```

### 状態

完了

---

## Phase 17-3：coefficient indeterminacy

追加:

```text
CoefficientIndeterminacyStatement
```

Representation:

```text
value
expression
constraint
```

Example:

```text
x = kβ+γ
k odd
```

を概念上:

```text
x ∈ {kβ+γ | k odd}
```

として保持。

再利用:

```text
ScalarSymbol
Multiple
Sum
OddScalarStatement
```

Concrete candidate:

```text
k=1,3,5,...
```

は列挙しない。

Initial import error:

```text
OddScalarStatement
```

を `set_rules` から import していたため collection error。

修正:

```text
set_rules
→
scalar_rules
```

修正後:

```text
13 passed
```

Full suite:

```text
1001 passed in 63.28s
```

### 状態

完了

---

## Phase 17-4：modulo / coset reasoning との接続

追加:

```text
x≡β mod A
↓
x∈β+A
```

`ModuloStatement` と既存 `Coset` を再利用。

Phase 15 の既存 modulo / coset equality reasoning は変更しなかった。

この Phase では reverse bridge はまだ追加せず、
Phase 15 → Phase 17 の入口だけを追加。

Full suite:

```text
1005 passed in 63.23s
```

### 状態

完了

---

## Phase 17-5：equality / membership bridge

追加:

```text
x=α
↓
x=±α
```

と:

```text
x∈β+A
↓
x≡β mod A
```

これにより Phase 17-4 と合わせて:

```text
x≡β mod A
↔
x∈β+A
```

が explicit theorem bridge になった。

### Nested pattern issue

Initial implementation では:

```text
CosetMembershipStatement(
  coset=Coset(
    representative=PatternVariable(...),
    subgroup=PatternVariable(...),
  )
)
```

という nested pattern を使ったが、current generic matcher は arbitrary
nested dataclass recursive unification を提供しないため match しなかった。

失敗:

```text
3 failed, 21 passed
```

修正:

```text
PremisePattern(
  statement_type=CosetMembershipStatement,
)
+
match_guard
+
conclusion_builder
```

とし、nested `Coset` structure を rule 内で明示的に読むようにした。

Generic engine は変更しなかった。

修正後:

```text
24 passed
```

Full suite:

```text
1012 passed in 67.09s
```

### 状態

完了

---

## Phase 17-6：symbolic scalar reasoning との接続

追加:

```text
x=kβ+γ
k odd
↓
CoefficientIndeterminacyStatement
```

Rule は equality の right-hand side が current structural form:

```text
Sum(
  left=Multiple(
    coefficient=k,
    expression=β,
  ),
  right=γ,
)
```

であることを確認。

さらに:

```text
expression.left.coefficient
==
OddScalarStatement.scalar
```

を要求。

Reject:

```text
x=kβ+γ
l odd
```

Current Phase では:

```text
γ+kβ
```

を normalize しない。

Candidate:

```text
k=1
k=3
k=5
...
```

を生成しない。

Focused:

```text
30 passed
```

Full suite:

```text
1018 passed in 68.27s
```

### 状態

完了

---

## Phase 17-7：representative scenario

新 rule は追加しなかった。

Initial facts:

```text
x=kβ+γ
k odd
x≡δ mod A
```

Same fixed-point run で:

```text
k≡1 mod 2
CoefficientIndeterminacyStatement
SignIndeterminacyStatement
CosetMembershipStatement
ModuloStatement
```

が coexist。

Reject:

```text
x=δ
```

No candidate enumeration。

Terminal:

```text
FIXED_POINT
new_steps == ()
```

Focused:

```text
31 passed
```

Full suite:

```text
1019 passed in 62.60s
```

### 状態

完了

---

## Phase 17-8：provenance / termination / inference-scope boundary

新 production rule は追加しなかった。

Regression-fixed:

### provenance

```text
x=kβ+γ
+
k odd
↓
CoefficientIndeterminacyStatement
```

の direct premises / inference_rule を追跡。

```text
x=kβ+γ
↓
SignIndeterminacyStatement
```

の provenance を追跡。

```text
x≡δ mod A
↓
x∈δ+A
```

の provenance を追跡。

### termination

Bidirectional bridge:

```text
Modulo
↔
CosetMembership
```

は duplicate rejection により finite `FIXED_POINT`。

Terminal round:

```text
new_steps == ()
```

Duplicate candidates:

```text
duplicate_rejected_steps
```

に保持。

### non-collapse

```text
x=±α
↛
x=α
```

```text
x=±α
↛
x=-α
```

```text
x∈β+A
↛
x=β
```

### inference scope

```text
CoefficientIndeterminacyStatement
```

を generic symbolic equality と誤認しない。

```text
SignIndeterminacyStatement
```

を equality rule の premise として誤認しない。

No candidate enumeration。

Focused:

```text
36 passed in 2.97s
```

Full suite:

```text
1024 passed in 66.01s
```

### 状態

完了

---

# Phase 17 completion summary

Phase 17 により proof layer は:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

という3種類の concrete indeterminacy を first-class knowledge として保持
できるようになった。

Main bridges:

```text
x≡β mod A
↔
x∈β+A
```

```text
x=α
→
x=±α
```

```text
x=kβ+γ
k odd
→
CoefficientIndeterminacyStatement
```

Important boundaries:

```text
indeterminacy
≠
exact equality
```

```text
uncertainty
≠
candidate enumeration
```

```text
mathematical applicability
≠
active inference scope
```

Current bidirectional modulo / coset membership cycle is finite for fixed known
terms and reaches genuine `FIXED_POINT`.

Generic inference engine:

```text
unchanged
```

Verified Phase 17 suite:

```text
36 passed
```

Verified full suite:

```text
1024 passed in 66.01s
```

### 状態

完了

---

# Phase 17 completion boundary

Phase 17 で実装しないもの:

```text
general Indeterminacy superclass
general CandidateFamily
general finite candidate-set algebra
set intersection / narrowing
automatic sign selection
automatic coset representative selection
automatic coefficient enumeration
general symbolic constraint hierarchy
general symbolic arithmetic solver
automatic indeterminacy collapse from ORDER
typed source / target / ambient group validation
stable homotopy group model
structured generator overhaul
iterated symbolic suspension E^t
Toda bracket syntax
Toda bracket defining conditions
Toda bracket value / containment rules
stable Toda bracket
higher Toda bracket
general theorem quantifier language
existential witness language
semantic cycle detection
fully recursive pattern unification
```

`max_rounds` は引き続き generic safety bound。

---


# Phase 18：Toda bracket minimum representation

Phase 18 は three-fold unstable Toda bracket を first-class に導入し、
bracket input structure と bracket value を分離した。

基本境界:

```text
bracket input structure
≠
bracket value
```

また:

```text
definedness
≠
membership
≠
exact value
```

を明示的に維持した。

---

## Phase 18-1：Toda bracket object の最小表現

追加:

```text
TodaBracket
```

Representation:

```text
TodaBracket(
  first=a,
  second=b,
  third=c,
)
```

Notation:

```text
{a,b,c}
```

`TodaBracket` の entries は `Expression`。

ただし bracket 自身は `Expression` にしなかった。

理由:

```text
Toda bracket
=
set-valued / indeterminate structure
```

であり、一つの exact homotopy element として扱わないため。

Three-fold bracket の actual scope に限定し、variable arity は導入しなかった。

Focused:

```text
tests/test_expression.py
35 passed in 2.05s
```

Full suite:

```text
1026 passed in 65.52s
```

### 状態

完了

---

## Phase 18-2：structural distinction

新 production code は追加しなかった。

Structural equality を regression 固定:

```text
{a,b,c}
=
structurally
{a,b,c}
```

```text
{a,b,c}
!=structurally
{a,c,b}
```

この distinction は数学的な非等価性を主張するものではなく、entry order
を representation layer で失わないための仕様。

Constructor-side sorting / permutation normalization は追加しなかった。

Focused:

```text
tests/test_expression.py
37 passed in 1.80s
```

Full suite:

```text
1028 passed in 64.59s
```

### 状態

完了

---

## Phase 18-3：bracket membership

新規:

```text
toda_rules.py
```

追加:

```text
TodaBracketMembershipStatement
```

Semantics:

```text
x ∈ {a,b,c}
```

Phase 14 の:

```text
MembershipStatement(x,A)
```

は subgroup membership 専用のままとし、general set membership に
拡張しなかった。

Bracket entries:

```text
a,b,c
```

は bracket の input であり、候補値ではない。

したがって:

```text
x∈{a,b,c}
↛
x=a
x=b
x=c
```

Focused:

```text
4 passed in 0.79s
```

Full suite:

```text
1032 passed in 66.12s
```

### 状態

完了

---

## Phase 18-4：Phase 17 Indeterminacy との接続

Production rule は追加しなかった。

確認した coexistence:

```text
x∈{a,b,c}
x=±α
```

```text
x∈{a,b,c}
x∈β+A
```

同じ `x` に関する別の partial information として同一 knowledge model
上に保持できることを確認。

No automatic bridge:

```text
x∈{a,b,c}
↛
x=±α
```

```text
x∈{a,b,c}
↛
x∈β+A
```

また Toda membership と sign / coset statements を同一視しないことを
固定。

Initial test import では存在しない algebra helper を import したため
collection error。

```text
ImportError:
cannot import name 'make_cyclic_group' from 'algebra'
```

既存 set-rule tests と同じ local helper を `tests/test_toda_rules.py` に
置く形へ修正。

修正後:

```text
8 passed in 1.98s
```

Full suite:

```text
1036 passed in 61.27s
```

### 状態

完了

---

## Phase 18-5：zero-composition defining facts との接続

追加:

```text
TodaBracketDefinedStatement
```

追加 rule:

```text
toda_bracket_defined_by_zero_compositions_inference_rule()
```

Semantics:

```text
ZERO(a∘b)
+
ZERO(b∘c)
↓
{a,b,c} defined
```

Existing Phase 10 bridge:

```text
Composition(...)=0
EQUALITY
↓
Composition(...)=0
ZERO
```

を再利用。

Integration:

```text
a∘b=0
b∘c=0
↓
ZERO(a∘b)
ZERO(b∘c)
↓
{a,b,c} defined
```

Shared middle entry:

```text
b
```

の structural identity を要求。

Reject:

```text
a∘b=0
d∘c=0
```

One zero-composition premise onlyでは definedness を生成しない。

Important boundary:

```text
{a,b,c} defined
↛
x∈{a,b,c}
```

Full source / target typing は導入しなかった。

Focused:

```text
13 passed in 2.11s
```

Full suite:

```text
1041 passed in 62.10s
```

### 状態

完了

---

## Phase 18-6：provenance

新 production rule は追加しなかった。

Regression-fixed chain:

```text
known a∘b=0
↓
ZERO(a∘b)

known b∘c=0
↓
ZERO(b∘c)

ZERO(a∘b)
+
ZERO(b∘c)
↓
{a,b,c} defined
```

Final definedness step:

```text
premises:
  ZERO(a∘b)
  ZERO(b∘c)

inference_rule:
  toda bracket defined by zero compositions
```

各 ZERO step:

```text
premise:
  corresponding original composition equality

inference_rule:
  composition equality → zero
```

Unrelated fact は direct provenance に混入しないことを固定。

Focused:

```text
15 passed in 3.15s
```

Full suite:

```text
1043 passed in 60.38s
```

### 状態

完了

---

## Phase 18-7：representative scenario

新 rule は追加しなかった。

Initial knowledge:

```text
a∘b=0
b∘c=0
x∈{a,b,c}
x=±α
```

Same fixed-point run で:

```text
ZERO(a∘b)
ZERO(b∘c)
{a,b,c} defined
```

を導出しつつ:

```text
x∈{a,b,c}
x=±α
```

を coexist。

Reject:

```text
x=α
```

Representative run:

```text
FIXED_POINT
round_count == 2
```

Focused:

```text
16 passed in 3.47s
```

Full suite:

```text
1044 passed in 59.62s
```

### 状態

完了

---

## Phase 18-8：termination / inference-scope boundary

新 production rule は追加しなかった。

Regression-fixed:

### genuine fixed point

Representative final knowledge へもう一度 active rule family を適用し:

```text
new_steps == ()
```

を確認。

### definedness / membership boundary

```text
{a,b,c} defined
↛
x∈{a,b,c}
```

### membership / exact value boundary

```text
x∈{a,b,c}
+
x=±α
↛
x=α
```

```text
x∈{a,b,c}
+
x=±α
↛
x=-α
```

### inference scope

```text
TodaBracketDefinedStatement
```

と:

```text
TodaBracketMembershipStatement
```

は generic equality symmetry の premise に match しない。

Initial run では test import に `Multiple` が不足して:

```text
NameError: name 'Multiple' is not defined
```

となった。

`Multiple` import を追加後:

```text
20 passed in 3.36s
```

Full suite:

```text
1048 passed in 61.09s
```

### 状態

完了

---

# Phase 18 completion summary

Phase 18 により proof layer は three-fold unstable Toda bracket の最小構造を
first-class に保持できるようになった。

Implemented:

```text
TodaBracket(a,b,c)
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Main chain:

```text
a∘b=0
b∘c=0
↓
generic ZERO
↓
{a,b,c} defined
```

Membership:

```text
x∈{a,b,c}
```

を definedness とは独立に保持。

Phase 17 partial information:

```text
x=±α
x∈β+A
```

とも coexist できる。

Important boundaries:

```text
bracket
≠
exact Expression
```

```text
definedness
≠
membership
```

```text
membership
≠
exact value
```

```text
x∈{a,b,c}
+
x=±α
↛
x=± selected value
```

Current representative rule family reaches genuine:

```text
FIXED_POINT
```

with terminal:

```text
new_steps == ()
```

Generic inference engine:

```text
unchanged
```

Verified focused suite:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

Verified full suite:

```text
1048 passed in 61.09s
```

### 状態

完了

---

# Phase 18 completion boundary

Phase 18 で実装しないもの:

```text
bracket-definedness → arbitrary membership
bracket membership → exact value
automatic Toda → sign indeterminacy
automatic Toda → coset indeterminacy
automatic reverse indeterminacy bridge
Toda bracket containment
general set-valued expression hierarchy
general candidate-set algebra
variable-arity Toda bracket
indexed unstable notation {a,E^t b,E^t c}_t
symbolic iterated suspension E^t
full source / target typing
stable homotopy group model
stable Toda bracket <a,b,c>
higher Toda bracket
general theorem quantifier language
existential witness language
semantic cycle detection
fully recursive pattern unification
```

`max_rounds` は引き続き generic safety bound。

---


# Phase 19：Toda bracket membership / first theorem bridge

Phase 19 は、Phase 18 で first-class にした three-fold Toda bracket
membership を、初めて actual literature-backed theorem fact から導出する
bridge に接続した。

Selected actual example:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

Literature notation の `_1` index は current Phase 19 representation には
保持せず、Phase 20 の indexed unstable notation に延期した。

`Eν′` は:

```text
Suspension(ν′)
```

として structural に保持した。

---

## Phase 19-1：最初の actual Toda fact の選定

最初の theorem bridge 用 actual example として:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

を採用。

Current Phase 18/19 three-fold representation へは:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

として投影する方針を固定。

Important:

```text
current unindexed projection
≠
lossless indexed notation
```

`_1` は Phase 20 で回収する。

### 状態

完了

---

## Phase 19-2：known Toda membership fact の最小表現

Existing:

```text
TodaBracketMembershipStatement
```

をそのまま actual membership conclusion に利用。

追加:

```text
source
note
```

Known membership fact を:

```text
ProofRule.GIVEN
```

として保持する helper:

```text
toda_bracket_membership_proof_step()
```

を追加。

Actual representation:

```text
ε₃
Eν′ = Suspension(ν′)
ν₇
```

General theorem hierarchy、structured generator overhaul、indexed bracket は
導入しなかった。

Focused:

```text
23 passed in 2.62s
```

Full suite:

```text
1051 passed in 64.71s
```

### 状態

完了

---

## Phase 19-3：最初の theorem bridge

追加:

```text
TodaBracketMembershipTheoremStatement
```

Fields:

```text
element
bracket
source
note
```

Semantics:

```text
matching bracket が defined なら
この literature-backed theorem が
element の bracket membership を与える
```

Theorem fact を GIVEN step にする helper:

```text
toda_bracket_membership_theorem_proof_step()
```

を追加。

Inference rule:

```text
toda_bracket_membership_from_theorem_inference_rule()
```

Main bridge:

```text
Toda membership theorem fact
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

Reject:

```text
different bracket
```

Boundaries:

```text
theorem fact only
↛
membership
```

```text
definedness only
↛
membership
```

General quantified theorem framework は導入しなかった。

Focused:

```text
27 passed in 2.20s
```

Full suite:

```text
1055 passed in 62.40s
```

### 状態

完了

---

## Phase 19-4：definedness との multi-round 接続

Production code は変更しなかった。

Initial facts:

```text
η₃∘Eν′=0
Eν′∘ν₇=0
Toda membership theorem fact
```

Same fixed-point run:

```text
round 1
composition equality → ZERO

round 2
ZERO + ZERO → Toda definedness

round 3
theorem + definedness → ε₃ membership
```

Derived:

```text
ZERO(η₃∘Eν′)
ZERO(Eν′∘ν₇)
{η₃,Eν′,ν₇} defined
ε₃∈{η₃,Eν′,ν₇}
```

Representative integration:

```text
round_count == 3
FIXED_POINT
```

Focused:

```text
28 passed in 2.25s
```

Full suite:

```text
1056 passed in 63.74s
```

### 状態

完了

---

## Phase 19-5：Phase 17 indeterminacy との接続

Production code は変更しなかった。

Theorem-derived membership と:

```text
ε₃=±α
```

を coexist させても:

```text
ε₃=α
ε₃=-α
```

を導かないことを固定。

Theorem-derived membership と:

```text
ε₃∈β+A
```

を coexist させても:

```text
ε₃=β
```

を導かないことを固定。

また:

```text
Toda membership
↛
sign indeterminacy
```

を actual theorem-derived membership に対して確認。

No Toda→coset bridge / candidate intersection / narrowing を追加しなかった。

Focused:

```text
31 passed in 2.05s
```

Full suite:

```text
1059 passed in 69.75s
```

### 状態

完了

---

## Phase 19-6：provenance

Production code は変更しなかった。

Final membership dependency:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
│
├─ Toda membership theorem fact
│
└─ {η₃,Eν′,ν₇} defined
   │
   ├─ ZERO(η₃∘Eν′)
   │  └─ η₃∘Eν′=0
   │
   └─ ZERO(Eν′∘ν₇)
      └─ Eν′∘ν₇=0
```

固定した事項:

- membership direct premises = theorem + definedness
- theorem step = GIVEN
- definedness step retains Toda definedness rule
- ZERO steps retain composition equality → ZERO rule
- original composition equalities remain reachable
- LiteratureReference remains attached
- unrelated facts do not enter direct provenance

新しい provenance framework は追加しなかった。

Focused:

```text
33 passed in 2.54s
```

Full suite:

```text
1061 passed in 61.17s
```

### 状態

完了

---

## Phase 19-7：representative scenario

Production code は変更しなかった。

Initial knowledge:

```text
η₃∘Eν′=0
Eν′∘ν₇=0
Toda membership theorem fact
ε₃=±α
ε₃∈β+A
```

Derived:

```text
ZERO(η₃∘Eν′)
ZERO(Eν′∘ν₇)
{η₃,Eν′,ν₇} defined
ε₃∈{η₃,Eν′,ν₇}
```

Coexisting:

```text
ε₃=±α
ε₃∈β+A
```

Not derived:

```text
ε₃=α
ε₃=-α
ε₃=β
```

Membership direct provenance remained:

```text
theorem fact
definedness
```

and sign / coset facts did not enter that branch.

Result:

```text
round_count == 3
FIXED_POINT
```

Focused:

```text
34 passed in 3.77s
```

Full suite:

```text
1062 passed in 64.51s
```

### 状態

完了

---

## Phase 19-8：termination / inference-scope boundary

Production code は変更しなかった。

Representative final knowledge に active Phase 19 rules を再適用し:

```text
new_steps == ()
```

を確認。

Current active family:

```text
composition equality → ZERO
ZERO + ZERO → definedness
theorem + definedness → membership
```

は current representative finite knowledge state 上で genuine:

```text
FIXED_POINT
```

に到達。

また:

```text
TodaBracketMembershipTheoremStatement
```

が generic equality symmetry の premise に match しないことを固定。

Phase 18 からの:

```text
TodaBracketDefinedStatement
TodaBracketMembershipStatement
```

も generic equality scope 外のまま。

Critical boundaries:

```text
definedness only
↛ membership
```

```text
theorem fact only
↛ membership
```

```text
membership
↛ exact equality
```

```text
membership
↛ automatic sign / coset indeterminacy
```

Focused:

```text
36 passed in 3.06s
```

Full suite:

```text
1064 passed in 61.64s
```

### 状態

完了

---

# Phase 19 completion summary

Phase 19 により、Toda bracket membership は単なる GIVEN statement だけで
なく、actual literature-backed theorem fact と bracket definedness の組から
導出できるようになった。

Implemented:

```text
TodaBracketMembershipStatement.source
TodaBracketMembershipStatement.note
TodaBracketMembershipTheoremStatement
toda_bracket_membership_proof_step()
toda_bracket_membership_theorem_proof_step()
toda_bracket_membership_from_theorem_inference_rule()
```

Main actual chain:

```text
η₃∘Eν′=0
Eν′∘ν₇=0
↓
ZERO
↓
{η₃,Eν′,ν₇} defined
+
Toda membership theorem fact
↓
ε₃∈{η₃,Eν′,ν₇}
```

Important:

```text
definedness
≠
membership
```

```text
theorem fact
≠
membership
```

```text
membership
≠
exact value
```

```text
Toda theorem statement
≠
generic equality
```

Phase 17 partial information と coexist しても exact representative を
選択しない。

Full provenance は theorem fact と両 defining composition equalities まで
追跡可能。

Representative run:

```text
round_count == 3
FIXED_POINT
terminal new_steps == ()
```

Generic inference engine:

```text
unchanged
```

Verified focused suite:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

Verified full suite:

```text
1064 passed in 61.64s
```

### 状態

完了

---

# Phase 19 completion boundary

Phase 19 で実装しないもの:

```text
lossless indexed notation {η₃,Eν′,ν₇}_1
general indexed unstable Toda notation {a,E^t b,E^t c}_t
symbolic iterated suspension E^t
general theorem hierarchy
universal quantification
existential theorem language
typed source / target validation
ambient homotopy group validation
automatic Toda → sign indeterminacy
automatic Toda → coset indeterminacy
candidate intersection / narrowing
general Toda value-set algebra
stable Toda bracket
higher Toda bracket
semantic cycle detection
fully recursive unification
```

The literature `_1` index used by the actual ε₃ source example remains an
explicit known representation limitation.

`max_rounds` remains the generic safety bound.

---

# Phase 20 boundary

Next candidate Phase:

```text
Phase 20: indexed unstable Toda notation
```

The immediate actual need comes from the Phase 19 source notation:

```text
{η₃,Eν′,ν₇}_1
```

Current Phase 19 stores only:

```text
{η₃,Eν′,ν₇}
```

Phase 20 should therefore preserve bracket index information explicitly and
then generalize toward:

```text
{a,E^t b,E^t c}_t
```

Bracket index and suspension exponent must remain structurally separate even
when notation uses the same symbol.

Stable notation remains deferred.

---

# Current verified status

Full suite at Phase 19 completion:

```powershell
python -m pytest -q
```

```text
1064 passed in 61.64s
```

Phase 19 Toda focused:

```powershell
python -m pytest tests/test_toda_rules.py -q
```

```text
36 passed in 3.06s
```

Phase 17 focused remains:

```powershell
python -m pytest tests/test_indeterminacy_rules.py -q
```

```text
36 passed in 2.97s
```

No failures.

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

各 Phase では:

1. mathematical semantics
2. representation
3. rules
4. integration
5. provenance
6. termination / scope if relevant
7. test result
8. generic-engine impact
9. next-Phase boundary

を記録する。
