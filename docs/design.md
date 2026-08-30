# ehp_proof 設計メモ

この文書は Phase 15 完了時点の current architecture / semantics /
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
proof-level expression / set / subgroup / modulo statements
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

Modulo / Toda / EHP theorem semantics も algebra layer には埋め込まない。

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

Additive / composition equality は generic `RelationType.EQUALITY` を使う。

Set / subgroup / modulo relation は専用 statement class を使い、element
expression equality と同じ `Relation` に無理に押し込まない。

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

Role-aware subgroup / modulo semantics はこの structural identity を意図的に
利用する。

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

Set / subgroup / modulo statements は domain rules として分離する。

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

それぞれ `reference.subgroup` で existing algebra-layer subgroup を取得する。

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

`Coset` is not made theorem-aware by custom Python equality.

Structural identity remains:

```text
same representative
+
same SubgroupTerm
```

Mathematical coset equality is represented separately.

---

# 32. ModuloStatement semantics

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

`ModuloStatement` is a dedicated theorem statement.

It is not encoded as ordinary `RelationType.EQUALITY` and is not reduced to
`Coset.__eq__`.

This preserves:

```text
mathematical congruence
≠
low-level structural equality
```

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

Forward rule constructs the explicit current difference syntax.

Reverse rule accepts only an element structurally of the form:

```text
Sum(
  left=α,
  right=Multiple(-1,β),
)
```

Therefore the following are rejected as modulo differences:

```text
α∈A
α+β∈A
α+2β∈A
```

Generic nested recursive unification was not added; existing `match_guard` /
`conclusion_builder` are sufficient.

---

# 35. CosetEqualityStatement semantics

```python
@dataclass(frozen=True)
class CosetEqualityStatement:
  left: Coset
  right: Coset
```

This is theorem-level equality between cosets.

Python structural equality between `Coset` values remains unchanged.

Phase 15 implements:

```text
α ≡ β mod A
↔
Coset(α,A)=Coset(β,A)
```

The reverse bridge requires:

```text
left.subgroup == right.subgroup
```

at proof-level `SubgroupTerm` identity.

Underlying raw subgroup value equality alone is insufficient.

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

Instead a concrete rule factory is created with an explicit modulus:

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

and prevents unrestricted subgroup enumeration.

Non-expression equality facts are rejected by the bridge.

---

# 37. ZERO → modulo scope

Explicitly selected modulus:

```text
α=0
→
α≡0 mod A
```

through:

```text
zero_implies_modulo_inference_rule(modulus=A)
```

No reverse rule:

```text
α≡0 mod A
↛
α=0
```

No Phase-15-specific global:

```text
ZERO → EQUALITY
```

conversion is introduced.

---

# 38. Subgroup equality modulo propagation

Explicit theorem equality transports modulus:

```text
A=B
α≡β mod A
→
α≡β mod B
```

and reverse direction through the same rule.

The bridge compares:

```text
ModuloStatement.modulus
```

with:

```text
SubgroupEqualityStatement.left/right
```

as role-aware `SubgroupTerm` values.

It does not compare only `.subgroup` raw values.

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

The generic existing role-aware subgroup equality is reused.

---

# 40. Subset → modulo design

Mathematically:

```text
A⊆B
α≡β mod A
→
α≡β mod B
```

No dedicated shortcut rule is added.

Existing composition suffices:

```text
α≡β mod A
→ α-β∈A
```

```text
α-β∈A
A⊆B
→ α-β∈B
```

```text
α-β∈B
→ α≡β mod B
```

This preserves explicit theorem paths and avoids redundant rule families.

---

# 41. Coset modulus transport design

Likewise, no dedicated:

```text
A=B
α+A=β+A
→ α+B=β+B
```

shortcut rule is needed.

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
```

```text
α≡β mod Im(E)
├→ α-β∈Im(E)
└→ Coset(α,Im(E))=Coset(β,Im(E))
```

ZERO branch:

```text
β=0
↓
β≡0 mod Ker(H)
↓
β≡0 mod Im(E)
```

Existing Phase 14 equality→subset / membership-subset rules can coexist in the
same knowledge state.

---

# 43. Phase 15 provenance semantics

Derived facts retain:

```text
ProofRule.INFERENCE
inference_rule
premises
```

Representative direct provenance includes:

```text
Exactness(E,H)
↓
Im(E)=Ker(H)
```

```text
α=β
↓
α≡β mod Ker(H)
```

```text
α≡β mod Ker(H)
+
Im(E)=Ker(H)
↓
α≡β mod Im(E)
```

```text
α≡β mod Im(E)
↓
Coset(α,Im(E))=Coset(β,Im(E))
```

Provenance chain を source facts へ flatten しない。

---

# 44. Alternative derivation boundary

A single conclusion may have multiple derivations.

Example:

```text
α-β∈Im(E)
```

may arise from:

```text
α≡β mod Im(E)
→ difference membership
```

or:

```text
α-β∈Ker(H)
Ker(H)⊆Im(E)
→ membership subset propagation
```

Current knowledge-state policy:

```text
first accepted ProofStep
```

is retained for an equal conclusion.

Alternative applications remain visible in execution traces:

```text
candidate_steps
duplicate_rejected_steps
```

Phase 15 does not redesign the knowledge state to store all alternative proof
objects as coequal canonical proofs.

---

# 45. Phase 15 role boundary

Critical non-inference:

```text
Image(E).subgroup == Kernel(H).subgroup
↛
Modulo(...,Image(E)) → Modulo(...,Kernel(H))
```

Explicit theorem equality is required.

Likewise:

```text
Coset(α,Image(E)) = Coset(β,Kernel(H))
```

is not accepted by the reverse coset-to-modulo bridge merely because underlying
subgroup values happen to match.

This extends the Phase 14 principle:

```text
same algebraic value
≠
same proof-level role
```

into quotient / modulo reasoning.

---

# 46. Phase 15 equality / ZERO inference-scope boundary

Equality and ZERO facts do not automatically enumerate modulo facts.

Without active concrete rules:

```text
equality_implies_modulo_inference_rule(modulus=A)
zero_implies_modulo_inference_rule(modulus=A)
```

knowledge containing only:

```text
α=β
β=0
```

does not generate `ModuloStatement`.

Rule activation / modulus selection remains caller / scenario controlled.

---

# 47. Phase 15 termination boundary

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

These rules do not create arbitrary new nested expressions or fresh subgroup
terms.

For finite known expressions and active `SubgroupTerm` values, the possible
Phase-15 statement set is finite enough for ordinary duplicate rejection to
reach genuine:

```text
FIXED_POINT
```

Phase 15 representative termination does not rely on `MAX_ROUNDS`.

This differs from repeated Suspension / recursive Hopf / some functoriality
families that can increase structural depth indefinitely.

No semantic cycle detector is added.

---

# 48. Phase 15 completion criteria

Phase 15 completion criteria:

1. first-class structural `Coset`.
2. first-class `ModuloStatement`.
3. first-class `CosetEqualityStatement`.
4. `Coset.subgroup` uses `SubgroupTerm`.
5. `ModuloStatement.modulus` uses `SubgroupTerm`.
6. raw subgroup compatibility.
7. image / kernel role-aware modulus compatibility.
8. structural identity separated from theorem equality.
9. modulo → difference membership.
10. difference membership → modulo.
11. reverse difference bridge rejects non-difference structure.
12. modulo → coset equality.
13. coset equality → modulo for same proof-level modulus.
14. role mismatch reject for coset equality.
15. equality → modulo with explicit modulus scope.
16. ZERO → modulo with explicit modulus scope.
17. modulo does not imply ordinary equality.
18. modulo-zero does not imply ZERO.
19. explicit subgroup equality transports modulo facts.
20. underlying raw subgroup value alone does not transport role-aware modulo.
21. Exactness → role-aware subgroup equality → modulo transport.
22. representative Phase 14 + 15 scenario.
23. direct provenance regression.
24. alternative derivation / duplicate trace regression.
25. equality / ZERO rule-activation boundary regression.
26. bidirectional Phase 15 cycles terminate at genuine `FIXED_POINT`.
27. terminal round has `new_steps == ()`.
28. generic inference engine unchanged.
29. full regression PASS.

Current verified full suite:

```text
956 passed in 64.09s
```

---

# 49. Phase 15 non-goals

Phase 15 では実装しない:

- premise-free modulo reflexivity generation
- dedicated modulo symmetry theorem family
- dedicated modulo transitivity theorem family
- dedicated coset equality symmetry / transitivity family
- theorem-aware `Coset.__eq__`
- quotient representative canonicalization
- theorem-aware subtraction normalization
- `α-0 → α` constructor simplification
- arbitrary subgroup / modulus enumeration
- automatic modulo generation from every equality / ZERO fact
- general quotient-group proof object
- quotient homomorphism theorem family
- symbolic scalar constraints
- symbolic parity / divisibility solver
- first-class coefficient indeterminacy
- `±α` indeterminacy object
- Toda bracket value set
- Toda bracket indeterminacy
- theorem quantifier language
- existential witness language
- automatic typed map validation
- semantic cycle detection

---

# 50. Current limitations

## 50.1 Conclusion identity

ordinary Python equality。

No theorem-aware canonical equivalence。

## 50.2 Alternative proofs

same conclusion の multiple candidate derivations は execution trace に残るが、
knowledge state は first accepted step を保持する。

## 50.3 Pattern language

Structured pattern variables and shared bindings exist。

Fully general recursive unification language ではない。

Phase 15 reverse difference bridge は nested recursive unification を追加せず
`match_guard` で current difference structure を検証する。

## 50.4 Search complexity

Exhaustive premise assignment can grow combinatorially。

Indexing / pruning / semi-naive evaluation は未実装。

## 50.5 Termination

`max_rounds` は generic safety bound。

Semantic cycle detection ではない。

Some structural theorem families can grow without bound。

Phase 14 relation closure と current Phase 15 modulo/coset bridge family は
finite active term set 上で `FIXED_POINT`。

## 50.6 Map typing

Proof-level `MapSymbol` has no complete source / target / ambient homotopy-group
typing。

## 50.7 Additive normalization

No canonical commutative / associative / scalar normal form。

## 50.8 Modulo normalization

No canonical representative selection。

No quotient arithmetic normalization。

## 50.9 Symbolic scalars

Integer coefficient variables / parity / divisibility constraints are not yet
first-class。

---

# 51. Phase 16 boundary

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

Phase 15 で Coset / modulo の最小基盤が完成したため、次の自然な Phase は:

```text
Phase 16: Symbolic scalar constraints
```

Initial actual needs:

```text
α = kβ + γ
k odd
```

```text
k ∈ Z
k ≡ 1 mod 2
```

Potential needs:

- symbolic integer variable
- parity constraint
- divisibility / nondivisibility constraint
- scalar occurrence inside `Multiple`
- theorem statement connecting a scalar constraint to an additive relation
- finite / terminating constraint propagation

Phase 16 でも actual mathematical need を先に固定し、general indeterminacy /
Toda bracket を先取りしない。

Generic engine の変更は actual scalar theorem が current rule language で
表現できないと実証された場合のみ。

---

# 52. Testing principle

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

# 53. Documentation policy

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
