# ehp_proof 設計メモ

この文書は Phase 12 完了時点の current architecture / semantics /
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
└── Suspension
```

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

`Composition(left, right)` は composition structure。

`Suspension(expression)` は Suspension structure。

`Sum(left, right)` は binary additive structure。

`Multiple(coefficient, expression)` は scalar-multiple syntax。

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

専用 `Inverse` node は Phase 12 では導入しない。

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

Phase 12 では constructor normalization:

```text
α+0 → α
0+α → α
```

を行わない。

zero identity theorem も Phase 12 scope には含めない。

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

EHP / ORDER / Suspension / Freudenthal / composition / Hopf / additive
reasoning が同じ generic relation layer を共有する。

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

ORDER semantics は Phase 12 でも変更しない。

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

したがって integer-only に限定しない。

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
H(x)=0 → x ∈ Im(E)
```

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

Conclusion:

```python
Relation(
  lhs=Sum(
    left=alpha,
    right=Multiple(
      coefficient=-1,
      expression=alpha,
    ),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
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

Phase 12 は一般の:

```text
nα ↔ α+...+α
```

を実装しない。

最小 bridge のみ:

```text
α+α = 2α
```

を explicit equality として導入する。

理由:

- `n=2` は association ambiguity がない。
- Phase 7 ORDER semantics を変更しない。
- general repeated-Sum normalization を先取りしない。

Representative connection:

```text
ord(α)=2
↓
2α=0

α+α=2α
↓
generic ZERO propagation
↓
α+α=0
```

---

# 27. Phase 12 representative scenario

Same inference environment に:

```text
additive inverse
commutativity
associativity
ORDER
double / repeated-Sum bridge
generic equality symmetry
generic equality transitivity
generic ZERO propagation
```

を配置する。

Representative branches:

```text
ord(α)=2
→ 2α=0
→ α+α=0
```

```text
α+(-α)=0
α+(-α)=(-α)+α
→ (-α)+α=0
```

```text
(α+β)+γ = α+(β+γ)
(α+β)+γ = γ+(α+β)
→ generic equality closure
```

有限 concrete scenario は genuine `FIXED_POINT` に到達する。

---

# 28. Phase 12 provenance requirements

Representative derived steps は:

```text
ProofRule.INFERENCE
premises
inference_rule
```

を保持する。

ORDER-derived fact:

```text
ord(α)=2
↓
2α=0
```

は `order_implies_zero_multiple_inference_rule` に trace。

Repeated-Sum ZERO:

```text
α+α=0
```

は:

```text
2α=0
+
α+α=2α
↓
generic ZERO propagation
```

に trace。

Inverse reverse ZERO:

```text
(-α)+α=0
```

は additive inverse + commutativity/symmetry + ZERO propagation に trace。

Unrelated branches の premises を直接混入させない。

---

# 29. Phase 12 normalization boundary

Phase 12 の重要な design boundary:

```text
α+β                    !=structural β+α
(α+β)+γ                !=structural α+(β+γ)
2α                     !=structural α+α
α+0                    !=structural α
0+α                    !=structural α
```

この差異は bug ではない。

Expression tree は syntax。

Mathematical equivalence は explicit Relation。

Therefore:

```text
syntax normalization
```

と:

```text
mathematical theorem reasoning
```

を分離する。

---

# 30. Phase 12 active-rule scope boundary

Concrete additive rules are explicit rule instances.

Examples:

```text
additive_inverse_inference_rule(alpha)
sum_commutativity_inference_rule(alpha,beta)
sum_associativity_inference_rule(alpha,beta,gamma)
double_equals_repeated_sum_inference_rule(alpha)
```

Active rule set にない theorem は自動適用しない。

Example:

```text
double bridge only
→ α+α=2α
```

ORDER rule を active にしない限り:

```text
2α=0
```

は出ない。

ZERO propagation rule を active にしない限り:

```text
α+α=0
```

は出ない。

---

# 31. Phase 12 termination boundary

Finite concrete additive rule set は finite expression closure の範囲で
duplicate rejection により `FIXED_POINT` を期待できる。

Phase 12 は以下を導入しない:

```text
arbitrary expression enumeration
universal recursive sum rewriting
automatic operand sorting
automatic associative flattening
general nα expansion
recursive additive normalization engine
```

それらを将来導入する場合は termination / search-space specification を
別 Phase で設計する。

---

# 32. Phase 12 completion criteria

Phase 12 completion criteria:

1. `Sum` が first-class Expression。
2. nested Sum が lossless。
3. inverse を `Multiple(-1, α)` で表現。
4. `Multiple` と repeated Sum を structural に分離。
5. zero-addition expressions を lossless に保持。
6. additive inverse ZERO rule。
7. commutativity equality rule。
8. associativity equality rule。
9. `α+α=2α` bridge。
10. ORDER reasoning と additive syntax の接続。
11. representative additive scenario。
12. provenance regression。
13. normalization boundary regression。
14. active rule-set scope regression。
15. finite concrete closure が `FIXED_POINT`。
16. generic inference engine 無改変。
17. full regression PASS。

Current verified full suite:

```text
809 passed in 62.32s
```

---

# 33. Phase 12 non-goals

Phase 12 では実装しない:

- `α+0=α` theorem rule
- `0+α=α` theorem rule
- general `nα ↔ repeated Sum`
- distributivity
- map additivity / homomorphism preservation
- Hopf additivity
- composition bilinearity
- theorem-aware additive canonicalization
- first-class `±α`
- first-class membership
- first-class subset relation
- coset / modulo
- symbolic odd/even scalar constraints
- Toda bracket
- Steenrod operations
- double EHP
- odd-primary theorem family

---

# 34. Current limitations

## 34.1 Conclusion identity

ordinary Python equality。

No theorem-aware canonical equivalence。

## 34.2 Alternative proofs

same conclusion の multiple candidate derivations は trace に残り得るが、
knowledge state は first accepted step を保持する。

## 34.3 Pattern language

structured Relation / dataclass statement matching は可能。

arbitrary recursive symbolic unification は未導入。

## 34.4 Unbound substitution

unbound `PatternVariable` は `None` へ substitute される。

Domain rule design で必要 variable を bind する。

## 34.5 Search performance

exhaustive assignment は combinatorial growth を持つ。

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 34.6 Termination

arbitrary symbolic rule family の termination proof は行わない。

`max_rounds` は safety bound。

Repeated Suspension / composition functoriality / recursive Hopf family は
unbounded structural growth の concrete examples。

Current additive concrete rule family は finite explicit scope で利用する。

---

# 35. Phase 13 boundary

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

Phase 12 で Abelian group expression の最小基盤を導入したため、
次の自然な Phase は Homomorphism reasoning。

候補:

```text
f(α+β)=f(α)+f(β)
f(-α)=-f(α)
f(nα)=n f(α)
f(0)=0
```

ただし Phase 13 でも actual mathematical need を先に固定し、
E/H/P を含む各 map にどの homomorphism law が適用可能かを明示する。

generic engine の変更は、actual homomorphism theorem が current rule
language で表現できないと実証された場合のみ。

---

# 36. Testing principle

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

# 37. Documentation policy

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
