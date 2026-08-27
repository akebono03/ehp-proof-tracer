# ehp_proof 開発記録

この文書は Phase 8 完了時点までの開発履歴を、
現在の実装と矛盾しない形で整理した改訂版である。

読み方:

```text
各 Phase の「未実装」「次の課題」
=
その Phase 時点の historical statement
```

current specification は README.md / docs/design.md を優先する。

---

# Phase 1：有限群計算の安定化

## 主な成果

- `GroupElement`
- `GroupMap.apply()`
- `GroupMap.kernel()`
- `GroupMap.image()`
- EHP exactness test
- finite examples の regression

### 状態

完了

---

# Phase 2：structured subgroup

## 主な成果

- `Subgroup`
- kernel subgroup
- image subgroup
- subgroup equality
- subgroup generators
- subgroup abstract structure

Exactness:

```text
Im(f)=Ker(g)
```

を subgroup equality として扱えるようにした。

### 状態

完了

---

# Phase 3：quotient / exact sequence / extension

## 主な成果

- `QuotientGroup`
- induced quotient map
- first-isomorphism checks
- `ExactSequenceStep`
- quotient / image structure comparison
- finite extension middle-group candidates
- EHP integration

到達点:

```text
EHP data
↓
kernel / image
↓
exact sequence
↓
quotient
↓
extension candidates
```

### 状態

完了

---

# Phase 4：presentation-based finitely generated abelian groups

有限群列挙中心から:

```text
Z^r ⊕ finite torsion
```

へ一般化。

## 主な成果

- presentation representation
- relation matrix
- integer lattice
- HNF / SNF
- general kernel / image / cokernel
- free / torsion / mixed maps
- non-diagonal maps
- zero maps / zero groups
- presentation-based exactness
- EHP integration
- finite-enumeration cross-check

### 状態

完了

---

# Phase 5：Proof / Generic Inference Engine

Phase 5 の目的:

```text
why this conclusion follows
```

を traceable にする generic inference foundation の構築。

Phase 5-65 を foundation completion point とする。

## 主な model

- `Relation`
- `ProofStep`
- `Proof`
- `LiteratureReference`
- `Expression`
- `Zero`
- `HomotopyElement`
- `Multiple`
- `Composition`
- `InferenceRule`
- `PremisePattern`
- `InferenceMatch`
- `PatternVariable`
- `VariableBinding`

## 推論 engine

段階的に:

- premise pattern matching
- multiple premises
- exhaustive premise assignments
- deterministic backtracking
- shared binding consistency
- conclusion builder
- conclusion pattern substitution
- recursive dataclass substitution
- one-round execution
- duplicate rejection
- fixed-point execution
- max-round bounded execution
- per-round trace
- application result
- rejection reason
- branch / merge
- multi-rule propagation

を実装。

## Phase 5 到達点

```text
known ProofSteps
+
InferenceRules
↓
matching
↓
bindings
↓
application
↓
new ProofSteps
↓
fixed-point iteration
↓
trace
```

### 状態

完了

---

# Phase 6：EHP domain inference foundation

generic engine 自体をさらに作る段階から、
actual EHP mathematics を `InferenceRule` として投入する段階へ移行。

## Phase 6-1：Image + Kernel → Exactness

```text
Image(first_map)
+
Kernel(second_map)
↓
Exactness(first_map, second_map)
```

## Phase 6-2 / 6-3：structured statement support

- dataclass statement matching
- statement conclusion substitution
- `match_guard`

を整備。

actual EHP rule が要求した generic capability の追加として実施。

## Phase 6-4 / 6-5：Exactness propagation

```text
Exactness + Image → Kernel
```

```text
Exactness + Kernel → Image
```

## Phase 6-6：fixed-point integration

相互伝播 rule を同一 run で検証。

## Phase 6-7：Exactness → EHP zero composition

```text
Exactness
↓
EHPZeroCompositionStatement
```

## Phase 6-8：two-round integration

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
```

## Phase 6-9：EHP zero composition → generic ZERO

```text
EHPZeroCompositionStatement
↓
Composition(second_map, first_map)=0
```

## Phase 6-11 / 6-13：composition ZERO propagation

composition-specific ZERO propagation を equality 両向きで実装。

## Phase 6-14：equality symmetry

```text
x=y
↓
y=x
```

## Phase 6-16：equality transitivity

```text
x=y
y=z
↓
x=z
```

## Phase 6-18 / 6-19：equality closure / ZERO propagation

symmetry + transitivity の fixed-point closure から、
derived equality を ZERO propagation が利用できるようにした。

## Phase 6 representative completion

```text
EHP structural facts
↓
EHP-specific inference
↓
generic ZERO
↓
equality closure
↓
ZERO propagation
↓
traceable target relation
↓
genuine fixed point
```

generic engine に EHP-specific branch を追加しなかった。

### 状態

完了

---

# Phase 7：Element-order reasoning

Phase 7 は first non-EHP theorem family として exact finite element order
を選択。

## Phase 7-1：ORDER semantics

Concrete representation:

```text
ord(α)=n
```

with exact positive finite additive order semantics.

`order_relation()` を導入し:

- positive int のみ accept
- bool reject
- zero / negative reject
- float / string reject

を固定。

## Phase 7-2：ORDER → zero multiple

```text
ord(α)=n
↓
nα=0
```

Rule:

```text
order_implies_zero_multiple_inference_rule()
```

## Phase 7-3：generic ZERO propagation

expression-type-independent:

```text
x=0
y=x
↓
y=0
```

を導入。

ORDER-derived ZERO が generic reasoning へ入れるようになった。

## Phase 7-4：equality closure integration

```text
ord(α)=n
↓
nα=0
↓
equality closure
↓
target=nα
↓
target=0
```

を確認。

## Phase 7-5：EHP / ORDER coexistence

same fixed-point knowledge state に:

```text
EHP-derived ZERO
ORDER-derived ZERO
```

を同時に保持できることを確認。

## Phase 7-6：provenance

EHP chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
EHP ZERO
```

ORDER chain:

```text
ORDER fact
↓
ORDER ZERO
```

が混線しないことを確認。

## Phase 7-7：representative completion scenario

EHP / ORDER / equality / generic ZERO rules を1 run へ統合。

final state へ追加 round を適用して:

```text
new_steps == ()
```

を確認。

Phase 7 completion full suite:

```text
706 passed in 60.22s
```

### 状態

完了

---

# Phase 8：Suspension reasoning

Phase 8 は Phase 7 後の actual mathematical rule family として
Suspension preservation を選択した。

目的:

```text
EHP / ORDER から得た relation
↓
Suspension
↓
generic relation reasoning へ再接続
```

を既存 generic engine 上で実現する。

---

# Phase 8-1：Suspension expression representation

Expression layer に:

```python
@dataclass(frozen=True)
class Suspension(Expression):
  expression: Expression
```

を追加。

単一 Suspension:

```text
E(α)
```

だけでなく nested form:

```text
E²(α)
E³(α)
```

を構造として表現できる。

Expression 自体には theorem semantics / dimension validation は持たせない。

## Regression

- construction
- nested structural equality
- inner expression preservation

を確認。

### 状態

完了

---

# Phase 8-2：Suspension preserves equality

Rule:

```text
suspension_preserves_equality_inference_rule()
```

を追加。

Semantics:

```text
x=y
↓
E(x)=E(y)
```

Output は ordinary generic `RelationType.EQUALITY`。

非 equality relation は match しない。

Derived `ProofStep` は:

```text
ProofRule.INFERENCE
```

を持ち、source `InferenceRule` と premise を保持する。

### 状態

完了

---

# Phase 8-3：Suspension preserves ZERO

Rule:

```text
suspension_preserves_zero_inference_rule()
```

Semantics:

```text
x=0
↓
E(x)=0
```

non-ZERO relation は reject。

Output は ordinary generic `RelationType.ZERO`。

### 状態

完了

---

# Phase 8-4：Suspension preserves zero multiple

Rule:

```text
suspension_preserves_zero_multiple_inference_rule()
```

Semantics:

```text
nα=0
↓
nE(α)=0
```

Coefficient `n` は保存し、expression `α` を Suspension する。

Known-zero lhs が `Multiple` であることを guard で確認。

### 状態

完了

---

# Phase 8-5：ORDER-derived zero multiple → Suspension

Phase 7 ORDER rule と Phase 8 multiple-Suspension rule を接続。

```text
ord(α)=n
↓ round 1
nα=0
↓ round 2
nE(α)=0
```

を確認。

provenance:

```text
order_step
↓
order_zero_step
↓
suspended_zero_step
```

を保持。

### 状態

完了

---

# Phase 8-6：Suspension-derived equality → generic ZERO propagation

Starting facts:

```text
x=y
y=0
```

Suspension rules:

```text
E(x)=E(y)
E(y)=0
```

generic ZERO propagation:

```text
E(x)=0
```

へ再接続できることを確認。

この Phase により:

```text
Suspension-derived facts
=
ordinary generic Relation facts
```

という design が実証された。

Suspension-specific ZERO propagation rule は追加していない。

### 状態

完了

---

# Phase 8-7：EHP-derived ZERO → Suspension

Existing EHP chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
Composition(H,E)=0
```

へ Suspension rule を追加し:

```text
E(Composition(H,E))=0
```

を導出。

productive rounds を明示的に追跡し、
premises / source rule / `ProofRule.INFERENCE` を確認。

### 状態

完了

---

# Phase 8-8：EHP + ORDER + Suspension representative scenario

Representative scenario に2 branch を統合。

## EHP branch

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
Composition(H,E)=0
↓
E(Composition(H,E))=0
```

## ORDER branch

```text
ord(α)=n
↓
nα=0
↓
nE(α)=0
```

Both branches を one evolving knowledge state で保持。

Final state で:

```text
EHP ZERO
ORDER ZERO
suspended EHP ZERO
suspended ORDER ZERO
```

が共存することを確認。

Phase 8-8 では Suspension depth を staged `run_inference_round()` calls で
制御した。

### 状態

完了

---

# Phase 8-9：representative provenance chain regression

Phase 8-8 で得られた representative chain の provenance を
独立 regression specification として固定。

## EHP provenance

```text
image_step + kernel_step
↓
exactness_step
↓
zero_composition_step
↓
ehp_zero_step
↓
suspended_ehp_zero_step
```

## ORDER provenance

```text
order_step
↓
order_zero_step
↓
suspended_order_zero_step
```

Assertions include:

- exact premises
- exact source `InferenceRule`
- `ProofRule.INFERENCE`
- EHP branch に ORDER step が入らない
- ORDER branch に EHP structural step が入らない
- suspended result 同士が相互 premise にならない

### 状態

完了

---

# Phase 8-10：Suspension termination / inference-scope boundary

Phase 8 の最重要設計境界を regression test として固定。

## 問題

Suspension preservation rule はその own conclusion へ再適用できる。

Example:

```text
x=0
↓
E(x)=0
↓
E²(x)=0
↓
E³(x)=0
↓
...
```

nested Suspension はすべて distinct conclusion。

したがって ordinary conclusion duplicate rejection では停止しない。

同じ問題が:

- EQUALITY preservation
- ZERO preservation
- zero-multiple preservation

の3種類すべてに存在する。

## 仕様判断

Suspension theorem を人工的に弱めない。

次の guard は追加しない:

```text
already suspended expression
→ rule does not apply
```

数学的 applicability と execution scope を分離する。

## Regression 1：bounded fixed-point scope

各 Suspension rule を:

```python
run_inference_until_stable_with_history(
  ...,
  max_rounds=2,
)
```

で実行。

2 levels of nested Suspension が生成され、
termination reason が:

```text
MAX_ROUNDS
```

になることを確認。

この behavior を expected specification とした。

## Regression 2：active rule-set scope

Single:

```python
run_inference_round()
```

では:

```text
x=0
→
E(x)=0
```

まで。

同じ Suspension rule を次 round でも active にした場合のみ:

```text
E²(x)=0
```

を生成する。

これにより Phase 8 の staged execution strategy を formal specification
として固定した。

## Production code

Phase 8-10 では production code を変更していない。

変更は regression tests のみ。

generic inference engine へ:

- Suspension depth
- theorem-specific cycle detection
- automatic apply-once behavior

は追加していない。

### 状態

完了

---

# Phase 8 completion summary

Phase 8 の成果:

1. `Suspension` expression を導入した。
2. nested Suspension を表現可能にした。
3. equality preservation rule を実装した。
4. ZERO preservation rule を実装した。
5. zero-multiple preservation rule を実装した。
6. ORDER-derived zero multiple を Suspension へ接続した。
7. Suspension-derived equality / ZERO を generic relation reasoning へ再接続した。
8. EHP-derived ZERO を Suspension へ接続した。
9. EHP + ORDER + Suspension representative scenario を構築した。
10. EHP / ORDER branch provenance を regression test で固定した。
11. repeated Suspension が generally unbounded closure を持つことを明示した。
12. bounded execution の `MAX_ROUNDS` semantics を固定した。
13. staged `run_inference_round()` による inference scope を仕様化した。
14. Suspension-specific generic-engine branch を導入しなかった。
15. full regression suite が pass した。

Architecture progression:

```text
Phase 5
generic inference engine foundation
        ↓
Phase 6
EHP-derived generic relations
        ↓
Phase 7
ORDER-derived generic relations
        ↓
Phase 8
Suspension transforms generic relations
        ↓
EHP + ORDER + Suspension coexistence
        ↓
traceable provenance
        ↓
explicit execution-scope boundary
```

### 状態

完了

---

# Phase 8 completion tests

Phase 8-10 focused tests:

```powershell
python -m pytest tests/test_relation_rules.py::test_suspension_preservation_rules_require_bounded_fixed_point_scope tests/test_relation_rules.py::test_suspension_reasoning_scope_is_controlled_by_active_rule_set -v
```

Result:

```text
2 passed in 0.18s
```

Relation-rule suite:

```powershell
python -m pytest tests/test_relation_rules.py -v
```

Result:

```text
28 passed in 0.12s
```

EHP + relation rules:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

Result:

```text
50 passed in 1.95s
```

Full suite:

```powershell
python -m pytest -v
```

Result:

```text
721 passed in 22.16s
```

No failures.

---

# Phase 8 completion boundary

Phase 8 で実装しないもの:

```text
automatic dimension validation
Freudenthal suspension theorem
stable range detection
stable isomorphism / epimorphism rules
automatic suspension depth planning
canonical E^n representation
expression normalization
theorem-aware equality
desuspension
automatic order preservation beyond explicit zero-multiple rule
Hopf invariant theorem family
Toda composition relations
Toda brackets
Steenrod operations
double EHP
odd-primary-specific rule families
```

これらを Phase 8 の scope に先取りしない。

---

# Phase 9 boundary

Phase 9 も speculative generic-engine work から開始しない。

Phase 8 の explicit Suspension representation を利用する actual theorem
family を選ぶ。

Natural candidate:

```text
Freudenthal / stable-range reasoning
```

Other candidates:

- Hopf invariant relations
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families

基本原則:

```text
new mathematical theorem
=
new domain InferenceRule
```

generic engine の変更は actual theorem が現在の rule language で正しく
表現できないと確認された場合のみ行う。

---

# Current verified status

At Phase 8 completion:

```text
721 passed in 22.16s
```

Combined EHP / relation suite:

```text
50 passed
```

Relation-rule suite:

```text
28 passed
```

Phase 8 termination / scope focused tests:

```text
2 passed
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
