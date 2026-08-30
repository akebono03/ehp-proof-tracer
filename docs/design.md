# ehp_proof 設計メモ

この文書は Phase 16 完了時点の current architecture / semantics /
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
proof-level expression / scalar / set / subgroup / modulo statements
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

Modulo / scalar constraint / Toda / EHP theorem semantics も algebra layer
には埋め込まない。

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

Symbolic scalar syntax:

```text
ScalarSymbol
```

`MapSymbol` 自体は homotopy-element `Expression` ではない。

`MapApplication(map, expression)` が proof-expression layer の `f(α)` を
表す。

`ScalarSymbol` は `Multiple.coefficient` に利用できる。

Expression layer は数学的 syntax / structure を lossless に保持する。

Expression layer は以下を担当しない:

- theorem applicability
- scalar constraint solving
- stable-range judgement
- dimension validation
- zero proof
- equality proof
- commutative sorting
- associative flattening
- theorem-aware normalization
- repeated-sum expansion
- subgroup membership validation
- coset equality proof
- quotient / modulo normalization

---

# 5. Sum semantics

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

# 6. Multiple / additive inverse / symbolic scalar semantics

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

```text
Multiple(0,α)
!=structural
Zero()
```

Symbolic coefficient:

```text
Multiple(
  coefficient=ScalarSymbol("k"),
  expression=β,
)
```

は:

```text
kβ
```

を structural に表す。

`ScalarSymbol("k")` は値を決定しない。

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

Additive / composition / symbolic scalar multiple equality は generic
`RelationType.EQUALITY` を使う。

Set / subgroup / modulo / scalar constraints は必要に応じて専用 statement
class を使い、element expression equality と同じ `Relation` に無理に
押し込まない。

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

Role-aware subgroup / modulo semantics と scalar statement identity はこの
structural identity を利用する。

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
homomorphism / scalar reasoning が同じ generic relation layer を共有する。

Set / subgroup / modulo / scalar-constraint statements は domain rules として
必要に応じて分離する。

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

Conclusion は `Multiple(n, α)` を使う。

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

# 17. Phase 10 composition design

Known composition relation:

```text
α∘β = γ
```

は `Composition` を含む ordinary generic equality として保持する。

Known zero composition は generic ZERO へ bridge できる。

Suspension-composition functoriality:

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

Generic Suspension preservation と equality symmetry / transitivity で接続。

Structural depth が増える family は unrestricted fixed-point-safe と扱わない。

---

# 18. Phase 11 generalized Hopf design

Generalized Hopf fact:

```text
H(α)=β
```

の `β` は `Expression`。

Implemented theorem boundary:

```text
H(x)=0
↛
x=0
```

Phase 14 の explicit kernel membership bridge が active なら:

```text
H(x)=0
→ x∈Ker(H)
```

を扱える。

`x∈Im(E)` へ進むには Exactness による role-aware bridge が必要。

---

# 19. Phase 12 additive design

Current additive laws are theorem rules, not constructor normalization:

```text
α+(-α)=0
α+β=β+α
(α+β)+γ=α+(β+γ)
α+α=2α
```

General repeated-sum normalization は行わない。

---

# 20. Phase 13 homomorphism design

Proof-level map syntax:

```text
MapSymbol
MapApplication
HomomorphismStatement
```

Map existence と homomorphism theorem fact を分離。

Explicit homomorphism fact のもとで:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

を導出する。

Untyped unrestricted `Homomorphism(H)` / `Homomorphism(P)` は automatic に
active にしない。

---

# 21. Phase 14 statement layer

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
を接続する theorem statement。

---

# 22. MembershipStatement semantics

```python
MembershipStatement(
  element=alpha,
  subgroup=A,
)
```

`element` は `Expression`。

`subgroup` は `SubgroupTerm`。

Basic semantics:

```text
α∈A
A⊆B
↓
α∈B
```

---

# 23. SubsetStatement semantics

```python
SubsetStatement(
  subset=A,
  superset=B,
)
```

`subset` / `superset` は `SubgroupTerm`。

Containment relation は statement として明示する。

Computed element-set containment を proof layer で暗黙に theorem fact としない。

---

# 24. SubgroupEqualityStatement semantics

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

# 25. Role-aware subgroup references

```text
ImageSubgroupReference
KernelSubgroupReference
```

それぞれ existing algebra-layer subgroup を `reference.subgroup` で取得する。

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

この差異は provenance preservation のための仕様。

---

# 26. SubgroupTerm

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

以下で共通利用する:

```text
MembershipStatement.subgroup
SubsetStatement.subset
SubsetStatement.superset
SubgroupEqualityStatement.left
SubgroupEqualityStatement.right
Coset.subgroup
ModuloStatement.modulus
```

Raw `Subgroup` compatibility は維持する。

---

# 27. Kernel / image membership helpers

```text
kernel_membership_statement(α,f)
→ α∈KernelSubgroupReference(f)
```

```text
image_membership_statement(α,f)
→ α∈ImageSubgroupReference(f)
```

Mapped ZERO bridge:

```text
f(α)=0
↔
α∈Ker(f)
```

は explicit rule として扱う。

---

# 28. Exactness role-aware bridge

```text
Exactness(f,g)
↓
ImageSubgroupReference(f)
=
KernelSubgroupReference(g)
```

Underlying raw subgroup equality だけで theorem-level role equality を生成しない。

---

# 29. Phase 14 subgroup closure

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

Finite active `SubgroupTerm` set では ordinary duplicate rejection により
`FIXED_POINT`。

---

# 30. Phase 14 theorem boundary

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

This preserves:

```text
algebraic value equality
≠
theorem-level role equality
```

---

# 31. Phase 15 Coset semantics

Phase 15 introduces structural coset syntax:

```text
Coset(
  representative=α,
  subgroup=A,
)
```

Intended notation:

```text
α + A
```

`Coset` is not made theorem-aware by custom Python equality.

Mathematical coset equality is represented separately.

---

# 32. ModuloStatement semantics

```text
ModuloStatement(
  left=α,
  right=β,
  modulus=A,
)
```

Intended notation:

```text
α ≡ β mod A
```

`ModuloStatement` is a dedicated theorem statement.

It is not encoded as ordinary `RelationType.EQUALITY` and is not reduced to
`Coset.__eq__`.

---

# 33. Difference representation for modulo

Current subtraction syntax:

```text
α-β
=
Sum(
  left=α,
  right=Multiple(-1,β),
)
```

Phase 15 does not introduce a new subtraction / inverse expression class.

No simplification such as:

```text
α-0 → α
```

is performed automatically.

---

# 34. Modulo ↔ difference membership

Implemented theorem bridge:

```text
α ≡ β mod A
↔
α-β ∈ A
```

Reverse rule は explicit structural difference form のみを受理する。

---

# 35. CosetEqualityStatement semantics

```text
CosetEqualityStatement(
  left=Coset(α,A),
  right=Coset(β,A),
)
```

This is theorem-level equality between cosets.

Phase 15 implements:

```text
α ≡ β mod A
↔
Coset(α,A)=Coset(β,A)
```

Reverse bridge requires:

```text
left.subgroup == right.subgroup
```

at proof-level `SubgroupTerm` identity.

---

# 36. Equality → modulo scope

Mathematically:

```text
α=β
→
α≡β mod A
```

for any applicable subgroup `A`.

Implementation scope does not enumerate all possible moduli.

Concrete rule factory:

```text
equality_implies_modulo_inference_rule(modulus=A)
```

This separates:

```text
mathematical applicability
```

from:

```text
active inference scope
```

---

# 37. ZERO → modulo scope

Explicitly selected modulus:

```text
α=0
→
α≡0 mod A
```

No reverse rule:

```text
α≡0 mod A
↛
α=0
```

---

# 38. Subgroup equality modulo propagation

Explicit theorem equality transports modulus:

```text
A=B
α≡β mod A
→
α≡β mod B
```

The bridge compares role-aware `SubgroupTerm` identity, not only raw subgroup
values.

---

# 39. Exactness → modulo transport

Phase 14 and Phase 15 connect through:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

and:

```text
α≡β mod Ker(H)
+
Im(E)=Ker(H)
↓
α≡β mod Im(E)
```

No special Exactness-modulo shortcut rule is added.

---

# 40. Subset → modulo design

Mathematically:

```text
A⊆B
α≡β mod A
→
α≡β mod B
```

Current design reuses:

```text
modulo
→ difference membership
→ subset propagation
→ modulo
```

instead of adding a dedicated shortcut.

---

# 41. Coset modulus transport design

No dedicated direct coset-transport rule is required.

Current bridges compose:

```text
coset equality
→ modulo
→ subgroup equality transport
→ modulo
→ coset equality
```

---

# 42. Phase 15 representative scenario

Representative initial facts:

```text
Exactness(E,H)
α=β
β=0
```

with equality / ZERO modulo bridges scoped to `Ker(H)`.

The scenario derives corresponding `Ker(H)` and `Im(E)` modulo, membership, and
coset-equality facts while preserving role identity and reaches `FIXED_POINT`.

---

# 43. Phase 15 provenance policy

For duplicate conclusions:

```text
same conclusion
← path A
← path B
```

knowledge state keeps the first accepted proof step.

Alternative candidate derivations remain observable in duplicate-rejected trace
data.

Phase 15 does not redesign the knowledge state into a proof DAG containing all
coequal proofs.

---

# 44. Phase 15 role boundary

Critical non-inference:

```text
Image(E).subgroup == Kernel(H).subgroup
↛
Modulo(...,Image(E)) → Modulo(...,Kernel(H))
```

Explicit theorem equality is required.

This extends:

```text
same algebraic value
≠
same proof-level role
```

into modulo reasoning.

---

# 45. Phase 15 equality / ZERO inference-scope boundary

Equality and ZERO facts do not automatically enumerate modulo facts.

Without active concrete rules:

```text
equality_implies_modulo_inference_rule(modulus=A)
zero_implies_modulo_inference_rule(modulus=A)
```

knowledge containing only equality / ZERO does not generate arbitrary
`ModuloStatement`s.

---

# 46. Phase 15 termination boundary

Current cycles:

```text
Modulo
↔ difference membership
```

```text
Modulo
↔ coset equality
```

```text
Modulo mod A
↔ Modulo mod B
```

through explicit subgroup equality.

For finite known expressions and active `SubgroupTerm` values, current Phase 15
statement possibilities are finite enough for ordinary duplicate rejection to
reach genuine `FIXED_POINT`.

---

# 47. Phase 16 symbolic scalar representation

Phase 16 introduces minimal symbolic scalar support.

Structural scalar:

```text
ScalarSymbol("k")
```

can occur in:

```text
Multiple(k,β)
```

and therefore in:

```text
α = kβ + γ
```

No general symbolic arithmetic engine is introduced.

---

# 48. Phase 16 parity statements

First-class statements:

```text
OddScalarStatement(
  scalar=k,
)
```

```text
EvenScalarStatement(
  scalar=k,
)
```

These are theorem-level parity facts.

Structural scalar identity alone does not imply parity.

---

# 49. ScalarCongruenceStatement semantics

```text
ScalarCongruenceStatement(
  scalar=k,
  residue=r,
  modulus=m,
)
```

represents:

```text
k ≡ r mod m
```

Current use is intentionally minimal and concrete.

Phase 16 does not add a general congruence arithmetic solver.

---

# 50. Odd / even → mod two bridge

Implemented:

```text
k odd
→
k≡1 mod 2
```

and:

```text
k even
→
k≡0 mod 2
```

as explicit inference rules.

The odd rule does not accept an `EvenScalarStatement`.

The even rule does not accept an `OddScalarStatement`.

---

# 51. Symbolic additive equality

The form:

```text
α = kβ + γ
```

uses existing:

```text
RelationType.EQUALITY
Multiple
Sum
ScalarSymbol
```

No new equality relation type is introduced.

Generic equality symmetry / transitivity can operate on the resulting
structured expressions.

---

# 52. Phase 16 order-two scalar bridge

Current main scalar theorem:

```text
ord(β)=2
k≡1 mod 2
↓
kβ=β
```

Conclusion:

```text
Relation(
  lhs=Multiple(k,β),
  rhs=β,
  relation_type=EQUALITY,
)
```

Applicability boundaries:

```text
ord(β)=3
↛
kβ=β
```

and:

```text
k≡0 mod 2
↛
kβ=β
```

The rule is deliberately specific to the actual current order-two need.

---

# 53. Phase 16 modulo connection

No scalar-specific modulo rule is added.

Connection is:

```text
scalar constraint
↓
ordinary equality
↓
existing equality→modulo bridge
```

Thus:

```text
k odd
ord(β)=2
↓
kβ=β
```

followed by explicitly active:

```text
equality_implies_modulo_inference_rule(modulus=A)
```

gives:

```text
kβ≡β mod A
```

This preserves layering and avoids Phase 16 duplication of Phase 15 semantics.

---

# 54. Phase 16 exactness / role-aware integration

Representative connection:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

together with:

```text
kβ≡β mod Ker(H)
```

produces:

```text
kβ≡β mod Im(E)
```

through the existing role-aware modulo propagation rule.

No scalar-specific Exactness rule is introduced.

---

# 55. Phase 16 membership / coset integration

Once symbolic modulo facts exist, existing Phase 15 rules apply unchanged:

```text
kβ≡β mod A
↔
kβ-β∈A
```

and:

```text
kβ≡β mod A
↔
[kβ]=[β] mod A
```

The symbolic coefficient requires no special membership / coset implementation.

---

# 56. Phase 16 representative scenario

Initial facts:

```text
k odd
ord(β)=2
Exactness(E,H)
```

Rules connect:

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

and:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

therefore:

```text
kβ≡β mod Im(E)
```

then:

```text
difference membership
coset equality
```

for both role-aware moduli.

Representative run reaches genuine:

```text
FIXED_POINT
```

---

# 57. Phase 16 provenance boundary

Provenance chain must remain explicit:

```text
OddScalarStatement
↓ parity rule
ScalarCongruenceStatement
```

```text
ORDER + ScalarCongruenceStatement
↓ order bridge
symbolic equality
```

```text
symbolic equality
↓ explicit equality→modulo
kernel modulo
```

```text
Exactness
↓
subgroup equality
```

```text
kernel modulo + subgroup equality
↓
image modulo
```

Alternative derivations of an equal symbolic membership conclusion obey the
existing policy:

```text
first accepted ProofStep
+
duplicate-rejected alternative trace
```

No Phase 16 proof-store redesign is performed.

---

# 58. Phase 16 termination boundary

Current scalar rules:

```text
Odd → congruence
Even → congruence
order-two + congruence → equality
```

do not recursively increase structural term depth.

Combined with the finite Phase 15 bridge family:

```text
Modulo ↔ membership
Modulo ↔ coset equality
role-aware modulus transport
```

the current representative scenario has a finite conclusion set and reaches:

```text
FIXED_POINT
```

The terminal round satisfies:

```text
new_steps == ()
```

This does not claim arbitrary future symbolic arithmetic systems terminate.

`max_rounds` remains a generic safety bound.

---

# 59. Phase 16 inference-scope boundary

Critical boundary:

With active Phase 16 scalar/order rules:

```text
k odd
ord(β)=2
```

can derive:

```text
k≡1 mod 2
kβ=β
```

but cannot derive:

```text
kβ≡β mod A
```

without explicit activation of:

```text
equality_implies_modulo_inference_rule(modulus=A)
```

Likewise, modulo / membership / coset facts are not generated merely because
they are mathematical consequences available under other possible rule sets.

Principle:

```text
mathematical applicability
≠
active inference scope
```

---

# 60. Phase 16 completion criteria

Phase 16 completion criteria:

1. `ScalarSymbol` supports symbolic coefficient representation.
2. symbolic scalar can occur in `Multiple`.
3. `α=kβ+γ` is structurally representable.
4. symbolic equality uses generic equality reasoning.
5. first-class `OddScalarStatement`.
6. first-class `EvenScalarStatement`.
7. first-class `ScalarCongruenceStatement`.
8. odd → congruent one modulo two.
9. even → congruent zero modulo two.
10. parity mismatch rejection.
11. order-two + one-mod-two → `kβ=β`.
12. non-order-two rejection.
13. zero-mod-two rejection.
14. odd + order-two multi-round integration.
15. symbolic equality reconnects to Phase 15 only through explicit modulo bridge.
16. symbolic modulo works with raw `Subgroup`.
17. symbolic modulo works with role-aware `SubgroupTerm`.
18. Exactness transports `Ker(H)` modulo to `Im(E)` modulo.
19. existing membership bridge works for symbolic difference.
20. existing coset bridge works for symbolic representatives.
21. representative Phase 16 scenario reaches `FIXED_POINT`.
22. direct provenance chain is preserved.
23. alternative derivation keeps first accepted provenance.
24. duplicate alternative remains in duplicate-rejected trace.
25. bidirectional Phase 15/16 bridge family terminates.
26. terminal round has `new_steps == ()`.
27. no modulo-scope crossing without explicit equality→modulo rule.
28. generic inference engine unchanged.
29. full regression PASS.

Current verified full suite:

```text
988 passed in 61.87s
```

---

# 61. Phase 16 non-goals

Phase 16 では実装しない:

- general symbolic integer arithmetic solver
- general congruence closure
- arbitrary modular arithmetic over symbolic coefficients
- symbolic divisibility / nondivisibility solver
- scalar inequalities
- automatic parity extraction from arbitrary formulas
- premise-free integer-domain theorem generation
- arbitrary modulus enumeration
- theorem quantifiers over symbolic integers
- existential scalar witness generation
- canonical coefficient normal form
- first-class coefficient indeterminacy set
- first-class `±α` indeterminacy
- Toda-bracket value set
- Toda-bracket indeterminacy
- general higher Toda-bracket syntax
- automatic typed map validation
- semantic cycle detection

---

# 62. Current limitations

## 62.1 Conclusion identity

ordinary Python equality。

No theorem-aware canonical equivalence.

## 62.2 Alternative proofs

same conclusion の multiple candidate derivations は execution trace に
残り得るが、knowledge state は first accepted step を保持する。

## 62.3 Pattern language

Structured pattern variables and shared bindings exist.

Fully general recursive symbolic unification language ではない。

## 62.4 Search complexity

Exhaustive premise assignment can grow combinatorially.

Indexing / pruning / semi-naive evaluation は未実装。

## 62.5 Termination

`max_rounds` は safety bound。

Semantic cycle detection ではない。

Repeated Suspension / recursive composition / recursive Hopf family など、
structural depth を増加させる family は別途 bounded / staged execution が必要。

Current Phase 16 concrete scalar family は finite known term set で
`FIXED_POINT`。

## 62.6 Map typing

Proof-level `MapSymbol` has no complete source / target / ambient homotopy-group
typing。

## 62.7 Additive normalization

No canonical commutative / associative / scalar normal form。

## 62.8 Modulo normalization

No canonical representative selection。

No quotient arithmetic normalization。

## 62.9 Symbolic scalar arithmetic

First-class symbolic scalar / parity / mod-two congruence is implemented.

General integer constraint solving is not implemented.

## 62.10 Indeterminacy

First-class coefficient / sign / coset-valued indeterminacy object is not yet
implemented.

---

# 63. Phase 17 boundary

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

Phase 16 で symbolic scalar constraints の最小基盤が完成したため、次の
自然な Phase は:

```text
Phase 17: Indeterminacy
```

Initial actual needs は実際の theorem form から決める。

Candidate forms:

```text
α = kβ + γ
k odd
```

を「k の具体値を選ばない family」として扱うこと、

```text
±α
```

のような sign uncertainty、

および既存 modulo / coset layer と接続する coefficient uncertainty。

Phase 17 でも uncertainty を premature に collapse しないことを優先する。

Toda bracket 全体を先取りせず、actual indeterminacy theorem に必要な最小
representation から開始する。

Generic engine の変更は actual indeterminacy theorem が current rule
language で正しく表現できないと実証された場合のみ。

---

# 64. Testing principle

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

# 65. Documentation policy

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
