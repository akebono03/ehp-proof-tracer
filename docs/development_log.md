# ehp_proof 開発記録

この文書は Phase 14 完了時点までの開発履歴を、現在の実装と矛盾しない
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

Phase 9 は actual theorem family として Freudenthal reasoning を追加。

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

Representative EHP + Toda + Suspension scenario、provenance、
termination boundary を固定。

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

Representative Hopf + EHP scenario と provenance regression、
recursive structural-growth boundary を固定。

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

---

# Phase 14-1：MembershipStatement

First-class statement:

```text
MembershipStatement(
  element=α,
  subgroup=A,
)
```

Notation:

```text
α∈A
```

Raw algebra `Subgroup` を直接保持できる最小表現から開始。

### 状態

完了

---

# Phase 14-2：SubsetStatement

First-class containment:

```text
SubsetStatement(
  subset=A,
  superset=B,
)
```

Notation:

```text
A⊆B
```

### 状態

完了

---

# Phase 14-3：membership subset propagation

追加:

```text
α∈A
A⊆B
↓
α∈B
```

Shared pattern binding により同じ subgroup term を接続。

Provenance を保持。

### 状態

完了

---

# Phase 14-4：SubgroupEqualityStatement

First-class proof-level subgroup equality:

```text
SubgroupEqualityStatement(
  left=A,
  right=B,
)
```

Notation:

```text
A=B
```

Algebra object equality と theorem statement を分離。

### 状態

完了

---

# Phase 14-5：subgroup equality membership propagation

```text
α∈A
A=B
↓
α∈B
```

および reverse direction を同じ rule で実装。

### 状態

完了

---

# Phase 14-6〜14-8：kernel / mapped-zero bridge

Kernel membership helper を既存 `GroupMap.kernel_subgroup()` と接続。

Rules:

```text
α∈Ker(f)
↓
f(α)=0
```

```text
f(α)=0
↓
α∈Ker(f)
```

Algebra `GroupMap` と proof `MapSymbol` を explicit rule arguments で接続。

Map name だけによる automatic identification は導入しない。

### 状態

完了

---

# Phase 14-9：Exactness → subgroup equality

Exactness:

```text
Exactness(f,g)
```

から:

```text
Im(f)=Ker(g)
```

という proof-level `SubgroupEqualityStatement` を導出する bridge を導入。

初期段階では raw subgroup value を使ったため、image / kernel role
provenance が collapse し得る境界が見つかった。

### 状態

完了

---

# Phase 14-10：image/kernel role identity と provenance

問題:

```text
f.image_subgroup() == g.kernel_subgroup()
```

の場合、raw `Subgroup` equality では:

```text
α∈Im(f)
```

と:

```text
α∈Ker(g)
```

が同一 `MembershipStatement` として collapse し得る。

これは mathematical subgroup value と theorem role を区別できない。

Phase 14-10 ではこの問題を明示し、role-aware representation の必要性を
regression 固定。

### 状態

完了

---

# Phase 14-11：role-aware subgroup reference

追加:

```text
ImageSubgroupReference(group_map=f)
KernelSubgroupReference(group_map=g)
```

両方とも:

```text
reference.subgroup
```

で existing algebra `Subgroup` を参照する。

しかし role-aware reference 自体は distinct。

Example:

```text
Image(E).subgroup == Kernel(H).subgroup
```

でも:

```text
Image(E) != Kernel(H)
```

を保証。

### 状態

完了

---

# Phase 14-12：membership helper の role-aware migration

`kernel_membership_statement()` を:

```text
MembershipStatement(
  element=α,
  subgroup=KernelSubgroupReference(f),
)
```

へ移行。

`image_membership_statement()` を:

```text
MembershipStatement(
  element=α,
  subgroup=ImageSubgroupReference(f),
)
```

へ移行。

Mapped-zero → kernel-membership bridge も helper を経由するため
role-aware conclusion を生成。

同じ underlying subgroup value でも image membership と kernel membership
が distinct に保持されることを固定。

Phase 14-12 verified:

```text
901 passed
```

### 状態

完了

---

# Phase 14-13：Exactness role-aware Image–Kernel equality bridge

Exactness rule を raw subgroup equality から role-aware equality へ移行。

Before:

```text
f.image_subgroup()
=
g.kernel_subgroup()
```

After:

```text
ImageSubgroupReference(f)
=
KernelSubgroupReference(g)
```

Representative:

```text
g(α)=0
↓
α∈Ker(g)

Exactness(f,g)
↓
Im(f)=Ker(g)

↓
α∈Im(f)
```

Generic `subgroup_equality_membership_propagation_inference_rule()` を再利用。

新しい special-case exactness-membership rule は追加しなかった。

Phase 14-13 full suite:

```text
901 passed in 60.54s
```

### 状態

完了

---

# Phase 14-14：SubgroupTerm formalization / role-aware propagation boundary

Formalized:

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

以下を `SubgroupTerm` 対応へ正式化:

```text
MembershipStatement.subgroup
SubsetStatement.subset
SubsetStatement.superset
SubgroupEqualityStatement.left
SubgroupEqualityStatement.right
```

Role-aware propagation を確認:

```text
α∈Ker(H)
Ker(H)⊆Im(E)
↓
α∈Im(E)
```

```text
α∈Ker(H)
Im(E)=Ker(H)
↓
α∈Im(E)
```

Boundary:

```text
Image(E).subgroup == Kernel(H).subgroup
```

だけでは shared binding として同一視しない。

Full suite:

```text
907 passed in 60.39s
```

### 状態

完了

---

# Phase 14-15：subgroup equality / subset closure

追加 rule:

```text
A=B
↓
B=A
```

```text
A=B
B=C
↓
A=C
```

```text
A⊆B
B⊆C
↓
A⊆C
```

Middle term は role-aware `SubgroupTerm` shared binding。

Underlying subgroup equality だけでは chain を接続しない。

Symmetry / transitivity による cycles があっても finite known terms
上では duplicate rejection により `FIXED_POINT`。

Full suite:

```text
913 passed in 65.30s
```

### 状態

完了

---

# Phase 14-16：equality / subset interconnection

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

専用 `A=B → B⊆A` rule は作らず、既存 symmetry と composition。

Role identity mismatch reject regression を追加。

Cyclic rule set:

```text
equality
↔
mutual subset
```

でも new structural term を生成しないため finite `FIXED_POINT`。

Full suite:

```text
919 passed in 61.95s
```

### 状態

完了

---

# Phase 14-17：representative scenario / provenance / termination boundary

Production code は変更せず、Phase 14 全体を一つの representative
fixed-point run に統合。

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

Provenance regression で direct intermediate premises を固定。

Theorem boundary regression では Exactness rule を active set から外し:

```text
H(α)=0
→ α∈Ker(H)
```

までは得るが:

```text
α∈Im(E)
```

や:

```text
Im(E)=Ker(H)
```

は得ないことを固定。

Underlying subgroup value equality だけでは theorem role bridge を生成しない。

Terminal round:

```text
new_steps == ()
```

を確認し genuine `FIXED_POINT` を固定。

Full suite:

```text
921 passed in 62.89s
```

### 状態

完了

---

# Phase 14-18：documentation / formal completion

README.md:

```text
current capabilities / current status
```

へ Phase 14 set/subgroup reasoning を反映。

docs/design.md:

```text
current architecture / semantics / boundaries
```

へ role-aware subgroup references、`SubgroupTerm`、Exactness bridge、
closure、termination boundary を反映。

docs/development_log.md:

```text
chronological history
```

として Phase 14-1〜14-18 を記録。

Phase 14 completion status:

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

# Phase 14 completion summary

Phase 14 により proof layer は:

```text
α∈A
A⊆B
A=B
α∈Ker(f)
α∈Im(f)
```

を first-class に扱えるようになった。

さらに:

```text
mapped ZERO
↓
kernel membership
```

```text
Exactness
↓
role-aware Im(f)=Ker(g)
```

```text
membership + equality/subset
↓
membership transport
```

```text
subgroup equality symmetry / transitivity
subset transitivity
equality ↔ mutual containment
```

を existing generic inference engine 上に実装。

重要な成果:

```text
same underlying subgroup
≠
same mathematical role
```

を proof representation に導入できた。

これにより image / kernel provenance を維持したまま EHP exactness と
element membership reasoning が接続された。

Generic engine に set/subgroup-specific branch は追加していない。

### 状態

完了

---

# Phase 14 completion boundary

Phase 14 で実装しないもの:

```text
subgroup reflexivity theorem generation
subset reflexivity theorem generation
union
intersection
complement
preimage witness
coset
modulo
symbolic scalar constraints
first-class ± indeterminacy
Toda bracket value set
Toda bracket indeterminacy
automatic typed map validation
semantic cycle detection
```

`max_rounds` は引き続き generic safety bound。

Current Phase 14 set/subgroup relation family は finite known terms 上で
`FIXED_POINT`。

---

# Phase 15 boundary

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

Phase 14 完了により、次の自然な Phase は:

```text
Phase 15: Coset / modulo reasoning
```

Candidate actual forms:

```text
α+A
α mod A
α≡β mod A
```

Potential bridge:

```text
α≡β mod A
↔
α-β∈A
```

ただし current additive representation:

```text
α-β
=
Sum(
  α,
  Multiple(-1,β),
)
```

との整合を保つ。

Role-aware `SubgroupTerm` は denominator / modulus subgroup に必要なら
再利用する。

Phase 15 でも actual mathematical need を先に固定し、
symbolic scalar constraints / general indeterminacy / Toda bracket を
先取りしない。

Generic engine の変更は actual coset/modulo theorem が current rule
language で表現できないと実証された場合のみ。

---

# Current verified status

Full suite at Phase 14 completion:

```powershell
python -m pytest -v
```

```text
921 passed in 62.89s
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
