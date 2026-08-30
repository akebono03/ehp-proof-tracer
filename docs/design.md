# ehp_proof 設計メモ

この文書は Phase 19 完了時点の current architecture / semantics /
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
indeterminacy / Toda statements
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

Separate set-valued Toda structure:

```text
TodaBracket
```
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
- Toda-bracket definedness proof
- Toda-bracket membership proof

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

## 30.9 Toda bracket theorem bridge

Three-fold Toda bracket representation, definedness, membership, and the first actual membership theorem bridge are implemented.

Still not implemented:

```text
indexed unstable Toda notation
stable Toda brackets
higher Toda brackets
general Toda value-set algebra
```

---


# 31. Phase 18 Toda bracket design

Phase 18 introduces the minimum first-class representation needed for a
three-fold unstable Toda bracket.

Core principle:

```text
bracket input structure
≠
bracket value
```

and:

```text
definedness
≠
membership
≠
exact value
```

No universal set-expression hierarchy is introduced.

---

# 32. TodaBracket semantics

```python
TodaBracket(
  first=a,
  second=b,
  third=c,
)
```

represents:

```text
{a,b,c}
```

The entries are `Expression`.

`TodaBracket` itself is intentionally not an `Expression`.

This prevents the bracket object from being silently treated as one homotopy
element.

The representation is fixed to three entries in Phase 18.

Variable arity is not introduced before an actual higher Toda example requires
it.

Entry order is structural:

```text
TodaBracket(a,b,c)
!=structural
TodaBracket(a,c,b)
```

This means only that constructor equality preserves input order.

It does not assert that both brackets are well-typed or mathematically defined.

---

# 33. TodaBracketMembershipStatement semantics

```python
TodaBracketMembershipStatement(
  element=x,
  bracket=TodaBracket(a,b,c),
)
```

means:

```text
x ∈ {a,b,c}
```

It is a Toda-specific statement.

It is not Phase 14 subgroup membership:

```text
MembershipStatement(x,A)
```

and `MembershipStatement` is not widened.

The entries `a,b,c` are bracket inputs, not candidate bracket values.

No rules derive:

```text
x=a
x=b
x=c
```

from bracket membership.

---

# 34. TodaBracketDefinedStatement semantics

```python
TodaBracketDefinedStatement(
  bracket=TodaBracket(a,b,c),
)
```

means that the current implemented defining conditions for the three-fold
bracket have been established.

Current Phase 18 rule:

```text
ZERO(a∘b)
+
ZERO(b∘c)
↓
{a,b,c} defined
```

The rule checks the shared middle entry structurally:

```text
first_composition.right
==
second_composition.left
```

The current rule does not perform full source / target sphere validation.

That validation remains deferred until typed homotopy elements are required.

---

# 35. Composition / ZERO bridge

Phase 18 reuses the existing Phase 10 bridge:

```text
Composition(a,b)=0
RelationType.EQUALITY
↓
Composition(a,b)=0
RelationType.ZERO
```

and analogously for `b∘c`.

Therefore a known pair:

```text
a∘b=0
b∘c=0
```

can reach:

```text
ZERO(a∘b)
ZERO(b∘c)
↓
TodaBracketDefinedStatement({a,b,c})
```

without modifying the generic inference engine.

---

# 36. Definedness / membership boundary

The following rule is intentionally absent:

```text
{a,b,c} defined
→
x∈{a,b,c}
```

Definedness only says the bracket is available as a mathematical object under
the current implemented conditions.

It does not provide a specific member.

Likewise:

```text
a∘b=0
b∘c=0
↛
x∈{a,b,c}
```

without an additional known bracket fact or theorem.

---

# 37. Phase 17 indeterminacy coexistence

Toda membership can coexist with Phase 17 partial information:

```text
x∈{a,b,c}
x=±α
```

or:

```text
x∈{a,b,c}
x∈β+A
```

The connection is currently shared `Expression` identity only.

No general theorem bridge is introduced:

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

and no reverse bridge is introduced.

In particular:

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

This preserves the Phase 17 non-collapse principle.

---

# 38. Phase 18 provenance semantics

The definedness dependency chain is:

```text
known a∘b=0
↓
generic ZERO(a∘b)

known b∘c=0
↓
generic ZERO(b∘c)

ZERO(a∘b)
+
ZERO(b∘c)
↓
TodaBracketDefinedStatement({a,b,c})
```

The final `ProofStep` stores exactly the two ZERO steps as direct premises.

Each ZERO step stores its corresponding original composition equality as its
direct premise.

The inference rules are preserved at both levels.

Unrelated facts are not inserted into the direct dependency chain.

No new recursive provenance API is added.

---

# 39. Phase 18 representative scenario

Representative initial knowledge:

```text
a∘b=0
b∘c=0
x∈{a,b,c}
x=±α
```

Active rule families:

```text
composition equality → generic ZERO
ZERO + ZERO → Toda bracket definedness
```

Derived:

```text
ZERO(a∘b)
ZERO(b∘c)
{a,b,c} defined
```

Coexisting given partial information:

```text
x∈{a,b,c}
x=±α
```

Not derived:

```text
x=α
```

The run reaches:

```text
FIXED_POINT
```

with two productive rounds.

---

# 40. Phase 18 termination semantics

The current Toda rule family does not increase structural depth recursively.

For finite known terms:

```text
round 1
EQUALITY composition → ZERO

round 2
ZERO + ZERO → definedness

terminal inference check
→ new_steps == ()
```

Thus the representative rule family reaches a genuine fixed point.

This does not establish termination for future indexed / stable / higher Toda
rule families.

---

# 41. Phase 18 inference-scope boundary

Toda-specific statements are not ordinary relations.

```text
TodaBracketDefinedStatement
≠
RelationType.EQUALITY
```

```text
TodaBracketMembershipStatement
≠
RelationType.EQUALITY
```

Generic equality symmetry does not match them.

No exact-value rule is activated by Toda membership alone.

No candidate enumeration is introduced.

No bracket entry is treated as a candidate member.

---

# 42. Phase 18 completion criteria

1. first-class `TodaBracket`.
2. exactly three ordered entries in the current implementation.
3. bracket object is not an `Expression`.
4. structural entry order is preserved.
5. first-class `TodaBracketMembershipStatement`.
6. first-class `TodaBracketDefinedStatement`.
7. subgroup `MembershipStatement` remains unchanged.
8. bracket entries are not candidate values.
9. two generic ZERO composition facts establish bracket definedness.
10. defining compositions must share the middle entry.
11. mismatched middle entry is rejected.
12. one ZERO fact alone is insufficient.
13. existing composition equality → ZERO bridge is reused.
14. definedness does not imply membership.
15. membership does not imply exact equality.
16. bracket membership coexists with sign indeterminacy.
17. bracket membership coexists with coset indeterminacy.
18. no automatic Toda→sign bridge.
19. no automatic Toda→coset bridge.
20. no automatic reverse bridge from Phase 17 indeterminacy.
21. sign is not selected.
22. definedness provenance includes both direct ZERO steps.
23. ZERO provenance includes original composition equalities.
24. unrelated facts do not enter direct provenance.
25. representative scenario reaches `FIXED_POINT`.
26. representative scenario has two productive rounds.
27. explicit terminal check yields `new_steps == ()`.
28. Toda statements remain outside generic equality scope.
29. no general set-valued expression hierarchy.
30. no variable-arity Toda bracket.
31. no indexed unstable Toda notation.
32. no stable Toda bracket.
33. no higher Toda framework.
34. no full source / target typing.
35. generic engine unchanged.
36. full regression PASS.

Verified:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

---

# 43. Phase 18 non-goals

Phase 18 では実装しない:

- bracket-definednessから arbitrary member の生成
- bracket membership から exact value の生成
- Toda bracket containment in a coset
- automatic Toda indeterminacy narrowing
- arbitrary bracket candidate enumeration
- general set-valued expression hierarchy
- general candidate-set algebra
- variable-arity Toda bracket
- indexed unstable notation `{a,E^t b,E^t c}_t`
- symbolic iterated suspension `E^t`
- full source / target typing
- stable homotopy group model
- stable Toda bracket `<a,b,c>`
- higher Toda bracket
- theorem quantifier language
- existential witness generation
- semantic cycle detection
- fully recursive pattern unification

---


# 44. Phase 19 Toda membership theorem bridge design

Phase 19 adds the first actual literature-backed theorem bridge for Toda
membership.

The selected concrete example is represented in the current proof layer as:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

The literature notation includes an index `_1`.

Current Phase 19 representation intentionally projects that fact to the
existing unindexed three-fold `TodaBracket`.

Therefore:

```text
current Phase 19 representation
≠
lossless indexed Toda notation
```

The index is deferred to Phase 20.

---

# 45. Actual ε₃ representation

The bracket is represented structurally as:

```python
TodaBracket(
  first=η₃,
  second=Suspension(ν′),
  third=ν₇,
)
```

`Eν′` is not stored as one generator name.

The actual membership conclusion is:

```python
TodaBracketMembershipStatement(
  element=ε₃,
  bracket=...,
)
```

The bracket remains set-valued structure and is not converted to an
`Expression`.

---

# 46. Toda membership provenance fields

`TodaBracketMembershipStatement` supports:

```text
element
bracket
source
note
```

`source` follows the existing literature-provenance style:

```text
LiteratureReference | str | None
```

A known membership fact may be converted to a `ProofRule.GIVEN` step through:

```text
toda_bracket_membership_proof_step()
```

The source fields belong to the statement so the accepted conclusion retains
literature metadata.

---

# 47. TodaBracketMembershipTheoremStatement semantics

Phase 19 adds:

```text
TodaBracketMembershipTheoremStatement
```

with:

```text
element
bracket
source
note
```

It means:

```text
this concrete literature-backed theorem
can conclude that element belongs to bracket
when the matching bracket is established as defined
```

It is intentionally a narrow actual-theorem representation.

It is not a universal theorem object.

It does not contain:

```text
quantified variables
typed binders
general assumptions list
general conclusion AST
theorem registry identity
```

Those remain deferred until an actual later theorem requires them.

Critical distinction:

```text
TodaBracketMembershipTheoremStatement
≠
TodaBracketMembershipStatement
```

The theorem statement is applicability knowledge, not the membership
conclusion itself.

---

# 48. Toda theorem fact as GIVEN

A concrete theorem fact is introduced by:

```text
toda_bracket_membership_theorem_proof_step()
```

The resulting step has:

```text
rule = ProofRule.GIVEN
premises = ()
```

Literature provenance is stored in the theorem statement.

No inference occurs merely by storing the theorem fact.

---

# 49. Toda membership theorem bridge

Implemented rule:

```text
toda_bracket_membership_from_theorem_inference_rule()
```

Premises:

```text
TodaBracketMembershipTheoremStatement(
  element=x,
  bracket=B,
)
+
TodaBracketDefinedStatement(
  bracket=B,
)
```

Conclusion:

```text
TodaBracketMembershipStatement(
  element=x,
  bracket=B,
  source=theorem.source,
  note=theorem.note,
)
```

The theorem bracket and defined bracket must be structurally equal.

A mismatched bracket is rejected.

Critical boundaries:

```text
theorem fact alone
↛
membership
```

```text
definedness alone
↛
membership
```

```text
matching theorem fact
+
definedness
→
membership
```

---

# 50. Phase 19 actual multi-round chain

Initial facts:

```text
η₃∘Eν′ = 0
Eν′∘ν₇ = 0
Toda membership theorem fact for ε₃
```

Active rules:

```text
composition equality → ZERO
ZERO + ZERO → Toda bracket definedness
Toda theorem fact + definedness → Toda membership
```

Productive rounds:

```text
round 1
ZERO(η₃∘Eν′)
ZERO(Eν′∘ν₇)

round 2
{η₃,Eν′,ν₇} defined

round 3
ε₃ ∈ {η₃,Eν′,ν₇}
```

The generic engine is unchanged.

---

# 51. Phase 17 indeterminacy coexistence

The theorem-derived membership can coexist with:

```text
ε₃ = ±α
```

and:

```text
ε₃ ∈ β+A
```

These are additional pieces of partial information.

They are not direct premises of the Toda theorem bridge.

No new rules are introduced:

```text
Toda membership
→ sign indeterminacy
```

```text
Toda membership
→ coset indeterminacy
```

and no exact-value collapse is permitted:

```text
ε₃∈TodaBracket(...)
+
ε₃=±α
↛
ε₃=α
```

```text
ε₃∈TodaBracket(...)
+
ε₃=±α
↛
ε₃=-α
```

```text
ε₃∈TodaBracket(...)
+
ε₃∈β+A
↛
ε₃=β
```

No candidate intersection or narrowing system is introduced.

---

# 52. Phase 19 provenance semantics

The final membership step has direct premises:

```text
theorem step
definedness step
```

The full dependency tree is:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
│
├─ Toda membership theorem fact
│
└─ {η₃,Eν′,ν₇} defined
   │
   ├─ ZERO(η₃∘Eν′)
   │  └─ η₃∘Eν′ = 0
   │
   └─ ZERO(Eν′∘ν₇)
      └─ Eν′∘ν₇ = 0
```

Each intermediate step retains its own `inference_rule`.

Unrelated facts and coexisting sign / coset facts do not enter the direct
membership dependency branch.

No new recursive provenance model is introduced.

---

# 53. Phase 19 representative scenario

Representative initial knowledge:

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

The membership direct provenance remains theorem + definedness only.

---

# 54. Phase 19 termination semantics

The current Phase 19 rule family does not recursively increase structural
depth.

For the representative fixed finite knowledge state:

```text
round 1
composition equality → ZERO

round 2
ZERO + ZERO → definedness

round 3
theorem + definedness → membership

terminal check
→ new_steps == ()
```

Therefore:

```text
round_count == 3
termination_reason == FIXED_POINT
```

This is a claim about the current active Phase 19 family only.

It does not establish termination for future indexed, stable, or higher Toda
families.

---

# 55. Phase 19 inference-scope boundary

All Toda-specific theorem / definedness / membership statements remain outside
generic equality scope:

```text
TodaBracketMembershipTheoremStatement
≠
RelationType.EQUALITY
```

```text
TodaBracketDefinedStatement
≠
RelationType.EQUALITY
```

```text
TodaBracketMembershipStatement
≠
RelationType.EQUALITY
```

No generic equality symmetry or transitivity rule treats these statements as
ordinary equality relations.

Critical Phase 19 non-generation boundaries:

```text
definedness
↛
membership
```

```text
theorem fact
↛
membership
```

```text
membership
↛
exact value
```

```text
membership
↛
sign / coset indeterminacy
```

---

# 56. Phase 19 completion criteria

1. actual ε₃ Toda fact selected.
2. current representation uses an unindexed three-fold projection.
3. `Eν′` is structural `Suspension(ν′)`.
4. membership preserves literature `source` / `note`.
5. known membership can be stored as a GIVEN proof step.
6. first-class narrow Toda membership theorem statement.
7. theorem fact can be stored as a GIVEN proof step.
8. theorem statement is distinct from membership.
9. matching theorem + definedness derives membership.
10. mismatched bracket is rejected.
11. theorem alone does not derive membership.
12. definedness alone does not derive membership.
13. actual defining composition equalities connect through ZERO.
14. actual chain derives definedness.
15. actual chain derives ε₃ membership.
16. representative derivation uses three productive rounds.
17. theorem-derived membership coexists with sign indeterminacy.
18. theorem-derived membership coexists with coset indeterminacy.
19. sign is not selected.
20. coset representative is not selected.
21. membership does not create sign indeterminacy.
22. membership does not create coset indeterminacy.
23. full provenance reaches theorem fact and both defining compositions.
24. unrelated facts are excluded from direct provenance.
25. representative scenario reaches `FIXED_POINT`.
26. explicit terminal round yields `new_steps == ()`.
27. Toda theorem statement is outside generic equality scope.
28. no general theorem hierarchy.
29. no indexed unstable notation.
30. literature `_1` remains intentionally unrepresented.
31. no typed source / target validation.
32. no stable Toda bracket.
33. no higher Toda bracket.
34. generic inference engine unchanged.
35. full regression passes.

Verified:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

```text
full suite
1064 passed in 61.64s
```

---

# 57. Phase 20 boundary

Next candidate Phase:

```text
Phase 20: indexed unstable Toda notation
```

Target notation:

```text
{a,E^t b,E^t c}_t
```

Phase 20 must preserve the bracket index explicitly rather than treating it as
display-only decoration.

The current ε₃ example gives an immediate actual need for this extension
because the source notation uses:

```text
{η₃,Eν′,ν₇}_1
```

while Phase 19 stores only:

```text
{η₃,Eν′,ν₇}
```

The representation must not silently claim those are losslessly identical.

Stable notation:

```text
<a,b,c>
```

remains a separate future context.

# 58. Testing principle

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

# 59. Documentation policy

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
