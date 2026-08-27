# ehp_proof 設計メモ

この文書は Phase 10 完了時点の current architecture / semantics /
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

逆向き依存を作らない。

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

Expression layer は:

- theorem applicability
- stable range
- dimension validation
- zero / equality proof
- normalization

を担当しない。

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

Phase 10 では `NONZERO` relation type は導入しない。

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

Theorem semantics は domain layer の責務。

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

One round 内で生成された conclusion を、その same round 内の別 rule の
新しい premise として逐次再利用する semantics ではない。

したがって rule chain:

```text
A
↓ rule 1
B
↓ rule 2
C
```

は、B が新規なら C は通常 next productive round で生成される。

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

EHP / ORDER / Suspension / Freudenthal reflection / Toda composition が同じ
generic relation layer を共有する。

---

# 10. Phase 6 EHP rule family

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
```

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

Suspension-derived facts は generic `Relation`。

Repeated Suspension は distinct nested expressions を無限に生成し得る。

```text
x=y
→ E(x)=E(y)
→ E²(x)=E²(y)
→ ...
```

したがって staged / bounded execution を必要に応じて使う。

---

# 13. Phase 9 principal design

Phase 9 は expression-level Suspension と theorem-level suspension map を
分離する。

```text
Suspension(expression)
```

は expression structure。

```text
SuspensionMapStatement(
  sphere_dimension,
  stem,
)
```

は Freudenthal theorem applicability metadata。

---

# 14. SuspensionMapStatement

Fields:

```text
sphere_dimension
stem
```

Map identity は dataclass structural equality。

Reflection rule は同じ `SuspensionMapStatement` を共有する premises にだけ
適用する。

---

# 15. Freudenthal range semantics

Stable-isomorphism range:

```text
stem <= sphere_dimension - 2
```

Boundary range:

```text
stem == sphere_dimension - 1
```

Outside current rule range:

```text
stem >= sphere_dimension
```

Outside は「他の theorem も存在しない」という意味ではなく、current
Freudenthal rule family が conclusion を出さないという scope boundary。

---

# 16. Stable isomorphism

```text
stable SuspensionMapStatement
↓
SuspensionIsomorphismStatement
```

Rule:

```text
freudenthal_stable_isomorphism_inference_rule()
```

range check は `match_guard`。

---

# 17. Boundary epimorphism

```text
boundary SuspensionMapStatement
↓
SuspensionEpimorphismStatement
```

Rule:

```text
freudenthal_boundary_epimorphism_inference_rule()
```

stable / boundary rules は overlap しない。

---

# 18. Isomorphism → injectivity

```text
SuspensionIsomorphismStatement(E)
↓
SuspensionInjectiveStatement(E)
```

Rule:

```text
suspension_isomorphism_implies_injective_inference_rule()
```

Reflection では isomorphism を直接使わず explicit injectivity consequence
を一旦導出する。

---

# 19. Map-level equality / ZERO statements

```text
SuspensionMapEqualityStatement(E,x,y)
```

は:

```text
E(x)=E(y)
```

を map `E` に結び付ける。

```text
SuspensionMapZeroStatement(E,x)
```

は:

```text
E(x)=0
```

を map `E` に結び付ける。

These are domain statements, not generic Relations.

---

# 20. Equality reflection

```text
Injective(E)
+
E(x)=E(y)
↓
x=y
```

Conclusion は generic EQUALITY Relation。

Different map は reject。

---

# 21. ZERO reflection

```text
Injective(E)
+
E(x)=0
↓
x=0
```

Conclusion は generic ZERO Relation。

Different map は reject。

---

# 22. Generic reconnection principle

```text
domain theorem / known relation
↓
domain-specific consequence
↓
generic Relation
↓
existing generic relation rules
```

Domain-specific symmetry / transitivity / ZERO propagation は作らない。

---

# 23. Phase 9 fixed-point integration

ZERO chain:

```text
SuspensionMapStatement(E)
+
SuspensionMapZeroStatement(E,x)
↓ round 1
isomorphism(E)
↓ round 2
injective(E)
↓ round 3
x=0
↓
FIXED_POINT
```

---

# 24. Representative Phase 9 scenario

Initial:

```text
stable map E
E(x)=E(y)
E(x)=0
```

Derived:

```text
stable
↓
isomorphism
↓
injectivity
├───────────────┐
↓               ↓
x=y             x=0
↓
y=x
└───────┬───────┘
        ↓
       y=0
```

Final `y=0` は generic `RelationType.ZERO`。

---

# 25. Phase 9 provenance requirements

Each derived step must preserve:

```text
ProofRule.INFERENCE
premises
inference_rule
```

Different suspension maps must not cross-match.

---

# 26. Phase 9 theorem boundary

Formal scope:

```text
stable:
stem <= n - 2
→ isomorphism
→ injectivity
→ equality / ZERO reflection
```

```text
boundary:
stem == n - 1
→ epimorphism only
```

```text
outside:
stem >= n
→ no Freudenthal-derived conclusion
```

---

# 27. Phase 9 termination semantics

Current Freudenthal rule family:

```text
map
→ isomorphism / epimorphism
→ injectivity
→ reflection
```

は finite closure family。

Stable / boundary / outside を同一 run に入れても:

```text
3 productive rounds
↓
FIXED_POINT
```

に到達する。

---

# 28. Phase 10 composition representation

Known composition relation:

```text
α∘β = γ
```

は `Composition` を含む ordinary generic equality として保持する。

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

Toda 専用 statement class は Phase 10 では追加しない。

source / note に literature / Toda provenance を保持できる。

---

# 29. Phase 10 zero-composition bridge

Known:

```text
α∘β = 0
```

から generic ZERO:

```text
α∘β = 0
```

を `RelationType.ZERO` として導出する。

Rule:

```text
composition_equality_to_zero_inference_rule()
```

Applicability は lhs が `Composition` であることを guard する。

Non-composition equality は reject。

EHP zero-composition と Toda zero-composition は同じ generic ZERO layer で
coexist できる。

---

# 30. Suspension preserves composition equality

Generic rule:

```text
x=y
→ E(x)=E(y)
```

を composition equality にそのまま適用する。

```text
α∘β = γ
↓
E(α∘β) = Eγ
```

専用 composition-Suspension statement は作らない。

---

# 31. Suspension–composition functoriality

Rule:

```text
suspension_composition_functoriality_inference_rule()
```

Semantics:

```text
α∘β = γ
↓
E(α∘β) = Eα∘Eβ
```

Conclusion:

```python
Relation(
  lhs=Suspension(
    expression=Composition(
      left=alpha,
      right=beta,
    ),
  ),
  rhs=Composition(
    left=Suspension(
      expression=alpha,
    ),
    right=Suspension(
      expression=beta,
    ),
  ),
  relation_type=RelationType.EQUALITY,
)
```

Rule applicability は premise relation の lhs が `Composition` の場合に限定。

この rule は composition の theorem semantics を表す domain rule であり、
generic engine に composition-specific branch を追加しない。

---

# 32. Phase 10 equality closure

Two facts:

```text
E(α∘β) = Eγ
E(α∘β) = Eα∘Eβ
```

から generic symmetry / transitivity を利用して:

```text
Eα∘Eβ = Eγ
```

を導出する。

Phase 10-specific equality closure rule は作らない。

---

# 33. Phase 10 representative scenario

Representative knowledge state:

```text
EHP structural facts
+
Toda zero composition
+
Toda nonzero composition equality
+
Suspension-derived equality
+
functoriality-derived equality
```

EHP branch:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
```

Toda zero branch:

```text
α∘β = 0
↓
generic ZERO
↓
generic ZERO propagation
```

Toda nonzero / Suspension branch:

```text
γ∘δ = ε
├─→ E(γ∘δ)=Eε
└─→ E(γ∘δ)=Eγ∘Eδ
          ↓
    symmetry / transitivity
          ↓
      Eγ∘Eδ=Eε
```

These branches coexist in the same proof / inference infrastructure.

---

# 34. Phase 10 provenance requirements

Representative regression must verify:

```text
EHP exactness step
premises =
(image_step, kernel_step)
```

```text
EHP zero-composition step
premises =
(exactness_step,)
```

```text
EHP generic ZERO step
premises =
(ehp_zero_composition_step,)
```

```text
Toda zero generic ZERO step
premises =
(toda_zero_relation_step source fact,)
```

```text
Suspension equality step
premises =
(toda_nonzero_composition_equality,)
```

```text
functoriality step
premises =
(toda_nonzero_composition_equality,)
```

```text
final Eα∘Eβ=Eγ
premises =
generic equality steps derived from
functoriality + suspended equality
```

Unrelated EHP / Toda-zero / Toda-nonzero branch premises must not be inserted
into direct premises.

---

# 35. Phase 10 termination / inference-scope boundary

## 35.1 Structural rules can be unbounded

Repeated Suspension already established:

```text
E(x)
E²(x)
E³(x)
...
```

Phase 10 adds a second concrete source of unbounded structural growth.

With:

```text
functoriality
+
symmetry
```

we can obtain:

```text
E(α∘β)=Eα∘Eβ
↓ symmetry
Eα∘Eβ=E(α∘β)
↓ functoriality
E(Eα∘Eβ)=E²α∘E²β
↓
...
```

All these conclusions can be structurally distinct.

Therefore unrestricted fixed-point termination is not assumed.

## 35.2 `MAX_ROUNDS` regression

The Phase 10 scope regression runs:

```text
functoriality
+
symmetry
```

with:

```text
max_rounds=3
```

and requires:

```text
InferenceTerminationReason.MAX_ROUNDS
```

It also verifies provenance:

```text
original composition equality
↓
first functoriality
↓
symmetry
↓
second-level functoriality
```

This proves actual expression-depth growth rather than merely checking the
termination enum.

## 35.3 Staged execution

For the representative finite task:

```text
structural stage
  suspension preservation: one round
  functoriality: one round
        ↓
generic finite closure stage
  symmetry
  transitivity
  ZERO propagation
        ↓
FIXED_POINT
```

This execution policy is explicit.

The generic engine is not changed to hide this domain-specific scheduling.

## 35.4 Terminal fixed point

For the finite generic stage, after convergence:

```python
derive_inference_round_result(
  bounded_rules,
  bounded_result.steps,
).new_steps == ()
```

must hold.

---

# 36. Phase 10 NONZERO semantics boundary

Phase 10 does not introduce:

```text
RelationType.NONZERO
```

A known nonzero composition is represented as an equality:

```text
α∘β = γ
```

where the supplied right-hand side is a non-zero expression.

This records the composition result, but does not by itself prove a general
logical proposition:

```text
α∘β ≠ 0
```

A first-class nonzero logic layer is future work.

---

# 37. Current limitations

## 37.1 Conclusion equality

ordinary Python equality を使用。theorem-aware normalization は未導入。

## 37.2 Alternative proofs

equal conclusion に対する knowledge state は first accepted step を保持。

## 37.3 Pattern depth

structured relation / dataclass matching はあるが fully general unification
ではない。

## 37.4 Search performance

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 37.5 General termination

arbitrary symbolic rule family の termination proof は行わない。

`max_rounds` は safety bound であり semantic cycle detector ではない。

## 37.6 Structural expression growth

Repeated Suspension / functoriality can generate unbounded structurally distinct
expressions.

Automatic depth planning / rule scheduling は未導入。

## 37.7 Expression normalization

未導入:

- canonical `E^n`
- canonical composition normalization
- theorem-aware equality
- associativity normalization

## 37.8 Composition algebra

Phase 10 で未導入:

- associativity rule
- identity rule
- bilinearity
- zero-composition algebra beyond explicit rules
- general composition simplification

## 37.9 NONZERO

first-class `NONZERO` relation は未導入。

## 37.10 Phase 9 map metadata

`sphere_dimension` / `stem` は explicit input。automatic extraction は未導入。

## 37.11 Epimorphism consequences

`SuspensionEpimorphismStatement` から:

- preimage existence
- lifting witness
- preimage selection

は導出しない。

## 37.12 Inverse / desuspension

general inverse-map construction / unrestricted desuspension は未導入。

---

# 38. Phase 10 completion criteria

Phase 10 は次を満たしたため完了とする。

1. `Composition` を first-class expression として theorem relations に利用。
2. known composition equality を generic EQUALITY Relation として保持。
3. zero composition equality を generic ZERO へ bridge。
4. EHP zero composition と Toda zero composition が coexist。
5. composition equality に Suspension preservation を適用。
6. Suspension–composition functoriality rule を実装。
7. non-composition equality への functoriality 誤適用を reject。
8. `E(α∘β)=Eγ` を導出。
9. `E(α∘β)=Eα∘Eβ` を導出。
10. generic symmetry / transitivity により `Eα∘Eβ=Eγ` を導出。
11. Toda zero / nonzero composition と EHP branch を representative scenario
    で統合。
12. generic ZERO propagation へ接続。
13. branch-specific provenance を保持。
14. unrelated branch premises の混線を防止。
15. unrestricted functoriality + symmetry が structural depth を増やすことを
    regression 固定。
16. bounded run が `MAX_ROUNDS` を返すことを確認。
17. staged structural execution 後の generic closure が genuine
    `FIXED_POINT` に到達。
18. terminal round `new_steps == ()`。
19. generic engine に Phase 10-specific branch を追加しない。
20. full regression PASS。

---

# 39. Phase 10 completion tests

Focused provenance / termination:

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase10_representative_provenance_is_preserved tests/test_ehp_rules.py::test_phase10_functoriality_scope_and_termination_boundary -v
```

Result:

```text
2 passed in 1.55s
```

Combined EHP / relation:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

Result:

```text
61 passed in 1.94s
```

Full suite:

```powershell
python -m pytest -v
```

Result:

```text
763 passed in 22.32s
```

---

# 40. Phase 11 boundary

Phase 11 も speculative generic-engine refactoring から開始しない。

Candidate actual theorem families:

- Hopf-invariant relations
- literature-backed theorem rules
- further Toda composition relations
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- epimorphism / preimage reasoning

Phase 10 で実装しないもの:

```text
NONZERO relation type
automatic nonzero proof
composition associativity
composition identity
composition bilinearity
canonical composition normalization
canonical E^n normalization
automatic suspension-depth planning
automatic rule scheduling
semantic termination analysis
cycle detection
Toda brackets
Steenrod operations
double EHP
odd-primary-specific theorem families
```

基本原則:

```text
new mathematical knowledge
=
new domain InferenceRule
```

generic engine を変更するのは actual theorem が current rule language で
正しく表現できないと実証された場合のみ。

---

# 41. Testing principle

1. representation test
2. single-rule semantic test
3. invalid premise / non-applicability test
4. multi-round integration
5. generic-rule reconnection
6. provenance test
7. representative scenario
8. theorem / inference-scope boundary
9. termination behavior
10. full regression

---

# 42. Documentation policy

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

current specification は latest README / design を優先する。
