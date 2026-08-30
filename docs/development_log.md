# ehp_proof 開発記録

この文書は Phase 16 完了時点までの開発履歴を、現在の実装と矛盾しない
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

Rule families:

```text
x=y → E(x)=E(y)
x=0 → E(x)=0
nα=0 → nE(α)=0
```

ORDER / EHP branches と Suspension を統合し、generic reasoning への
reconnection と provenance を固定。

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

Actual theorem family として Freudenthal reasoning を追加。

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

Representative scenario、generic reasoning、provenance、theorem boundary、
finite fixed-point termination を固定。

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

Known zero composition:

```text
α∘β = 0
```

から generic ZERO へ bridge。

Suspension-composition functoriality:

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

Generic Suspension preservation と equality closure を使い:

```text
E(α∘β)=Eγ
E(α∘β)=Eα∘Eβ
↓
Eα∘Eβ=Eγ
```

へ接続。

Representative EHP + Toda + Suspension scenario、provenance、termination
boundary を固定。

Phase 10 completion:

```text
763 passed in 22.32s
```

### 状態

完了

---

# Phase 11：Generalized Hopf-invariant reasoning

Generalized Hopf invariant value を integer 専用にはしない。

```text
H(α)=β
```

の `β` は `Expression`。

Implemented:

```text
H(α)=β
↓
HopfCompositionLawStatement(α,β)
```

```text
HopfCompositionLawStatement(α,β)
↓
H(α∘Eγ)=β∘Eγ
```

```text
H(x)=y
y=0
↓
H(x)=0
```

EHP bridge:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eα)=0
```

Theorem boundary:

```text
H(x)=0
↛
x=0
```

Representative Hopf + EHP scenario と provenance regression、recursive
structural-growth boundary を固定。

Phase 11 completion:

```text
791 passed in 23.41s
```

### 状態

完了

---

# Phase 12：Additive expression / reasoning

Phase 12 は proof-expression layer に最小 additive structure を導入した。

追加:

```text
Sum(left,right)
```

Semantics:

```text
α+β
```

Binary tree structure を lossless に保持。

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

ORDER bridge:

```text
ord(α)=2
↓
2α=0

α+α=2α
↓
α+α=0
```

Normalization boundary:

```text
α+β                    !=structural β+α
(α+β)+γ                !=structural α+(β+γ)
2α                     !=structural α+α
α+0                    !=structural α
```

Finite concrete additive family は `FIXED_POINT`。

Phase 12 completion:

```text
809 passed in 62.32s
```

### 状態

完了

---

# Phase 13：Homomorphism reasoning

Phase 13 は additive expression と map reasoning を接続した。

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

Known ZERO preservationも接続。

Generic `E` homomorphism reasoning を existing `Suspension` syntax に接続。

Untyped unrestricted:

```text
Homomorphism(H)
Homomorphism(P)
```

は自動導入しない。

ORDER integration:

```text
ord(α)=n
↓
nα=0
↓
n f(α)=0
```

ただし:

```text
ord(f(α))=n
```

とはしない。

Finite concrete rule family は `FIXED_POINT`。

Phase 13 completion:

```text
856 passed in 62.31s
```

### 状態

完了

---

# Phase 14：Set / subgroup reasoning

Phase 14 は proof-level に element membership、subset、subgroup equality
を導入し、既存 algebra `Subgroup` / kernel / image と接続した。

最重要設計原則:

```text
same underlying subgroup value
≠
same proof-level subgroup role
```

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

Mapped ZERO と kernel membership:

```text
f(α)=0
↔
α∈Ker(f)
```

Exactness:

```text
Exactness(f,g)
↓
Im(f)=Ker(g)
```

Membership / equality / subset closure:

```text
α∈A
A⊆B
→ α∈B
```

```text
α∈A
A=B
→ α∈B
```

```text
A=B → B=A
```

```text
A=B
B=C
→ A=C
```

```text
A⊆B
B⊆C
→ A⊆C
```

```text
A=B → A⊆B
```

```text
A⊆B
B⊆A
→ A=B
```

Same underlying subgroup value does not cross role boundaries without explicit
theorem equality.

Representative Exactness + membership + closure scenario reaches genuine
`FIXED_POINT`.

Phase 14 completion:

```text
921 passed in 62.89s
```

### 状態

完了

---

# Phase 15：Coset / modulo reasoning

Phase 15 は Phase 14 の role-aware subgroup layer 上に quotient /
congruence semantics を導入した。

## Phase 15-1〜15-2：Coset / modulo minimum representation

追加:

```text
Coset
ModuloStatement
CosetEqualityStatement
```

Notation:

```text
α+A
α≡β mod A
α+A=β+A
```

`Coset` の Python equality は theorem-aware に変更しない。

## Phase 15-3：difference membership bridge

Current subtraction:

```text
α-β
=
Sum(
  left=α,
  right=Multiple(-1,β),
)
```

Implemented:

```text
α≡β mod A
↔
α-β∈A
```

Reverse rule は explicit difference structure のみ受理。

## Phase 15-4：coset equality bridge

```text
α≡β mod A
↔
α+A=β+A
```

Reverse bridge は同じ proof-level `SubgroupTerm` を要求。

## Phase 15-5：equality / ZERO bridge

Explicit modulus scope:

```text
α=β
→ α≡β mod A
```

```text
α=0
→ α≡0 mod A
```

arbitrary modulus enumeration は行わない。

## Phase 15-6：role-aware modulus transport

```text
A=B
α≡β mod A
→
α≡β mod B
```

Raw subgroup value equalityだけでは role-aware modulo を transport しない。

## Phase 15-7：Exactness integration

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
↓
role-aware modulo transport
```

No special Exactness-modulo shortcut を追加しない。

## Phase 15-8：representative / provenance / termination boundary

Representative:

```text
Exactness(E,H)
α=β
β=0
```

から kernel/image modulo、difference membership、coset equality を導出。

Alternative derivation では first accepted provenance を knowledge state に
保持し、別 derivation を duplicate-rejected trace に残す。

Bidirectional bridge:

```text
Modulo ↔ membership
Modulo ↔ coset equality
```

を含めても finite active term set で genuine `FIXED_POINT` に到達。

## Phase 15-9：完了整理

Phase 15 completion full suite:

```text
956 passed in 64.09s
```

Generic inference engine:

```text
unchanged
```

### 状態

完了

---

# Phase 16：Symbolic scalar constraints

Phase 16 は symbolic integer coefficient を concrete integer に collapse
せず、既存 additive / ORDER / modulo layers に接続する最小基盤を追加した。

Generic inference engine は Phase 16 を通じて変更していない。

## Phase 16-1：symbolic scalar representation

追加:

```text
ScalarSymbol
```

Symbolic coefficient:

```text
kβ
```

を:

```text
Multiple(
  coefficient=k,
  expression=β,
)
```

として表現可能にした。

これにより:

```text
α = kβ + γ
```

のような additive relation を lossless に表現できる。

## Phase 16-2：parity statement

追加:

```text
OddScalarStatement(k)
EvenScalarStatement(k)
```

Parity を scalar name や syntax から暗黙推論せず、proof-level fact として
保持する。

## Phase 16-3：scalar congruence statement

追加:

```text
ScalarCongruenceStatement(
  scalar=k,
  residue=r,
  modulus=m,
)
```

Current principal use:

```text
k≡1 mod 2
k≡0 mod 2
```

General modular arithmetic solver は導入しない。

## Phase 16-4：odd / even → mod two

Explicit rules:

```text
k odd
→
k≡1 mod 2
```

```text
k even
→
k≡0 mod 2
```

Parity mismatch rejection をテストで固定。

## Phase 16-5：symbolic additive equality / generic equality reconnection

```text
α = kβ + γ
```

を ordinary `RelationType.EQUALITY` として扱う。

Generic equality symmetry が symbolic `Multiple` / `Sum` を含む relation に
そのまま適用可能であることを確認。

No dedicated symbolic equality type を追加しない。

## Phase 16-6：order reasoning との接続

Principal theorem bridge:

```text
ord(β)=2
k≡1 mod 2
↓
kβ=β
```

Reject boundaries:

```text
ord(β)=3
↛
kβ=β
```

```text
k≡0 mod 2
↛
kβ=β
```

Odd scalar fact と order-two fact を同一 fixed-point run に投入して:

```text
k odd
↓
k≡1 mod 2
↓
kβ=β
```

へ multi-round 接続。

## Phase 16-7：modulo reasoning との接続

Scalar-specific modulo shortcut は追加しない。

既存 Phase 15 bridge を再利用:

```text
kβ=β
↓
kβ≡β mod A
```

ただし:

```text
equality_implies_modulo_inference_rule(modulus=A)
```

が explicit に active である場合のみ。

Symbolic `Multiple` を含む modulo statement が既存 membership / coset /
role-aware modulus transport と互換であることを確認。

## Phase 16-8：representative scenario

Initial facts:

```text
k odd
ord(β)=2
Exactness(E,H)
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

```text
kβ=β
↓
kβ≡β mod Ker(H)
```

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
kβ≡β mod Ker(H)
+
Im(E)=Ker(H)
↓
kβ≡β mod Im(E)
```

Existing Phase 15 rules then derive:

```text
kβ-β∈Ker(H)
kβ-β∈Im(E)
```

and:

```text
[kβ]=[β] mod Ker(H)
[kβ]=[β] mod Im(E)
```

Representative scenario reaches genuine:

```text
FIXED_POINT
```

Phase 16 focused integration after representative addition:

```text
122 passed in 3.93s
```

At that checkpoint full suite:

```text
985 passed in 64.40s
```

## Phase 16-9：provenance / termination / inference-scope boundary

### Provenance

Symbolic membership conclusion with two derivations:

```text
image modulo
→ image difference membership
```

and:

```text
kernel difference membership
+
Im(E)=Ker(H)
→ image difference membership
```

を同一 round で生成。

確認:

```text
first accepted derivation
=
knowledge-state provenance
```

and:

```text
alternative derivation
=
duplicate_rejected_steps trace
```

### Termination

Rules:

```text
odd → congruence
order-two + congruence → equality
equality → modulo
modulo ↔ membership
modulo ↔ coset equality
role-aware modulus transport
```

を同時に active にしても current finite scenario は:

```text
FIXED_POINT
```

に到達。

Terminal round:

```text
new_steps == ()
```

### Inference scope

Critical regression:

```text
k odd
ord(β)=2
```

with scalar/order rules derives:

```text
k≡1 mod 2
kβ=β
```

but without explicit equality→modulo rule:

```text
no ModuloStatement
no MembershipStatement
no CosetEqualityStatement
```

Principle:

```text
mathematical applicability
≠
active inference scope
```

Phase 16-9 focused:

```text
3 passed in 2.10s
```

Full suite:

```text
988 passed in 61.87s
```

### 状態

完了

---

# Phase 16 completion summary

Phase 16 により proof layer は symbolic scalar constraints の最小 vertical
slice を扱えるようになった。

Representation:

```text
ScalarSymbol(k)
OddScalarStatement(k)
EvenScalarStatement(k)
ScalarCongruenceStatement(k,r,m)
```

Principal theorem chain:

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

then existing Phase 15 bridges:

```text
modulo
↔ difference membership
↔ coset equality
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

The scalar layer derives ordinary equality and reconnects to existing modulo
reasoning only through explicitly active bridges.

Generic inference engine:

```text
unchanged
```

Verified full suite:

```text
988 passed in 61.87s
```

### 状態

完了

---

# Phase 16 completion boundary

Phase 16 で実装しないもの:

```text
general symbolic integer arithmetic solver
general scalar congruence closure
symbolic divisibility / nondivisibility solver
symbolic inequalities
automatic parity inference from arbitrary arithmetic formulas
arbitrary coefficient modulus enumeration
theorem quantifiers over integer variables
existential scalar witnesses
canonical scalar normal form
first-class coefficient indeterminacy
first-class ±α indeterminacy
Toda bracket value sets
Toda bracket indeterminacy
general Toda bracket syntax
automatic typed map validation
semantic cycle detection
```

`max_rounds` は引き続き generic safety bound。

Current Phase 16 concrete scalar + Phase 15 bridge family は finite known term
set 上で genuine `FIXED_POINT`。

---

# Phase 17 boundary

Roadmap dependency:

```text
Abelian group expression
↓
Homomorphism reasoning
↓
Set / subgroup reasoning
↓
Coset / modulo
↓
Symbolic scalar constraints
↓
Indeterminacy
↓
Toda bracket
```

Phase 16 完了により、次の自然な Phase は:

```text
Phase 17: Indeterminacy
```

Candidate actual needs:

```text
α = kβ + γ
k odd
```

を単なる constraint ではなく possible representative family として保持する
仕組み、

```text
±α
```

の sign uncertainty、

coefficient uncertainty と existing coset / modulo layer の接続。

Phase 17 でも actual mathematical theorem / notation を先に固定し、
Toda bracket 全体を先取りしない。

Generic engine の変更は actual indeterminacy theorem が current rule
language で表現できないと実証された場合のみ。

---

# Current verified status

Full suite at Phase 16 completion:

```powershell
python -m pytest -q
```

```text
988 passed in 61.87s
```

Phase 16-9 focused:

```text
3 passed in 2.10s
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
