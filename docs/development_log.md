# ehp_proof 開発記録

この文書は Phase 15 完了時点までの開発履歴を、現在の実装と矛盾しない
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

## Phase 12-1：Sum minimum representation

追加:

```text
Sum(left,right)
```

Semantics:

```text
α+β
```

Binary tree structure を lossless に保持。

## Phase 12-2：Sum structural equality / nested representation

```text
Sum(α,β) != Sum(β,α)
```

```text
(α+β)+γ
!=structural
α+(β+γ)
```

## Phase 12-3：Multiple / Zero boundary

```text
Multiple(2,α)
!=structural
Sum(α,α)
```

```text
Multiple(0,α)
!=structural
Zero()
```

## Phase 12-4：inverse minimum representation

```text
-α
=
Multiple(-1,α)
```

専用 `Inverse` class は導入しない。

## Phase 12-5：zero addition representation / boundary

```text
α+0
0+α
```

を表現可能にしつつ constructor simplification は行わない。

## Phase 12-6：additive inverse rule

```text
α+(-α)=0
```

## Phase 12-7：commutativity

```text
α+β = β+α
```

## Phase 12-8：associativity

```text
(α+β)+γ = α+(β+γ)
```

## Phase 12-9：ORDER reasoning integration

Phase 7 ORDER rule:

```text
ord(α)=n
↓
nα=0
```

は変更しない。

最小 bridge:

```text
α+α = 2α
```

を追加。

Representative:

```text
ord(α)=2
↓
2α=0

α+α=2α
↓
α+α=0
```

## Phase 12-10〜12-11：representative / provenance / termination

Additive inverse、commutativity、associativity、ORDER、generic equality /
ZERO を同一 environment で統合。

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

## Phase 13-1〜13-3：generic map representation

```text
MapSymbol
MapApplication
HomomorphismStatement
```

を導入。

Algebra `GroupMap` と proof-level map syntax を分離。

Map existence と homomorphism theorem fact を分離。

## Phase 13-4〜13-7：homomorphism laws

Explicit homomorphism fact のもとで:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

Known ZERO preservation も追加。

## Phase 13-8〜13-9：E / Suspension bridge

Generic `E` homomorphism reasoning を existing `Suspension` syntax に接続。

Freudenthal theorem-level `SuspensionMapStatement` とは分離。

## Phase 13-10：H / P boundary

Mathematical H semantics は Phase 11 generalized Hopf map と整合。

ただし untyped `MapSymbol` へ unrestricted:

```text
Homomorphism(H)
Homomorphism(P)
```

を自動導入しない。

## Phase 13-11：ORDER integration

```text
ord(α)=n
↓
nα=0
```

と homomorphism preservation を接続して:

```text
n f(α)=0
```

を導出。

ただし:

```text
ord(f(α))=n
```

とはしない。

## Phase 13-12：representative / provenance / termination

Homomorphism laws、ORDER、generic ZERO、E / Suspension を同一 inference
environment で統合。

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

Generic inference engine は Phase 14 を通じて変更しない。

## Phase 14-1〜14-4：statement layer

追加:

```text
MembershipStatement
SubsetStatement
SubgroupEqualityStatement
```

Notation:

```text
α∈A
A⊆B
A=B
```

## Phase 14-5〜14-10：kernel / image / Exactness connection

Mapped ZERO と kernel membership を接続:

```text
f(α)=0
↔
α∈Ker(f)
```

Image membership helper も追加。

Exactness は:

```text
Im(f)=Ker(g)
```

を proof-level theorem statement として生成。

## Phase 14-11〜14-14：role-aware subgroup reference

追加:

```text
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

Critical distinction:

```text
Image(E).subgroup == Kernel(H).subgroup
```

でも:

```text
Image(E) != Kernel(H)
```

を保証。

Membership helpers / Exactness conclusion を role-aware term へ移行。

## Phase 14-15：subgroup equality / subset closure

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

Middle term は shared `SubgroupTerm` binding。

Underlying subgroup equality だけでは chain を接続しない。

## Phase 14-16：equality / subset interconnection

追加:

```text
A=B
↓
A⊆B
```

Equality symmetry と組み合わせ:

```text
A=B
↓
B=A
↓
B⊆A
```

逆 bridge:

```text
A⊆B
B⊆A
↓
A=B
```

## Phase 14-17：representative scenario / provenance / termination boundary

Initial facts:

```text
Exactness(E,H)
H(α)=0
```

Representative chain:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
H(α)=0
↓
α∈Ker(H)
```

```text
Im(E)=Ker(H)
+
α∈Ker(H)
↓
α∈Im(E)
```

Equality/subset closure:

```text
Im(E)=Ker(H)
→ Ker(H)=Im(E)
→ Im(E)⊆Ker(H)
→ Ker(H)⊆Im(E)
```

Theorem boundary regression では Exactness rule が無ければ image membership
へ進まないことを固定。

Terminal round:

```text
new_steps == ()
```

を確認し genuine `FIXED_POINT`。

## Phase 14-18：documentation / formal completion

Phase 14 completion:

```text
921 passed in 62.89s
```

Generic inference engine:

```text
unchanged
```

### 状態

完了

---

# Phase 15：Coset / modulo reasoning

Phase 15 は Phase 14 の `SubgroupTerm` と additive syntax の上に、coset /
congruence reasoning の最小層を追加した。

基本原則:

```text
mathematical meaning
≠
low-level structural equality
```

Generic inference engine は Phase 15 を通じて変更しない。

---

# Phase 15-1：Coset minimum representation

追加:

```python
@dataclass(frozen=True)
class Coset:
  representative: Expression
  subgroup: SubgroupTerm
```

Intended notation:

```text
α + A
```

Structural representation のみ。

`Coset` は `Expression` subclass にせず、quotient-side structural term として
保持。

Python equality は structural equality のまま。

Role-aware subgroup term を保存する regression を追加。

Full suite:

```text
924 passed in 63.16s
```

### 状態

完了

---

# Phase 15-2：ModuloStatement minimum representation

追加:

```python
@dataclass(frozen=True)
class ModuloStatement:
  left: Expression
  right: Expression
  modulus: SubgroupTerm
```

Intended notation:

```text
α ≡ β mod A
```

Dedicated statement とし、generic equality や coset structural equality へ
押し込まない。

Structural boundary:

```text
ModuloStatement(α,β,A)
!=structural
ModuloStatement(β,α,A)
```

Role-aware modulus identity を保持。

Full suite:

```text
928 passed in 61.66s
```

### 状態

完了

---

# Phase 15-3：difference membership bridge

Current additive difference syntax:

```text
α-β
=
Sum(
  left=α,
  right=Multiple(-1,β),
)
```

追加:

```text
α ≡ β mod A
→
α-β ∈ A
```

```text
α-β ∈ A
→
α ≡ β mod A
```

Reverse bridge は `Sum(..., Multiple(-1,...))` の structural form を
`match_guard` で確認。

Reject:

```text
α∈A
α+β∈A
α+2β∈A
```

Bidirectional bridge は duplicate rejection により finite `FIXED_POINT`。

Full suite:

```text
934 passed in 66.48s
```

### 状態

完了

---

# Phase 15-4：coset equality bridge

追加:

```python
@dataclass(frozen=True)
class CosetEqualityStatement:
  left: Coset
  right: Coset
```

Theorem-level bridge:

```text
α ≡ β mod A
↔
α+A = β+A
```

`Coset.__eq__` は theorem-aware に変更しない。

Reverse bridge は左右 coset の `SubgroupTerm` が同じ場合のみ発火。

Therefore:

```text
Image(E).subgroup == Kernel(H).subgroup
```

でも role mismatch の coset equality は modulo に変換しない。

Full suite:

```text
940 passed in 60.04s
```

### 状態

完了

---

# Phase 15-5：ZERO / equality connection

追加:

```text
α=β
→
α≡β mod A
```

```text
α=0
→
α≡0 mod A
```

Implementation scope:

```text
equality_implies_modulo_inference_rule(modulus=A)
zero_implies_modulo_inference_rule(modulus=A)
```

Modulus は rule factory で explicit に選ぶ。

Equality / ZERO だけから arbitrary subgroup moduli を enumerate しない。

Non-expression equality は reject。

No reverse:

```text
α≡β mod A
↛
α=β
```

```text
α≡0 mod A
↛
α=0
```

`ZERO → EQUALITY` の general bridge は Phase 15 のために追加しない。

Full suite:

```text
946 passed in 63.12s
```

### 状態

完了

---

# Phase 15-6：subgroup equality modulo propagation

追加:

```text
A=B
α≡β mod A
→
α≡β mod B
```

同じ rule で reverse direction も扱う。

Role-aware matching:

```text
ModuloStatement.modulus
==
SubgroupEqualityStatement.left/right
```

Underlying `.subgroup` value equality だけでは発火しない。

Exactness integration:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
α≡β mod Ker(H)
↓
α≡β mod Im(E)
```

No special Exactness-modulo shortcut rule。

Subset propagation も dedicated shortcut を追加せず:

```text
modulo
→ difference membership
→ membership subset propagation
→ modulo
```

で composition。

Full suite:

```text
951 passed in 64.17s
```

### 状態

完了

---

# Phase 15-7：representative scenario

Production code は変更せず、Phase 14〜15-6 の既存 rules を一つの
fixed-point run に統合。

Initial facts:

```text
Exactness(E,H)
α=β
β=0
```

Representative chain:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
α=β
↓
α≡β mod Ker(H)
↓
α≡β mod Im(E)
├→ α-β∈Im(E)
└→ α+Im(E)=β+Im(E)
```

ZERO branch:

```text
β=0
↓
β≡0 mod Ker(H)
↓
β≡0 mod Im(E)
```

Phase 14 equality→subset / membership-subset propagation も同じ knowledge state
に参加。

Main path provenance を direct intermediate `ProofStep` で固定。

Alternative provenance の優先順位はこの Phase では過剰に固定しない。

Full suite:

```text
952 passed in 66.81s
```

### 状態

完了

---

# Phase 15-8：provenance / termination boundary

Production code は変更しない。

## Alternative derivation regression

同じ conclusion:

```text
α-β∈Im(E)
```

に複数 path:

```text
α≡β mod Im(E)
→ difference membership
```

```text
α-β∈Ker(H)
Ker(H)⊆Im(E)
→ membership subset propagation
```

がある場合を検証。

Current engine policy:

```text
first accepted ProofStep
```

を knowledge state に保持。

Alternative candidate は:

```text
candidate_steps
duplicate_rejected_steps
```

に trace として保持。

## Bidirectional termination regression

同時 active:

```text
Modulo ↔ difference membership
Modulo ↔ coset equality
Modulo mod A ↔ Modulo mod B
```

でも finite known term set 上で genuine:

```text
FIXED_POINT
```

を確認。

Expected finite representative statement families:

```text
2 ModuloStatement
2 MembershipStatement
2 CosetEqualityStatement
```

程度に閉じ、structural depth を増殖させないことを固定。

## Role boundary regression

```text
Image(E).subgroup == Kernel(H).subgroup
```

だけでは:

```text
mod Ker(H)
→ mod Im(E)
```

へ進まない。

Explicit `SubgroupEqualityStatement` が必要。

## Equality / ZERO scope regression

Active modulo-producing rule が無い knowledge:

```text
α=β
β=0
```

から `ModuloStatement` / modulo-derived membership / coset equality を生成しない。

Rule activation と modulus selection が explicit scope であることを固定。

## Termination result

Phase 15 current cycles は `MAX_ROUNDS` boundary ではなく genuine finite
`FIXED_POINT` boundary として仕様化。

Terminal round:

```text
new_steps == ()
```

Full suite:

```text
956 passed in 64.09s
```

### 状態

完了

---

# Phase 15-9：documentation / formal completion

README.md:

```text
current capabilities / current status
```

へ Phase 15 Coset / modulo reasoning を反映。

docs/design.md:

```text
current architecture / semantics / boundaries
```

へ以下を正式化:

- `Coset`
- `ModuloStatement`
- `CosetEqualityStatement`
- difference-membership bridge
- equality / ZERO modulo scope
- role-aware modulus transport
- Exactness integration
- alternative provenance policy
- finite fixed-point termination boundary

docs/development_log.md:

```text
chronological history
```

として Phase 15-1〜15-9 を記録。

Phase 15 completion status:

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

# Phase 15 completion summary

Phase 15 により proof layer は:

```text
α+A
α≡β mod A
α+A=β+A
α-β∈A
```

を扱えるようになった。

Main theorem bridges:

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

```text
α=0
→
α≡0 mod A
```

```text
A=B
α≡β mod A
→
α≡β mod B
```

Phase 14 integration:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
↓
role-aware modulo transport
```

重要な設計成果:

```text
same underlying subgroup value
≠
same modulus role
```

と:

```text
mathematical congruence
≠
structural Python equality
```

を維持したまま quotient / modulo reasoning を追加できた。

Current Phase 15 cyclic rules は new structural depth を生成せず finite
`FIXED_POINT` に到達。

Generic engine に modulo-specific branch は追加していない。

### 状態

完了

---

# Phase 15 completion boundary

Phase 15 で実装しないもの:

```text
premise-free modulo reflexivity theorem generation
dedicated modulo symmetry / transitivity theorem family
dedicated coset equality symmetry / transitivity theorem family
theorem-aware Coset.__eq__
quotient representative canonicalization
theorem-aware subtraction normalization
α-0 → α constructor simplification
arbitrary modulus enumeration
automatic modulo generation from every equality / ZERO fact
general quotient-group proof object
quotient homomorphism theorem family
symbolic scalar constraints
symbolic parity / divisibility solver
first-class coefficient indeterminacy
±α indeterminacy object
Toda bracket value set
Toda bracket indeterminacy
theorem quantifier language
existential witness language
automatic typed map validation
semantic cycle detection
```

`max_rounds` は引き続き generic safety bound。

Phase 15 current bridge family itself は finite known term set 上で genuine
`FIXED_POINT`。

---

# Phase 16 boundary

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

Phase 15 完了により、次の自然な Phase は:

```text
Phase 16: Symbolic scalar constraints
```

Candidate actual forms:

```text
α = kβ + γ
k odd
```

```text
k ∈ Z
k ≡ 1 mod 2
```

Potential minimal representations:

- symbolic integer / scalar term
- parity statement
- divisibility / congruence constraint for scalars
- `Multiple(k,β)` と symbolic scalar の接続
- scalar constraint を premise とする theorem rule

Phase 16 でも actual mathematical need を先に固定し、general
indeterminacy / Toda bracket を先取りしない。

Generic engine の変更は actual symbolic-scalar theorem が current rule
language で表現できないと実証された場合のみ。

---

# Current verified status

Full suite at Phase 15 completion:

```powershell
python -m pytest -v
```

```text
956 passed in 64.09s
```

Representative long-lived regression:

```text
tests/test_stable_rules.py::test_phase9_inference_scope_termination_and_theorem_boundary
PASSED
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
chronological implementation history

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
