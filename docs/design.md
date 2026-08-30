# ehp_proof 設計メモ

この文書は Phase 17 完了時点の current architecture / semantics /
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
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy statements
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

Modulo / scalar constraint / indeterminacy / Toda semantics も algebra layer
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

`ScalarSymbol` は `Multiple.coefficient` に利用できる。

Expression layer は数学的 syntax / structure を lossless に保持する。

Expression layer は以下を担当しない:

- theorem applicability
- scalar constraint solving
- candidate enumeration
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
- indeterminacy collapse
- Toda-bracket value selection

---

# 5. Sum semantics

`Sum` は binary tree を保持する。

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

Current additive inverse:

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

`ScalarSymbol("k")` は concrete integer を選択しない。

---

# 7. Relation / Proof layer

Current `RelationType`:

```text
EQUALITY
ZERO
ORDER
```

Additive / composition / symbolic multiple equality は generic
`RelationType.EQUALITY` を使う。

以下は必要に応じて専用 statement class を使う:

- set / subgroup
- modulo / coset
- scalar constraints
- indeterminacy

これらを ordinary equality に無理に押し込まない。

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

# 8. Generic inference engine

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

# 9. Matching semantics

- exhaustive deterministic premise assignment
- `PatternVariable`
- `VariableBinding`
- shared-binding consistency
- same available-step index を one assignment 内で再利用しない
- conclusion duplicate identity は ordinary Python equality

Pattern language は structured matching を提供するが、arbitrary nested
dataclass に対する fully recursive unification system ではない。

Nested structure の domain-specific inspection が必要な場合は:

```text
statement_type
+
match_guard
+
conclusion_builder
```

を使う。

Phase 17 の reverse coset bridge と symbolic coefficient bridge はこの
boundary を利用する。

---

# 10. Fixed-point semantics

Derived conclusions は next round の premises になる。

Termination:

```text
FIXED_POINT
MAX_ROUNDS
```

`round_count` は productive round 数。

`max_rounds` は safety bound であり semantic cycle detector ではない。

One round 内で生成された conclusion は same round 内で fresh premise として
逐次再利用しない。

同一 conclusion の first accepted `ProofStep` を knowledge state に保持する。
Alternative derivation は duplicate-rejected trace に残り得る。

---

# 11. Generic relation rules

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

Domain-specific statements は explicit bridge がある場合だけ generic
relation layer と接続する。

---

# 12. Phase 6–13 summary

## Phase 6: EHP

```text
Image + Kernel → Exactness
Exactness → EHP zero composition
EHP zero composition → generic ZERO
```

## Phase 7: ORDER

```text
ord(α)=n
↓
nα=0
```

## Phase 8: Suspension

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension は unbounded structural growth を起こし得る。

## Phase 9: Freudenthal

```text
stable range
→ isomorphism
→ injectivity
→ equality / ZERO reflection
```

boundary は epimorphism only。

## Phase 10: Composition

```text
α∘β=γ
```

を structured equality として保持し、
Suspension-composition functoriality と generic equality へ接続。

## Phase 11: generalized Hopf

```text
H(α)=β
```

の value は general `Expression`。

Critical boundary:

```text
H(x)=0
↛
x=0
```

## Phase 12: additive

```text
Sum
Multiple(-1,α)
```

を導入。

Additive law は explicit theorem relation。

## Phase 13: homomorphism

```text
HomomorphismStatement(f)
```

のもとで:

```text
f(α+β)=f(α)+f(β)
f(0)=0
f(-α)=-f(α)
f(nα)=n f(α)
```

---

# 13. Phase 14 set / subgroup design

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

Role-aware subgroup references:

```text
ImageSubgroupReference
KernelSubgroupReference
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

role-aware theorem equality を通して membership を transport する。

---

# 14. Phase 15 coset / modulo design

First-class:

```text
Coset
ModuloStatement
CosetEqualityStatement
```

Semantics:

```text
α+A
α≡β mod A
α+A=β+A
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

Explicit scope:

```text
α=β
→
α≡β mod A
```

arbitrary modulus enumeration は行わない。

Important:

```text
mathematical congruence
≠
ordinary equality
```

---

# 15. Phase 16 symbolic scalar design

First-class:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

Representative rules:

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

```text
ord(β)=2
+
k≡1 mod 2
→
kβ=β
```

Phase 16 does not implement:

```text
general symbolic arithmetic solver
general congruence closure
automatic coefficient enumeration
```

The symbolic-scalar layer only crosses into modulo reasoning through explicit
bridges.

---

# 16. Phase 17 indeterminacy design

Phase 17 introduces first-class proof statements for concrete forms of
non-unique mathematical information.

Core principle:

```text
uncertainty
≠
candidate enumeration
```

and:

```text
indeterminate information
must not be silently strengthened
to exact information
```

No universal `Indeterminacy` superclass is introduced.

No general `CandidateFamily` is introduced.

Generalization is deferred until actual examples demonstrate a shared structure.

---

# 17. CosetMembershipStatement semantics

```python
CosetMembershipStatement(
  element=x,
  coset=Coset(
    representative=beta,
    subgroup=A,
  ),
)
```

means:

```text
x ∈ β+A
```

This is distinct from Phase 14:

```text
MembershipStatement(
  element=x,
  subgroup=A,
)
```

which means:

```text
x ∈ A
```

The field distinction is intentional.

`MembershipStatement` is not widened to accept arbitrary set-like objects.

---

# 18. SignIndeterminacyStatement semantics

```python
SignIndeterminacyStatement(
  value=x,
  representative=alpha,
)
```

means:

```text
x = ±α
```

It is not a `RelationType.EQUALITY`.

The statement does not generate:

```text
x=α
```

or:

```text
x=-α
```

because the sign has not been selected.

The representation does not store a Python list:

```text
[α,-α]
```

The mathematical structure of sign ambiguity is kept explicit.

---

# 19. CoefficientIndeterminacyStatement semantics

```python
CoefficientIndeterminacyStatement(
  value=x,
  expression=expression,
  constraint=OddScalarStatement(k),
)
```

with:

```text
expression = kβ+γ
```

means:

```text
x ∈ {kβ+γ | k odd}
```

The representation reuses:

```text
ScalarSymbol
Multiple
Sum
OddScalarStatement
```

It does not add:

```text
odd=True
```

or a second scalar-constraint hierarchy.

Current Phase 17 constraint field is intentionally narrow:

```text
OddScalarStatement
```

rather than a speculative universal constraint protocol.

---

# 20. Modulo → coset membership bridge

Implemented:

```text
x≡β mod A
↓
x∈β+A
```

The conclusion reuses the existing Phase 15 `Coset`.

This bridge does not derive:

```text
x=β
```

No coset elements are enumerated.

---

# 21. Coset membership → modulo bridge

Implemented:

```text
x∈β+A
↓
x≡β mod A
```

Because nested dataclass pattern matching is not fully recursive, this rule uses:

```text
PremisePattern(statement_type=CosetMembershipStatement)
+
match_guard
+
conclusion_builder
```

The generic matcher is not extended.

This is consistent with the existing Phase 15 reverse-bridge design.

---

# 22. Equality → sign indeterminacy bridge

Implemented:

```text
x=α
↓
x=±α
```

This is information weakening:

```text
exact value
↓
sign-indeterminate value
```

The reverse direction is not implemented:

```text
x=±α
↛
x=α
```

Existing equality symmetry may derive a symmetrically oriented exact equality,
after which the explicit weakening rule may apply.

The sign rule itself does not duplicate equality symmetry.

---

# 23. Symbolic scalar → coefficient indeterminacy bridge

Implemented premise pair:

```text
x=kβ+γ
k odd
```

Conclusion:

```text
CoefficientIndeterminacyStatement(
  value=x,
  expression=kβ+γ,
  constraint=k odd,
)
```

The current accepted expression shape is intentionally:

```text
Sum(
  left=Multiple(
    coefficient=k,
    expression=β,
  ),
  right=γ,
)
```

The rule checks:

```text
equality coefficient
==
OddScalarStatement.scalar
```

A mismatched fact:

```text
x=kβ+γ
l odd
```

is rejected.

Current Phase 17 does not normalize:

```text
γ+kβ
```

into:

```text
kβ+γ
```

and does not recursively search arbitrary expression trees for symbolic
coefficients.

---

# 24. Phase 17 representative scenario

Representative initial knowledge:

```text
x=kβ+γ
k odd
x≡δ mod A
```

Active rule families:

```text
odd → mod-two congruence
symbolic odd equality → coefficient indeterminacy
equality → sign indeterminacy
modulo → coset membership
coset membership → modulo
```

Representative derived knowledge:

```text
k≡1 mod 2
x∈{kβ+γ | k odd}
x=±(kβ+γ)
x∈δ+A
x≡δ mod A
```

Not derived:

```text
x=δ
```

No concrete odd scalar candidate is generated.

The scenario reaches:

```text
FIXED_POINT
```

---

# 25. Phase 17 provenance semantics

Each derived indeterminacy `ProofStep` stores direct provenance.

Coefficient indeterminacy:

```text
premises:
  x=kβ+γ
  k odd
inference_rule:
  symbolic odd equality → coefficient indeterminacy
```

Sign indeterminacy:

```text
premise:
  x=kβ+γ
inference_rule:
  equality → sign indeterminacy
```

Coset membership:

```text
premise:
  x≡δ mod A
inference_rule:
  modulo → coset membership
```

Unrelated branches are not added to direct premises.

---

# 26. Phase 17 termination semantics

The bidirectional bridge:

```text
Modulo
↔
CosetMembership
```

is a theorem cycle.

For a fixed finite known term set, it does not increase structural depth.

Example:

```text
given Modulo
↓
new CosetMembership
↓
candidate Modulo
↓
duplicate rejected
```

The terminal round has:

```text
new_steps == ()
```

and duplicate candidates appear in:

```text
duplicate_rejected_steps
```

The engine therefore reaches genuine:

```text
FIXED_POINT
```

for the current Phase 17 cycle.

This does not prove arbitrary future indeterminacy / Toda rule families terminate.

---

# 27. Phase 17 non-collapse boundary

Critical regression specifications:

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

```text
CoefficientIndeterminacyStatement
≠
RelationType.EQUALITY
```

The proof system must not strengthen incomplete information without an explicit
mathematical theorem that justifies the strengthening.

---

# 28. Candidate enumeration boundary

Current system does not convert:

```text
k odd
```

into:

```text
k=1
k=3
k=5
...
```

and does not convert coefficient indeterminacy into:

```text
x=β+γ
x=3β+γ
x=5β+γ
...
```

Similarly:

```text
x∈β+A
```

does not enumerate coset elements.

This is both a mathematical semantics decision and a termination boundary.

---

# 29. Generalization boundary

Phase 17 intentionally does not introduce:

```text
Indeterminacy
CandidateFamily
FiniteCandidateSet
GeneralSetExpression
ConstraintProtocol
```

as universal abstractions.

Current concrete mathematical structures remain separate:

```text
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

Common abstraction should be introduced only after actual Toda / theorem
examples demonstrate the necessary common semantics.

---

# 30. Current limitations

## 30.1 Conclusion identity

ordinary Python equality。

No theorem-aware canonical equivalence.

## 30.2 Alternative proofs

same conclusion の multiple candidate derivations may remain in execution trace,
while knowledge state keeps the first accepted step.

## 30.3 Pattern language

Structured matching exists.

Fully general recursive symbolic unification does not.

## 30.4 Search complexity

Exhaustive premise assignment can grow combinatorially.

No general indexing / semi-naive evaluation / agenda optimization.

## 30.5 Termination

`max_rounds` remains generic safety bound.

Current Phase 17 modulo/coset family is finite for fixed known terms.

Structural families such as repeated Suspension remain potentially unbounded.

## 30.6 Map / homotopy typing

Proof-level expressions do not yet fully carry:

```text
source
target
ambient group
stable / unstable context
```

## 30.7 Scalar reasoning

No general symbolic integer arithmetic solver.

## 30.8 Indeterminacy narrowing

No intersection / narrowing of multiple independent candidate families.

## 30.9 Toda bracket

No first-class Toda bracket expression / statement yet.

---

# 31. Phase 17 completion criteria

1. first-class `CosetMembershipStatement`.
2. first-class `SignIndeterminacyStatement`.
3. first-class `CoefficientIndeterminacyStatement`.
4. reuse of existing `Coset`.
5. reuse of existing symbolic scalar structures.
6. sign uncertainty is not ordinary equality.
7. coefficient uncertainty is not concrete enumeration.
8. modulo → coset membership.
9. coset membership → modulo.
10. equality → sign indeterminacy.
11. sign indeterminacy does not imply equality.
12. symbolic odd equality → coefficient indeterminacy.
13. scalar identity must match.
14. unsupported expression order is not normalized automatically.
15. nested reverse bridge uses guard / builder, not engine changes.
16. representative scenario combines symbolic scalar and modulo branches.
17. representative scenario reaches `FIXED_POINT`.
18. coefficient provenance is traceable.
19. sign provenance is traceable.
20. coset provenance is traceable.
21. modulo/coset cycle terminates through duplicate rejection.
22. terminal round has no new steps.
23. sign is not selected automatically.
24. coset representative is not selected automatically.
25. coefficient candidates are not enumerated.
26. indeterminacy statements do not leak into equality-rule scope.
27. no general `CandidateFamily`.
28. no general `Indeterminacy` superclass.
29. generic engine unchanged.
30. full regression PASS.

Verified:

```text
tests/test_indeterminacy_rules.py
36 passed
```

```text
full suite
1024 passed in 66.01s
```

---

# 32. Phase 17 non-goals

Phase 17 では実装しない:

- general set-valued expression hierarchy
- arbitrary finite candidate-set algebra
- arbitrary coefficient-constraint families
- automatic indeterminacy intersection / narrowing
- automatic collapse from order facts
- automatic selection of sign
- automatic selection of coset representative
- candidate enumeration
- theorem quantifier language
- existential witness generation
- typed source / target validation
- stable homotopy group model
- structured generator overhaul
- iterated symbolic suspension `E^t`
- Toda bracket syntax
- Toda bracket defining-condition validation
- Toda bracket value / containment rules
- stable Toda bracket
- higher Toda bracket
- semantic cycle detection
- fully recursive pattern unification

---

# 33. Phase 18 boundary

Next phase:

```text
Phase 18: Toda bracket minimum representation
```

Initial design requirement:

```text
bracket input structure
≠
bracket value
```

A Toda bracket must not be modeled as a function that returns one exact
`Expression`.

Primary actual notation candidates:

```text
{a,b,c}
```

and later / when required:

```text
{a,E^t b,E^t c}_t
```

Stable notation:

```text
<a,b,c>
```

must remain semantically distinguishable from unstable notation.

Phase 18 should first determine the smallest bracket object and membership /
value statement needed by an actual mathematical example.

Potential Phase 17 reuse:

```text
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

Toda-specific abstraction should only be introduced where the bracket itself
requires it.

No full higher-Toda framework should be introduced before a concrete theorem
needs it.

---

# 34. Testing principle

For a new mathematical layer:

1. representation test
2. structural distinction test
3. typing / validity test when the layer requires it
4. single-rule semantic test
5. invalid-premise rejection
6. multi-round integration
7. generic-rule reconnection
8. provenance
9. representative scenario
10. termination / inference-scope boundary
11. full regression

For Toda bracket work, later tests should additionally cover:

```text
defining compositions
zero-composition assumptions
bracket membership
set-valued semantics
indeterminacy preservation
index / suspension-parameter distinction
stable / unstable distinction
```

---

# 35. Documentation policy

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
