# ehp_proof 開発記録

この文書は Phase 10 完了時点までの開発履歴を、現在の実装と矛盾しない
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

を subgroup equality として扱えるようにした。

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

## Phase 8-1

`Suspension(expression)` を導入。

## Phase 8-2

```text
x=y → E(x)=E(y)
```

## Phase 8-3

```text
x=0 → E(x)=0
```

## Phase 8-4

```text
nα=0 → nE(α)=0
```

## Phase 8-5〜8-9

ORDER / EHP branches と Suspension を統合し、generic reasoning への
reconnection と provenance を固定。

## Phase 8-10

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

主目的:

```text
suspension-map metadata
↓
range judgement
↓
theorem conclusion
↓
injectivity
↓
reflection
↓
generic relation reasoning
```

Generic engine に Freudenthal-specific branch は追加しない。

## Phase 9-1：SuspensionMapStatement

```text
SuspensionMapStatement(
  sphere_dimension,
  stem,
)
```

を導入。

Phase 8 `Suspension(expression)` とは責務を分離。

### 状態

完了

## Phase 9-2：stable / boundary range judgement

Stable:

```text
stem <= sphere_dimension - 2
```

Boundary:

```text
stem == sphere_dimension - 1
```

Outside:

```text
stem >= sphere_dimension
```

を区別。

### 状態

完了

## Phase 9-3：stable range → suspension isomorphism

```text
stable SuspensionMapStatement
↓
SuspensionIsomorphismStatement
```

Boundary / outside は reject。

### 状態

完了

## Phase 9-4：boundary range → suspension epimorphism

```text
boundary SuspensionMapStatement
↓
SuspensionEpimorphismStatement
```

stable / boundary rules の非重複も固定。

### 状態

完了

## Phase 9-5：isomorphism → injectivity → equality reflection

```text
SuspensionIsomorphismStatement(E)
↓
SuspensionInjectiveStatement(E)
```

```text
Injective(E)
+
SuspensionMapEqualityStatement(E,x,y)
↓
Relation(x,y,EQUALITY)
```

### 状態

完了

## Phase 9-6：injectivity → ZERO reflection

```text
Injective(E)
+
SuspensionMapZeroStatement(E,x)
↓
Relation(x,Zero(),ZERO)
```

### 状態

完了

## Phase 9-7：stable range → ZERO reflection fixed-point integration

```text
map
↓
isomorphism
↓
injectivity
↓
x=0
↓
FIXED_POINT
```

### 状態

完了

## Phase 9-8：representative scenario + generic reasoning + provenance

```text
stable map E
+
E(x)=E(y)
+
E(x)=0
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

### 状態

完了

## Phase 9-9：inference-scope / termination / theorem-boundary

Stable / boundary / outside maps を同一 run に投入。

Stable:

```text
→ isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary:

```text
→ epimorphism only
```

Outside:

```text
→ no Freudenthal-derived conclusion
```

Termination:

```text
3 productive rounds
↓
FIXED_POINT
```

Phase 9 completion:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 10：Composition reasoning / Suspension–composition functoriality

Phase 10 は Toda composition relations を current generic Relation /
Expression infrastructure に接続する actual theorem / relation family として
進めた。

基本方針:

```text
Toda-specific engine
```

を作るのではなく、

```text
Composition
+
Relation(EQUALITY / ZERO)
+
Suspension
+
generic equality / ZERO rules
```

を組み合わせる。

Generic engine の変更は行わない。

---

# Phase 10-1〜10-5：composition relation foundation

Known composition relation:

```text
α∘β = γ
```

を structured `Composition` を含む generic `RelationType.EQUALITY` として
扱う。

Known zero composition:

```text
α∘β = 0
```

から generic ZERO relation:

```text
Relation(
  lhs=α∘β,
  rhs=0,
  relation_type=ZERO,
)
```

へ bridge する rule を追加。

EHP-derived zero composition と Toda zero composition が同じ fixed-point
knowledge state で coexist できることを確認。

### 状態

完了

---

# Phase 10-6：`E(α∘β)` と composition internal structure

Phase 8 で導入した:

```text
Suspension(expression)
```

は `Composition` を nested expression としてそのまま保持できる。

したがって:

```text
E(α∘β)
```

を別 class へ展開せず:

```python
Suspension(
  expression=Composition(
    left=alpha,
    right=beta,
  ),
)
```

として表現する。

この representation により composition 内部構造を lossless に保持。

### 状態

完了

---

# Phase 10-7：Suspension–composition functoriality

Rule:

```text
suspension_composition_functoriality_inference_rule()
```

Known:

```text
α∘β = γ
```

から:

```text
E(α∘β) = Eα∘Eβ
```

を導出。

Applicability は lhs が `Composition` である equality に限定。

Non-composition equality は reject。

### 状態

完了

---

# Phase 10-8：Suspension equality closure

Known composition equality:

```text
α∘β = γ
```

に対して2経路を作る。

Path A:

```text
α∘β = γ
↓ Suspension preserves equality
E(α∘β) = Eγ
```

Path B:

```text
α∘β = γ
↓ functoriality
E(α∘β) = Eα∘Eβ
```

Generic equality symmetry / transitivity により:

```text
Eα∘Eβ = Eγ
```

を導出。

Phase 10-specific transitivity rule は追加しない。

### 状態

完了

---

# Phase 10-9：representative integration

Representative scenario:

```text
EHP
+
Toda zero composition
+
Toda nonzero composition equality
+
Suspension / functoriality
+
generic ZERO / equality reasoning
```

を1つの integration scenario で確認。

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

重要な実装境界:

`Suspension` preservation と functoriality を unrestricted fixed-point rule
set に同時投入しない。

理由は structural expression depth が無制限に増え得るため。

Phase 10-9 representative test は structural rules を explicit one-round
stage として適用後、generic finite closure を fixed point まで実行。

### 状態

完了

---

# Phase 10-10：representative provenance / termination boundary

Phase 10-10 では新しい production rule は追加しない。

追加した regression:

```text
test_phase10_representative_provenance_is_preserved
```

```text
test_phase10_functoriality_scope_and_termination_boundary
```

## Provenance regression

EHP branch:

```text
image_step + kernel_step
↓
exactness_step
↓
ehp_zero_composition_step
↓
ehp_zero_step
```

Toda zero branch:

```text
toda_zero_step
↓
toda_zero_relation_step
```

Toda nonzero / Suspension branch:

```text
toda_nonzero_step
├─→ suspended_equality_step
└─→ functoriality_step
          ↓
    generic equality closure
          ↓
componentwise_result_step
```

各 step の:

```text
ProofRule.INFERENCE
premises
inference_rule
```

を確認。

さらに unrelated branch premise が direct dependency に混入しないことを
regression 固定。

## Termination / inference-scope regression

当初:

```text
functoriality
+
symmetry
```

を `max_rounds=2` で実行し、second-level functoriality conclusion を期待した。

しかし actual engine semantics では same-round newly derived step は同 round
で次 rule の premise として逐次利用されないため、chain は:

```text
Round 1
E(α∘β)=Eα∘Eβ

Round 2
Eα∘Eβ=E(α∘β)

Round 3
E(Eα∘Eβ)=E²α∘E²β
```

となる。

この実際の round semantics に合わせて `max_rounds=3` に修正。

Regression は:

```text
InferenceTerminationReason.MAX_ROUNDS
round_count == 3
```

を要求し、さらに:

```text
original composition equality
↓
first functoriality
↓
symmetry
↓
second-level functoriality
```

の provenance を確認。

これにより「単に MAX_ROUNDS になった」だけでなく、実際に distinct
expression depth が増加していることを仕様化した。

## Bounded / staged side

Structural rules を explicit one-round で適用後:

```text
symmetry
+
transitivity
```

だけを fixed-point closure すると:

```text
Eα∘Eβ = Eγ
```

へ到達し:

```text
InferenceTerminationReason.FIXED_POINT
```

となる。

Terminal round:

```text
new_steps == ()
```

も確認。

### Phase 10-10 focused result

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase10_representative_provenance_is_preserved tests/test_ehp_rules.py::test_phase10_functoriality_scope_and_termination_boundary -v
```

```text
2 passed in 1.55s
```

### Combined EHP / relation result

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

```text
61 passed in 1.94s
```

### Full regression

```powershell
python -m pytest -v
```

```text
763 passed in 22.32s
```

No failures.

### 状態

完了

---

# Phase 10 completion summary

Architecture progression:

```text
Phase 5
Generic inference engine
        ↓
Phase 6
EHP-derived generic relations
        ↓
Phase 7
ORDER-derived generic relations
        ↓
Phase 8
Suspension transformation
        ↓
Phase 9
Freudenthal theorem reasoning
        ↓
Phase 10
Composition reasoning
+
Suspension–composition functoriality
        ↓
generic equality / ZERO reasoning
        ↓
traceable staged conclusion
```

Phase 10 principal vertical slice:

```text
Toda composition equality
α∘β = γ
        ↓
structured Composition
        ↓
┌──────────────────────────────┐
│                              │
↓                              ↓
Suspension equality       functoriality
↓                              ↓
E(α∘β)=Eγ               E(α∘β)=Eα∘Eβ
└──────────────┬───────────────┘
               ↓
       generic equality closure
               ↓
          Eα∘Eβ=Eγ
```

同時に:

```text
EHP zero composition
Toda zero composition
Toda nonzero composition equality
generic ZERO propagation
```

を同じ proof/inference infrastructure 上で統合。

成果:

1. composition fact を structured generic equality として扱える。
2. zero composition を generic ZERO へ bridge。
3. EHP / Toda zero branches が coexist。
4. composition equality を Suspension できる。
5. Suspension–composition functoriality を rule 化。
6. generic equality closure で componentwise suspended composition と
   suspended result を接続。
7. representative EHP + Toda + Suspension scenario。
8. branch-specific provenance。
9. structural rule family の unbounded growth を regression 固定。
10. staged execution policy を明示。
11. bounded generic stage は genuine fixed point。
12. generic engine 無改変。
13. full suite 763 PASS。

### 状態

完了

---

# Phase 10 completion boundary

Phase 10 で実装しないもの:

```text
RelationType.NONZERO
automatic proof of nonzeroness
composition associativity
composition identity
composition bilinearity
canonical composition normalization
canonical E^n normalization
automatic suspension-depth planning
automatic rule scheduling
semantic cycle detection
general termination proof
Toda bracket
Steenrod operations
double EHP
odd-primary-specific theorem families
```

`max_rounds` は引き続き safety bound。

Structural rules の scope は caller / scenario 側で明示する。

---

# Phase 11 boundary

Phase 11 も speculative generic-engine work から開始しない。

候補 actual theorem families:

- Hopf-invariant relations
- literature-backed theorem rules
- further Toda composition relations
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- epimorphism / preimage reasoning

基本原則:

```text
new mathematical theorem
=
new domain InferenceRule
```

generic engine を変更するのは actual theorem が current rule language では
正しく表現できないと実証された場合のみ。

---

# Current verified status

Phase 10 completion:

```text
763 passed in 22.32s
```

Combined EHP / relation:

```text
61 passed in 1.94s
```

Phase 10-10 focused:

```text
2 passed in 1.55s
```

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
