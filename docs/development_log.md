# ehp_proof 開発記録

この文書は Phase 17 完了時点までの開発履歴を、現在の実装と矛盾しない
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

# Phase 18 boundary

Phase 17 完了により、次の自然な Phase は:

```text
Phase 18: Toda bracket minimum representation
```

Phase 18 は:

```text
bracket input structure
```

と:

```text
bracket value / indeterminacy
```

を分離して設計する。

Primary actual notation:

```text
{a,b,c}
```

将来必要な indexed unstable notation:

```text
{a,E^t b,E^t c}_t
```

Stable notation:

```text
<a,b,c>
```

は unstable notation と同一視しない。

Phase 17 の:

```text
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

を可能な限り再利用しつつ、Toda-specific abstraction は actual bracket
example が要求する最小範囲だけ追加する。

Full higher-Toda framework を先取りしない。

Generic engine の変更は actual Toda theorem が current rule language で
表現できないと実証された場合のみ。

---

# Current verified status

Full suite at Phase 17 completion:

```powershell
python -m pytest -q
```

```text
1024 passed in 66.01s
```

Phase 17 focused:

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
