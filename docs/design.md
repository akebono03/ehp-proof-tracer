# ehp_proof 設計メモ

この文書は Phase 11 完了時点の current architecture / semantics /
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
├── Composition
└── Suspension
```

`Composition(left, right)` は composition structure。

`Suspension(expression)` は expression structure のみ。

Expression layer は theorem applicability、stable range、dimension
validation、zero / equality proof、normalization を担当しない。

---

# 5. Relation / Proof layer

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

`ProofStep` fields:

```text
conclusion
premises
rule
note
inference_rule
```

provenance は `premises` と `inference_rule` に保持する。

Derived conclusion に source を機械的に複製することは provenance の
必須条件ではない。

---

# 6. Generic inference engine

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

# 7. Matching semantics

- exhaustive deterministic premise assignment
- `PatternVariable`
- `VariableBinding`
- shared-binding consistency
- same available-step index を one assignment 内で再利用しない

同一 conclusion は ordinary Python equality で duplicate reject。

---

# 8. Fixed-point semantics

Derived conclusions は次 round の premises になる。

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

# 9. Generic relation rules

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

EHP / ORDER / Suspension / Freudenthal / Toda / Hopf が同じ generic
relation layer を共有する。

---

# 10. Phase 6 EHP rule family

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
```

Generic engine に EHP-specific branch は追加しない。

---

# 11. Phase 7 ORDER rule family

```text
ord(α)=n
↓
nα=0
```

Conclusion は generic ZERO relation。

---

# 12. Phase 8 Suspension rule family

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension は distinct nested expressions を無限に生成し得る。

```text
x=0
→ E(x)=0
→ E²(x)=0
→ ...
```

したがって必要に応じて staged / bounded execution を使う。

原則:

```text
mathematical applicability
≠
execution scope
```

---

# 13. Phase 9 Freudenthal design

Expression-level:

```text
Suspension(expression)
```

と theorem-level:

```text
SuspensionMapStatement(
  sphere_dimension,
  stem,
)
```

を分離する。

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

Different suspension maps must not cross-match.

---

# 14. Phase 10 composition representation

Known composition relation:

```text
α∘β = γ
```

は `Composition` を含む ordinary generic equality として保持する。

Toda 専用 statement class は作らない。

Known zero composition:

```text
α∘β=0
```

は generic ZERO へ bridge できる。

---

# 15. Suspension-composition functoriality

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

Applicability は premise lhs が `Composition` の場合に限定する。

Generic Suspension preservation:

```text
α∘β=γ
↓
E(α∘β)=Eγ
```

との間を generic symmetry / transitivity で接続し:

```text
Eα∘Eβ=Eγ
```

を得る。

---

# 16. Phase 10 termination boundary

With:

```text
functoriality
+
symmetry
```

structural depth が増え得る:

```text
E(α∘β)=Eα∘Eβ
↓
Eα∘Eβ=E(α∘β)
↓
E(Eα∘Eβ)=E²α∘E²β
↓
...
```

したがって unrestricted fixed-point termination は仮定しない。

Finite representative task は staged execution を使う。

---

# 17. Phase 11 generalized Hopf-invariant representation

Generalized Hopf fact:

```text
H(α)=β
```

は:

```text
HopfInvariantStatement(
  expression=α,
  value=β,
)
```

で表す。

Fields:

```text
expression
value
source
note
```

`value` は `Expression`。

したがって generalized Hopf invariant value を integer に限定しない。

Representable examples:

```text
H(α)=0
H(α)=β
H(α)=nβ
H(α)=β∘Eγ
```

---

# 18. Known Hopf fact / provenance

Known fact は `LiteratureReference` を保持できる。

Known fact は `ProofRule.GIVEN` の `ProofStep` として knowledge state に
入る。

Provenance:

```text
derived step
↓
premises
↓
known Hopf fact
↓
LiteratureReference
```

を採用する。

---

# 19. Hopf composition-law applicability

```text
H(α)=β
↓
HopfCompositionLawStatement(α,β)
```

`HopfCompositionLawStatement` は actual formula ではなく theorem-ready
intermediate statement。

Fields:

```text
alpha
beta
```

---

# 20. Generalized Hopf composition formula

Given:

```text
HopfCompositionLawStatement(α,β)
+
γ
```

derive:

```text
H(α∘Eγ)=β∘Eγ
```

既存 `Composition` / `Suspension` を再利用する。

---

# 21. Hopf value ZERO bridge

Given:

```text
H(x)=y
+
Relation(y,0,ZERO)
```

derive:

```text
H(x)=0
```

Guard は ZERO relation の lhs が exactly `hopf_statement.value` であることを
要求する。

Unrelated ZERO は reject。

---

# 22. Hopf-zero theorem boundary

重要:

```text
H(x)=0
↛
x=0
```

Phase 11 は Hopf invariant vanishing と element vanishing を区別する。

また:

```text
H(x)=0
→ x ∈ Ker(H)=Im(E)
```

の element-level membership reasoning もまだ実装しない。

この逆方向には membership / image / kernel membership / witness
representation が必要。

---

# 23. Suspension / composition reconnection

Take:

```text
β=Eδ
```

Then:

```text
H(α∘Eγ)=Eδ∘Eγ
```

If:

```text
δ∘γ=0
```

existing rules derive:

```text
E(δ∘γ)=0
```

and:

```text
E(δ∘γ)=Eδ∘Eγ
```

symmetry + generic ZERO propagation gives:

```text
Eδ∘Eγ=0
```

then:

```text
H(α∘Eγ)=0
```

Hopf-specific equality / ZERO engine は作らない。

---

# 24. Phase 11 EHP bridge

Map-level:

```text
H∘E=0
```

と element-level:

```text
H(Eα)=0
```

を区別する。

Bridge premise は:

```text
EHPZeroCompositionStatement(E,H)
```

Rule semantics:

```text
EHPZeroCompositionStatement(E,H)
+
α
↓
H(Eα)=0
```

Applicability guard:

```text
first_map.name == "E"
second_map.name == "H"
```

`H→P` pair は reject。

---

# 25. Phase 11 representative scenario

Same knowledge state に:

```text
Hopf branch
+
EHP branch
```

を置く。

Hopf branch:

```text
H(α)=Eδ
↓
HopfCompositionLawStatement
↓
H(α∘Eγ)=Eδ∘Eγ
↓
generic structural / ZERO reasoning
↓
H(α∘Eγ)=0
```

EHP branch:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eγ)=0
```

Final finite stage は genuine `FIXED_POINT`。

---

# 26. Phase 11 provenance requirements

Hopf final zero:

```text
H(α∘Eγ)=0
```

must trace through:

```text
H(α∘Eγ)=Eδ∘Eγ
↓
HopfCompositionLawStatement(α,Eδ)
↓
H(α)=Eδ
↓
LiteratureReference
```

EHP branch:

```text
H(Eγ)=0
↓
EHPZeroCompositionStatement(E,H)
↓
Exactness(E,H)
```

Each derived step preserves:

```text
ProofRule.INFERENCE
premises
inference_rule
```

Unrelated branch premises must not contaminate direct premises.

---

# 27. Phase 11 theorem scope

Allowed:

```text
H(α)=β
→ HopfCompositionLawStatement(α,β)
```

```text
HopfCompositionLawStatement(α,β)
+
γ
→ H(α∘Eγ)=β∘Eγ
```

```text
H(x)=y
+
y=0
→ H(x)=0
```

```text
EHPZeroCompositionStatement(E,H)
+
α
→ H(Eα)=0
```

Not allowed:

```text
H(x)=0 → x=0
```

```text
H(x)=y
+
z=0
where y != z
→ H(x)=0
```

```text
EHPZeroCompositionStatement(H,P)
+
α
→ H(Eα)=0
```

Not implemented:

```text
H(x)=0 → x ∈ Im(E)
H(x)=0 → exists y, x=E(y)
Hopf additivity
general Hopf algebra identities
```

---

# 28. Phase 11 inference-scope / termination boundary

Phase 11 introduces recursive structural growth:

```text
H(α)=β
↓
Law(α,β)
↓
H(α∘Eγ)=β∘Eγ
↓
Law(α∘Eγ,β∘Eγ)
↓
H((α∘Eγ)∘Eγ)
=
(β∘Eγ)∘Eγ
↓
...
```

Therefore:

```text
hopf_composition_law_inference_rule
+
hopf_composition_formula_inference_rule
```

is not unrestricted fixed-point-safe.

Bounded regression requires:

```text
InferenceTerminationReason.MAX_ROUNDS
```

while confirming actual increasing composition depth.

Finite tasks use:

```text
explicit law stage
↓
explicit formula stage
↓
finite ZERO / generic stage
↓
FIXED_POINT
```

---

# 29. General execution policy after Phase 11

Potentially finite closure families and potentially unbounded structural
familiesを区別する。

Potentially unbounded examples:

```text
repeated Suspension
functoriality + symmetry
Hopf law + Hopf formula
```

Caller / representative scenario が intended theorem depth を明示する。

Automatic rule scheduling はまだ導入しない。

---

# 30. Current limitations

## 30.1 Conclusion equality

ordinary Python equality。theorem-aware normalization は未導入。

## 30.2 Alternative proofs

equal conclusion の knowledge state は first accepted step を保持。

## 30.3 Pattern depth

structured matching はあるが fully general recursive unification ではない。

## 30.4 Search performance

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 30.5 General termination

`max_rounds` は safety bound。semantic cycle detector ではない。

## 30.6 Structural expression growth

Potentially unbounded:

- repeated Suspension
- functoriality / symmetry
- recursive Hopf composition-law application

## 30.7 Expression normalization

未導入:

- canonical `E^n`
- canonical composition normalization
- theorem-aware equality
- associativity normalization

## 30.8 Composition algebra

未導入:

- associativity
- identity
- bilinearity
- general composition simplification

## 30.9 NONZERO

first-class `NONZERO` relation は未導入。

## 30.10 Membership

未導入:

```text
element ∈ subset
element ∈ subgroup
element ∈ image
element ∈ kernel
subset inclusion
```

## 30.11 Indeterminacy / conditional coefficients

未導入:

```text
mod A
α ∈ A
A ⊆ B
α=kβ+γ with k odd
±α
```

## 30.12 Hopf algebra

未導入:

- additivity
- scalar compatibility theorem family
- kernel membership reasoning
- image witness generation
- arbitrary generalized Hopf identities

---

# 31. Phase 11 completion criteria

Phase 11 は次を満たしたため完了とする。

1. generalized Hopf invariant `H(α)=β` を structured statement として表現。
2. value を integer に限定せず `Expression` として保持。
3. source / note provenance を保持。
4. known fact を `ProofStep` 化。
5. Hopf composition-law applicability statement を導出。
6. generalized Hopf composition formula を導出。
7. value ZERO から `H(x)=0` を導出。
8. unrelated ZERO を reject。
9. `H(x)=0 → x=0` を導出しない。
10. Suspension / composition functoriality と接続。
11. generic ZERO propagation と接続。
12. EHP `E→H` zero-composition と `H(Eα)=0` を bridge。
13. `H→P` pair を reject。
14. EHP exactness から Hopf zero へ multi-round 接続。
15. Hopf / EHP representative branches を統合。
16. representative finite stage が `FIXED_POINT`。
17. literature provenance を final conclusion から追跡可能。
18. EHP exactness provenance を final conclusion から追跡可能。
19. theorem scope boundary を regression 固定。
20. recursive Hopf structural growth を regression 固定。
21. bounded unrestricted run が `MAX_ROUNDS`。
22. staged run が `FIXED_POINT`。
23. generic engine に Hopf-specific branch を追加しない。
24. full regression PASS。

---

# 32. Phase 11 completion tests

Phase 11 suite:

```powershell
python -m pytest tests/test_hopf_rules.py -v
```

Result:

```text
28 passed
```

Focused Phase 11-10:

```powershell
python -m pytest tests/test_hopf_rules.py::test_phase11_theorem_scope_boundary tests/test_hopf_rules.py::test_phase11_inference_scope_and_termination_boundary -v
```

Result:

```text
2 passed
```

Full suite:

```powershell
python -m pytest -v
```

Result:

```text
791 passed in 23.41s
```

---

# 33. Phase 12 boundary

Phase 12 も speculative generic-engine refactoring から開始しない。

Natural representation candidates:

```text
α+β
-α
±α
```

```text
α ∈ A
A ⊆ B
α ∈ Ker(H)
α ∈ Im(E)
```

```text
mod A
Toda-bracket indeterminacy
```

```text
α=kβ+γ
k odd
```

Other theorem-family candidates:

- further Toda relations
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- epimorphism / preimage reasoning

基本原則:

```text
actual mathematical need
↓
minimal representation
↓
domain rule
↓
existing generic engine
```

---

# 34. Documentation policy

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
```

Historical limitation は historical statement として保持する。

Current specification は latest README / design を優先する。
