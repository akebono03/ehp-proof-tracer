# ehp_proof 設計メモ

この文書は Phase 14 完了時点の current architecture / semantics /
design boundary を正本としてまとめる。

過去の development log にある「未実装」「今後の課題」は historical
statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
homotopy / EHP domain inference rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / set / subgroup statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

基本原則:

```text
new mathematical knowledge
=
new domain InferenceRule
```

generic engine を変更するのは actual mathematical rule が current rule
language では正しく表現できないと実証された場合のみ。

---

# 2. Algebra layer

責務:

- finitely generated abelian groups
- relation matrices
- integer lattices
- HNF / SNF
- homomorphisms
- kernel / image / cokernel
- subgroup / quotient
- exact sequence
- finite extension candidates

群は:

```text
Z^r ⊕ finite torsion
```

として扱う。

```text
Im(f)=Ker(g)
```

という exactness と:

```text
B / Im(f) ≅ Im(g)
```

という abstract isomorphism を区別する。

proof-level role identity は algebra layer の `Subgroup` equality そのもの
には埋め込まない。

2-primary / odd-primary / Toda / EHP theorem semantics は algebra layer に
埋め込まない。

---

# 3. EHP data layer

責務:

- E/H/P maps
- repository data
- generator correspondence
- source / target group selection
- EHP segment construction

一般群論計算は algebra layer に委譲する。

---

# 4. Expression layer

Current expression tree:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
└── Suspension
```

Generic map identity:

```text
MapSymbol
```

`MapSymbol` 自体は homotopy-element `Expression` ではない。

`MapApplication(map, expression)` が proof-expression layer の `f(α)` を
表す。

Expression layer は数学的 syntax / structure を lossless に保持する。

Expression layer は以下を担当しない:

- theorem applicability
- stable-range judgement
- dimension validation
- zero proof
- equality proof
- commutative sorting
- associative flattening
- theorem-aware normalization
- repeated-sum expansion
- subgroup membership validation

---

# 5. Phase 12 Sum semantics

`Sum` は:

```python
Sum(
  left=alpha,
  right=beta,
)
```

として binary tree を保持する。

重要:

```text
Sum(alpha,beta)
!=structural
Sum(beta,alpha)
```

また:

```text
Sum(Sum(alpha,beta),gamma)
!=structural
Sum(alpha,Sum(beta,gamma))
```

数学的可換性 / 結合性は Expression equality ではなく
`RelationType.EQUALITY` で表す。

---

# 6. Multiple / additive inverse semantics

Current additive inverse representation:

```text
-α
=
Multiple(-1, α)
```

専用 `Inverse` node は導入しない。

`Multiple` と `Sum` は structural に区別する。

```text
Multiple(2,α)
!=structural
Sum(α,α)
```

同様に:

```text
Multiple(0,α)
!=structural
Zero()
```

---

# 7. Zero-addition boundary

以下は lossless に表現できる:

```text
α+0
0+α
```

ただし:

```text
α+0 !=structural α
0+α !=structural α
```

constructor normalization は行わない。

zero identity theorem も current implementation には含めない。

---

# 8. Relation / Proof layer

Current `RelationType`:

```text
EQUALITY
ZERO
ORDER
```

ZERO:

```python
Relation(
  lhs=x,
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

ORDER は exact positive finite additive order を表す。

Known composition equality:

```python
Relation(
  lhs=Composition(
    left=alpha,
    right=beta,
  ),
  rhs=gamma,
  relation_type=RelationType.EQUALITY,
)
```

Additive equality も同じ generic `RelationType.EQUALITY` を使う。

Set / subgroup relation は専用 statement class を使い、element expression
equality と同じ `Relation` に無理に押し込まない。

`ProofStep` fields:

```text
conclusion
premises
rule
note
inference_rule
```

provenance は `premises` と `inference_rule` に保持する。

---

# 9. Generic inference engine

Engine の責務:

```text
match
bind
apply
deduplicate
iterate
trace
```

`InferenceRule`:

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

`match_guard` は domain validity を generic engine へ埋め込まないための
hook。

---

# 10. Matching semantics

- exhaustive deterministic premise assignment
- `PatternVariable`
- `VariableBinding`
- shared-binding consistency
- same available-step index を one assignment 内で再利用しない

同一 conclusion は ordinary Python equality で duplicate reject。

Mathematical equality は duplicate identity へ自動反映しない。

Phase 14 ではこの性質を role-aware subgroup identity に積極的に利用する。

---

# 11. Fixed-point semantics

Derived conclusions は next round の premises になる。

Termination:

```text
FIXED_POINT
MAX_ROUNDS
```

`round_count` は productive round 数。

`max_rounds` は safety bound であり semantic cycle detector ではない。

One round 内で生成された conclusion は、その same round 内で別 rule の
fresh premise として逐次再利用しない。

---

# 12. Generic relation rules

```text
x=y
→ y=x
```

```text
x=y
y=z
→ x=z
```

```text
x=0
y=x
→ y=0
```

EHP / ORDER / Suspension / Freudenthal / composition / Hopf / additive /
homomorphism reasoning が同じ generic relation layer を共有する。

Set / subgroup relation closure は `SubgroupEqualityStatement` /
`SubsetStatement` 用の domain rules として分離する。

---

# 13. Phase 6 EHP rule family

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
```

Generic engine に EHP-specific branch は追加しない。

---

# 14. Phase 7 ORDER rule family

```text
ord(α)=n
↓
nα=0
```

Conclusion は:

```python
Relation(
  lhs=Multiple(
    coefficient=n,
    expression=alpha,
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

---

# 15. Phase 8 Suspension rule family

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension は distinct nested expressions を無限に生成し得る。

必要に応じて staged / bounded execution を使う。

原則:

```text
mathematical applicability
≠
execution scope
```

---

# 16. Phase 9 Freudenthal design

Expression-level:

```text
Suspension(expression)
```

と theorem-level suspension-map statement を分離する。

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

Outside:

```text
stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

---

# 17. Phase 10 composition representation

Known composition relation:

```text
α∘β = γ
```

は `Composition` を含む ordinary generic equality として保持する。

Known zero composition は generic ZERO へ bridge できる。

---

# 18. Suspension-composition functoriality

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

Generic Suspension preservation:

```text
α∘β=γ
↓
E(α∘β)=Eγ
```

との間を generic symmetry / transitivity で接続する。

---

# 19. Phase 10 termination boundary

`functoriality + symmetry` で structural depth が増え得る。

したがって unrestricted fixed-point termination は仮定しない。

Finite representative task は staged execution を使う。

---

# 20. Phase 11 generalized Hopf representation

Generalized Hopf fact:

```text
H(α)=β
```

の `β` は `Expression`。

integer-only に限定しない。

Known fact は literature provenance を保持できる。

---

# 21. Phase 11 theorem boundary

Implemented:

```text
H(α)=β
→ HopfCompositionLawStatement(α,β)
```

```text
HopfCompositionLawStatement(α,β)
→ H(α∘Eγ)=β∘Eγ
```

```text
H(x)=y
y=0
→ H(x)=0
```

```text
EHPZeroCompositionStatement(E,H)
→ H(Eα)=0
```

Not inferred:

```text
H(x)=0 → x=0
```

Phase 14 で kernel membership が導入されたため、適切な GroupMap /
MapSymbol bridge を明示した場合には:

```text
H(x)=0
→ x∈Ker(H)
```

を表現できる。

ただし:

```text
x∈Ker(H)
→ x∈Im(E)
```

には Exactness による明示的 role bridge が必要。

---

# 22. Phase 11 termination boundary

Hopf law / formula family は recursive structural growth を持ち得る。

```text
H(α)=β
↓
Law(α,β)
↓
H(α∘Eγ)=β∘Eγ
↓
...
```

したがって unrestricted fixed-point-safe とは扱わない。

---

# 23. Phase 12 additive inverse rule

Rule semantics:

```text
α+(-α)=0
```

where:

```text
-α = Multiple(-1, α)
```

Expression constructor は zero へ normalize しない。

---

# 24. Phase 12 commutativity

Rule semantics:

```text
α+β = β+α
```

Conclusion は generic equality。

重要:

```text
mathematical equality
≠
structural equality
```

reverse direction 用の専用 rule は作らない。

既存 `equality_symmetry_inference_rule()` を再利用する。

---

# 25. Phase 12 associativity

Rule semantics:

```text
(α+β)+γ = α+(β+γ)
```

両辺は structurally distinct nested `Sum`。

Reverse direction は generic equality symmetry を再利用する。

No flattening.

No associative canonical form.

---

# 26. Phase 12 ORDER bridge

一般の:

```text
nα ↔ α+...+α
```

を実装しない。

最小 bridge:

```text
α+α = 2α
```

のみを explicit equality として導入。

---

# 27. Phase 12 representative / normalization boundary

Representative additive scenario は:

```text
additive inverse
commutativity
associativity
ORDER
double / repeated-Sum bridge
generic equality
generic ZERO
```

を同一 knowledge state で扱う。

Structural distinction:

```text
α+β                    !=structural β+α
(α+β)+γ                !=structural α+(β+γ)
2α                     !=structural α+α
α+0                    !=structural α
0+α                    !=structural α
```

この差異は bug ではない。

---

# 28. Phase 13 MapSymbol / MapApplication

Proof-expression layer の generic map identity:

```text
MapSymbol
```

map application:

```text
MapApplication(map, expression)
```

Algebra `GroupMap` とは責務を分離する。

同じ name だけで自動的に identical semantics としない。

---

# 29. Phase 13 HomomorphismStatement

Homomorphism theorem fact:

```text
HomomorphismStatement(map=f)
```

Map existence と homomorphism theorem fact は別。

Known `GroupMap` が存在するだけで arbitrary proof `MapSymbol` に
homomorphism law を適用しない。

---

# 30. Phase 13 homomorphism laws

Explicit homomorphism fact のもとで:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

を concrete rule scope で扱う。

Known ZERO preservation:

```text
x=0
+
Homomorphism(f)
↓
f(x)=0
```

---

# 31. Phase 13 E bridge

`E` の generic homomorphism additivity を existing Suspension syntax に
接続する。

Generic:

```text
MapApplication(E, α+β)
=
MapApplication(E,α)+MapApplication(E,β)
```

Bridge:

```text
Suspension(α+β)
=
Suspension(α)+Suspension(β)
```

Freudenthal `SuspensionMapStatement` とは分離する。

---

# 32. Phase 13 H / P theorem scope

Mathematically the EHP `H` and generalized Hopf `H` refer to the same
generalized Hopf map.

しかし proof-expression `MapSymbol` は source / target / ambient group を
保持しない。

そのため unrestricted:

```text
Homomorphism(H)
Homomorphism(P)
```

は automatic activation しない。

---

# 33. Phase 13 ORDER integration

```text
ord(α)=n
→ nα=0
```

と homomorphism preservation を接続し:

```text
n f(α)=0
```

を導出できる。

ただし:

```text
ord(f(α))=n
```

は導出しない。

annihilation と exact order を区別する。

---

# 34. Phase 13 termination / scope boundary

Concrete rule factories による finite scope。

導入しない:

```text
arbitrary expression enumeration
recursive map distribution
universal map congruence
automatic Homomorphism(H)
automatic Homomorphism(P)
```

Current finite family は `FIXED_POINT` に到達する。

---

# 35. Phase 14 statement layer

Phase 14 は proof-level set / subgroup reasoning を導入する。

First-class statement:

```text
MembershipStatement
SubsetStatement
SubgroupEqualityStatement
```

Notation:

```text
α ∈ A
A ⊆ B
A = B
```

これらは algebra-layer `Subgroup` object と proof-level mathematical role
を接続するための theorem statement。

---

# 36. MembershipStatement semantics

```python
MembershipStatement(
  element=alpha,
  subgroup=A,
)
```

`element` は `Expression`。

`subgroup` は Phase 14 完了時点では `SubgroupTerm`。

Basic semantics:

```text
α∈A
A⊆B
↓
α∈B
```

---

# 37. SubsetStatement semantics

```python
SubsetStatement(
  subset=A,
  superset=B,
)
```

`subset` / `superset` は `SubgroupTerm`。

Containment relation は statement として明示する。

Computed element-set containment を proof layer で暗黙に再計算して theorem
fact としない。

---

# 38. SubgroupEqualityStatement semantics

```python
SubgroupEqualityStatement(
  left=A,
  right=B,
)
```

`left` / `right` は `SubgroupTerm`。

重要:

```text
SubgroupEqualityStatement(A,B)
```

は theorem-level mathematical statement。

Python object equality:

```text
A == B
```

とは意味が異なる。

---

# 39. Role-aware subgroup references

Phase 14 の central design decision。

```python
@dataclass(frozen=True)
class ImageSubgroupReference:
  group_map: GroupMap
```

```python
@dataclass(frozen=True)
class KernelSubgroupReference:
  group_map: GroupMap
```

それぞれ:

```text
reference.subgroup
```

で existing algebra-layer subgroup を取得できる。

しかし role-aware reference equality は group map / role identity を保持する。

したがって:

```text
ImageSubgroupReference(E).subgroup
==
KernelSubgroupReference(H).subgroup
```

であっても:

```text
ImageSubgroupReference(E)
!=
KernelSubgroupReference(H)
```

となり得る。

この差異は bug ではなく provenance preservation のための仕様。

---

# 40. SubgroupTerm

Phase 14 完了時点:

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

以下の statement はすべて `SubgroupTerm` を受け取る:

```text
MembershipStatement.subgroup
SubsetStatement.subset
SubsetStatement.superset
SubgroupEqualityStatement.left
SubgroupEqualityStatement.right
```

既存 raw `Subgroup` API は維持する。

---

# 41. Legacy subgroup-value compatibility

Existing raw subgroup use:

```text
MembershipStatement(
  element=α,
  subgroup=f.kernel_subgroup(),
)
```

は引き続き表現可能。

ただし new role-aware helper は reference を返す。

Legacy raw subgroup value equality は ordinary Python equality に従うため、
image / kernel の provenance が collapse する場合がある。

New theorem paths では role-aware reference を優先する。

---

# 42. Kernel membership helper

```text
kernel_membership_statement(
  element=α,
  group_map=f,
)
```

は:

```text
MembershipStatement(
  element=α,
  subgroup=KernelSubgroupReference(f),
)
```

を生成する。

Kernel role identity を helper boundary で保持する。

---

# 43. Image membership helper

```text
image_membership_statement(
  element=α,
  group_map=f,
)
```

は:

```text
MembershipStatement(
  element=α,
  subgroup=ImageSubgroupReference(f),
)
```

を生成する。

Image role identity を helper boundary で保持する。

---

# 44. Kernel membership ↔ mapped ZERO

Given explicit algebra `GroupMap` and proof `MapSymbol`:

```text
α∈Ker(f)
↓
f(α)=0
```

and:

```text
f(α)=0
↓
α∈Ker(f)
```

を explicit inference rule で接続する。

Important boundary:

```text
GroupMap.name == MapSymbol.name
```

だけから automatic semantic identity を生成しない。

Caller が explicit pair を rule factory に渡す。

---

# 45. Phase 14 Exactness role-aware bridge

Phase 14-13 以降:

```text
Exactness(f,g)
```

から:

```text
ImageSubgroupReference(f)
=
KernelSubgroupReference(g)
```

を導出する。

旧:

```text
f.image_subgroup()
=
g.kernel_subgroup()
```

という raw value equality だけに collapse しない。

この変更により:

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

が theorem provenance を保ったまま成立する。

---

# 46. Membership subset propagation

Generic subgroup-domain rule:

```text
α∈A
A⊆B
↓
α∈B
```

Shared `PatternVariable` binding により A は同一 `SubgroupTerm` でなければ
ならない。

Underlying subgroup values が等しいだけでは match しない。

---

# 47. Membership equality propagation

```text
α∈A
A=B
↓
α∈B
```

reverse membership:

```text
α∈B
A=B
↓
α∈A
```

も同じ rule で扱う。

Guard は `SubgroupTerm` structural identity を使う。

Underlying raw subgroup equality へ自動 unwrap しない。

---

# 48. Role-aware propagation boundary

Suppose:

```text
Image(E).subgroup == Kernel(H).subgroup
```

but:

```text
Image(E) != Kernel(H)
```

Then:

```text
α∈Image(E)
Kernel(H)⊆B
```

から:

```text
α∈B
```

を導出しない。

Likewise:

```text
α∈Image(E)
Kernel(H)=B
```

から equality membership transport を行わない。

Role bridge は explicit theorem statement が必要。

---

# 49. Subgroup equality symmetry

```text
A=B
↓
B=A
```

`SubgroupTerm` structural binding を使用する。

専用 underlying-value comparison は行わない。

---

# 50. Subgroup equality transitivity

```text
A=B
B=C
↓
A=C
```

shared middle binding `B` は同じ `SubgroupTerm` でなければならない。

```text
A=Image(E)
Kernel(H)=C
```

かつ:

```text
Image(E).subgroup == Kernel(H).subgroup
```

だけでは transitivity chain を接続しない。

Explicit:

```text
Image(E)=Kernel(H)
```

が必要。

---

# 51. Subset transitivity

```text
A⊆B
B⊆C
↓
A⊆C
```

Middle term は shared `SubgroupTerm` binding。

Underlying value equality だけでは middle を接続しない。

---

# 52. Equality → subset

Minimal rule:

```text
A=B
↓
A⊆B
```

Reverse containment 専用 rule は作らない。

Existing subgroup equality symmetry:

```text
A=B
↓
B=A
```

と組み合わせて:

```text
B⊆A
```

を得る。

---

# 53. Mutual subset → equality

```text
A⊆B
B⊆A
↓
A=B
```

これは subgroup equality の集合論的 antisymmetry bridge。

Pattern binding は role-aware structural identity を使う。

---

# 54. Phase 14 relation closure

Current finite relation family:

```text
A=B
→ B=A
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
A=B
→ A⊆B
```

```text
A⊆B
B⊆A
→ A=B
```

Cycle は存在するが new structural term constructor は生成しない。

Finite active `SubgroupTerm` set では ordinary duplicate rejection により
`FIXED_POINT`。

---

# 55. Phase 14 representative scenario

Representative initial facts:

```text
Exactness(E,H)
H(α)=0
```

where mapped ZERO is represented by proof `MapApplication`.

Rules:

```text
Exactness → role-aware subgroup equality
mapped ZERO → kernel membership
membership across subgroup equality
membership across subset
subgroup equality symmetry
subgroup equality transitivity
subset transitivity
equality → subset
mutual subset → equality
```

Representative conclusions:

```text
Im(E)=Ker(H)
Ker(H)=Im(E)
α∈Ker(H)
α∈Im(E)
Im(E)⊆Ker(H)
Ker(H)⊆Im(E)
```

---

# 56. Phase 14 provenance requirements

Exactness equality:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

must have direct premise:

```text
exactness_step
```

Kernel membership:

```text
H(α)=0
↓
α∈Ker(H)
```

must have direct premise:

```text
mapped_zero_step
```

Image membership:

```text
α∈Ker(H)
+
Im(E)=Ker(H)
↓
α∈Im(E)
```

must have direct premises equal to those two intermediate `ProofStep` values.

Provenance chain を source facts へ flatten しない。

---

# 57. Phase 14 theorem boundary

Critical non-inference:

```text
Image(E).subgroup == Kernel(H).subgroup
↛
Image(E)=Kernel(H)
```

Therefore without Exactness:

```text
H(α)=0
→ α∈Ker(H)
```

but not:

```text
α∈Im(E)
```

This preserves distinction:

```text
algebraic value equality
≠
theorem-level role equality
```

---

# 58. Phase 14 termination boundary

Set/subgroup closure contains cycles:

```text
A=B
→ A⊆B

A=B
→ B=A
→ B⊆A

A⊆B
B⊆A
→ A=B
```

However no rule constructs new nested subgroup terms.

For finite known terms, relation possibilities are finite.

Thus current Phase 14 representative family reaches genuine:

```text
FIXED_POINT
```

This does not prove arbitrary future set-rule families terminate.

`max_rounds` remains generic safety bound.

---

# 59. Phase 14 completion criteria

Phase 14 completion criteria:

1. first-class `MembershipStatement`.
2. first-class `SubsetStatement`.
3. first-class `SubgroupEqualityStatement`.
4. raw `Subgroup` compatibility.
5. `ImageSubgroupReference`.
6. `KernelSubgroupReference`.
7. role-aware distinction even for equal subgroup values.
8. `SubgroupTerm` formalization.
9. kernel membership helper.
10. image membership helper.
11. kernel membership → mapped ZERO.
12. mapped ZERO → kernel membership.
13. Exactness → role-aware `Im(f)=Ker(g)`.
14. membership across subset.
15. membership across subgroup equality.
16. subgroup equality symmetry.
17. subgroup equality transitivity.
18. subset transitivity.
19. equality → subset.
20. mutual subset → equality.
21. role mismatch reject regressions.
22. representative Exactness + membership + closure scenario.
23. provenance regression.
24. theorem boundary regression without Exactness.
25. finite relation cycle reaches `FIXED_POINT`.
26. generic engine unchanged.
27. full regression PASS.

Current verified full suite:

```text
921 passed in 62.89s
```

---

# 60. Phase 14 non-goals

Phase 14 では実装しない:

- subgroup equality reflexivity as premise-free theorem generation
- subset reflexivity as premise-free theorem generation
- arbitrary set union
- arbitrary set intersection
- complement
- arbitrary set-valued expressions
- explicit image preimage witness generation
- coset / modulo
- symbolic scalar constraints
- first-class `±α` indeterminacy
- Toda bracket value set
- Toda bracket indeterminacy
- theorem quantifier language
- existential witness language
- automatic typed map validation
- unrestricted `Homomorphism(H)`
- unrestricted `Homomorphism(P)`
- semantic cycle detection
- theorem-aware subgroup canonicalization

---

# 61. Current limitations

## 61.1 Conclusion identity

ordinary Python equality。

No theorem-aware canonical equivalence.

## 61.2 Alternative proofs

same conclusion の multiple candidate derivations は execution trace に
残り得るが、knowledge state は first accepted step を保持する。

## 61.3 Pattern language

Structured pattern variables and shared bindings exist.

Fully general recursive unification language ではない。

## 61.4 Search complexity

Exhaustive premise assignment can grow combinatorially.

Indexing / pruning / semi-naive evaluation は未実装。

## 61.5 Termination

`max_rounds` は safety bound。

Semantic cycle detection ではない。

Some structural theorem families can grow without bound.

Phase 14 relation closure itself is finite for finite active `SubgroupTerm`
values.

## 61.6 Map typing

Proof-level `MapSymbol` has no source / target / ambient homotopy-group typing.

## 61.7 Set/subgroup scope

First-class membership / subset / subgroup equality are implemented.

Not implemented:

```text
coset
modulo
union
intersection
complement
preimage witness
general set-valued expression
```

## 61.8 Arithmetic / indeterminacy

Not implemented:

```text
symbolic scalar coefficient
odd/even scalar constraints
first-class ±
general indeterminacy
Toda bracket
```

---

# 62. Phase 15 boundary

Roadmap dependency order:

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

Phase 14 で Set / subgroup reasoning の最小基盤が完成した。

次の自然な Phase:

```text
Phase 15: Coset / modulo reasoning
```

Initial actual needs candidates:

```text
α + A
α mod A
α ≡ β mod A
```

Potential theorem connections:

```text
α ≡ β mod A
↔
α-β ∈ A
```

or additive-group notation consistent with current `Sum` / `Multiple(-1,β)`.

ただし actual mathematical use case を先に固定する。

Phase 15 でも:

```text
symbolic scalar constraints
general indeterminacy
Toda bracket
```

を先取りしない。

Role-aware subgroup reference は coset denominator / modulus subgroup にも
必要なら再利用する。

Generic engine の変更は actual coset/modulo theorem が current rule
language では正しく表現できないと実証された場合のみ。

---

# 63. Testing principle

Domain rule family を追加するときは:

1. expression / representation test
2. single-rule semantic test
3. invalid premise / applicability test
4. multi-round integration
5. generic-rule reconnection
6. provenance test
7. representative scenario
8. termination / scope boundary if relevant
9. full regression

を基本とする。

---

# 64. Documentation policy

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

Historical limitation は historical statement として保持する。

Current specification は latest README / design を優先する。
