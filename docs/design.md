# ehp_proof 設計メモ

この文書は Phase 9 完了時点の current architecture / semantics /
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

EHP / ORDER / Suspension / Phase 9 reflection が同じ generic relation layer
を共有する。

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

理由:

1. theorem consequence を明示する
2. provenance を細かく保持する
3. equality / ZERO reflection で共有できる
4. future theorem family から injectivity を与える余地を残す

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

Rule:

```text
suspension_injectivity_reflects_equality_inference_rule()
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

Rule:

```text
suspension_injectivity_reflects_zero_inference_rule()
```

Conclusion は generic ZERO Relation。

Different map は reject。

---

# 22. Generic reconnection principle

```text
Freudenthal theorem
↓
injectivity
↓
equality / ZERO reflection
↓
generic Relation
↓
existing generic relation rules
```

Freudenthal-specific symmetry / transitivity / ZERO propagation は作らない。

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

# 25. Provenance requirements

```text
map_step
↓
isomorphism_step
↓
injective_step
├─────────────────────────┐
│ + suspended equality    │ + suspended zero
↓                         ↓
reflected equality        reflected zero
↓                         │
symmetric equality        │
└────────────┬────────────┘
             ↓
       propagated zero
```

Each derived step must preserve:

```text
ProofRule.INFERENCE
premises
inference_rule
```

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

Current Phase 9 では:

```text
epimorphism → injectivity
```

を導入しない。

したがって boundary から reflection を行わない。

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

Phase 8 repeated Suspension の bounded-execution semantics と明確に区別する。

---

# 28. Current limitations

## 28.1 Conclusion equality

ordinary Python equality を使用。theorem-aware normalization は未導入。

## 28.2 Alternative proofs

equal conclusion に対する knowledge state は first accepted step を保持。

## 28.3 Pattern depth

structured relation / dataclass matching はあるが fully general unification
ではない。

## 28.4 Search performance

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 28.5 General termination

arbitrary symbolic rule family の termination proof は行わない。

## 28.6 Phase 9 map metadata

`sphere_dimension` / `stem` は explicit input。automatic extraction は未導入。

## 28.7 Epimorphism consequences

`SuspensionEpimorphismStatement` から:

- preimage existence
- lifting witness
- preimage selection

は導出しない。

## 28.8 Inverse / desuspension

general inverse-map construction / unrestricted desuspension は未導入。

---

# 29. Phase 9 completion criteria

Phase 9 は次を満たしたため完了とする。

1. suspension map metadata を first-class statement として表現。
2. stable / boundary range を判定。
3. stable → isomorphism。
4. boundary → epimorphism。
5. stable / boundary rules の非重複。
6. isomorphism → explicit injectivity。
7. injectivity → equality reflection。
8. injectivity → ZERO reflection。
9. different maps を混同しない。
10. reflected facts が generic Relation へ戻る。
11. generic equality / ZERO reasoning へ再接続。
12. representative branch / merge scenario。
13. provenance 保持。
14. stable / boundary / outside scope を regression 固定。
15. genuine FIXED_POINT。
16. generic engine に Freudenthal-specific branch を追加しない。
17. full regression PASS。

---

# 30. Phase 10 boundary

Phase 10 も speculative generic-engine refactoring から開始しない。

候補:

- Hopf invariant relations
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- future epimorphism / preimage reasoning

actual theorem が current rule language で表現できないと実証された場合のみ
generic engine を拡張する。

---

# 31. Testing principle

1. representation test
2. single-rule semantic test
3. invalid premise / non-applicability test
4. multi-round integration
5. generic-rule reconnection
6. provenance test
7. representative scenario
8. theorem boundary / inference-scope test
9. termination behavior
10. full regression

---

# 32. Documentation policy

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
