# ehp_proof 開発記録

この文書は Phase 11 完了時点までの開発履歴を、現在の実装と矛盾しない
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

## Phase 9-3〜9-7

Stable range から suspension isomorphism、injectivity、equality / ZERO
reflection へ接続。

Boundary は epimorphism only。

## Phase 9-8〜9-9

Representative scenario、generic reasoning、provenance、theorem boundary、
finite fixed-point termination を固定。

Phase 9 completion:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 10：Composition reasoning / Suspension-composition functoriality

Phase 10 は Toda composition relations を current generic Relation /
Expression infrastructure に接続する actual theorem / relation family として
進めた。

Generic engine の変更は行わない。

## Phase 10-1〜10-5：composition relation foundation

Known:

```text
α∘β = γ
```

を structured `Composition` を含む generic equality として扱う。

Known zero composition:

```text
α∘β = 0
```

から generic ZERO へ bridge。

EHP-derived ZERO と Toda-derived ZERO が coexist。

## Phase 10-6：`E(α∘β)` internal structure

```python
Suspension(
  expression=Composition(
    left=alpha,
    right=beta,
  ),
)
```

として composition internal structure を lossless に保持。

## Phase 10-7：Suspension-composition functoriality

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

Non-composition equality は reject。

## Phase 10-8：generic equality closure

```text
E(α∘β)=Eγ
E(α∘β)=Eα∘Eβ
↓
Eα∘Eβ=Eγ
```

Phase 10-specific transitivity rule は追加しない。

## Phase 10-9：representative integration

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

を1 scenario で確認。

## Phase 10-10：provenance / termination boundary

`functoriality + symmetry` で structural depth が増え得ることを regression
固定。

Bounded side:

```text
MAX_ROUNDS
```

Staged finite side:

```text
FIXED_POINT
```

Phase 10 completion:

```text
763 passed in 22.32s
```

### 状態

完了

---

# Phase 11：Generalized Hopf-invariant reasoning

Phase 11 は generalized Hopf invariant を actual theorem family として
追加した。

重要な設計判断:

```text
generalized Hopf invariant value
```

を integer 専用にはしない。

```text
H(α)=β
```

の `β` は `Expression` として保持する。

Generic engine は変更しない。

---

# Phase 11-1：generalized Hopf invariant statement

追加:

```text
HopfInvariantStatement
```

Fields:

```text
expression
value
source
note
```

Semantics:

```text
H(expression)=value
```

`value` は `Expression`。

Tests で structural equality、zero value、multiple value、provenance、
proof-step representation を確認。

### 状態

完了

---

# Phase 11-2：known generalized Hopf fact / provenance

Known Hopf fact を `ProofRule.GIVEN` の `ProofStep` として保持。

`LiteratureReference` を statement source に保持可能。

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

を採用。

### 状態

完了

---

# Phase 11-3：first generalized Hopf theorem inference rule

Known:

```text
H(α)=β
```

から:

```text
HopfCompositionLawStatement(
  alpha=α,
  beta=β,
)
```

を導出。

これは actual formula ではなく theorem-applicability intermediate
statement。

### 状態

完了

---

# Phase 11-4：generalized Hopf composition formula

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

Existing `Composition` / `Suspension` を再利用。

Generic engine の変更なし。

### 状態

完了

---

# Phase 11-5：Hopf invariant value ZERO bridge

重要な theorem boundary:

```text
H(x)=0
↛
x=0
```

Implemented bridge:

```text
H(x)=y
+
y=0
↓
H(x)=0
```

Guard により同じ `y` の ZERO のみを許可。

Unrelated ZERO は reject。

### 状態

完了

---

# Phase 11-6：Suspension / composition functoriality 接続

Take:

```text
β=Eδ
```

11-4 gives:

```text
H(α∘Eγ)=Eδ∘Eγ
```

Known:

```text
δ∘γ=0
```

Existing rules から:

```text
E(δ∘γ)=0
```

および:

```text
E(δ∘γ)=Eδ∘Eγ
```

を導出し、symmetry + generic ZERO propagation で:

```text
Eδ∘Eγ=0
```

さらに11-5で:

```text
H(α∘Eγ)=0
```

へ到達。

Production code を増やさず既存 rule family の接続だけで達成。

Phase 11-6:

```text
tests/test_hopf_rules.py
21 passed
```

Full suite:

```text
784 passed
```

### 状態

完了

---

# Phase 11-7：EHP reasoning との接続

Map-level:

```text
H∘E=0
```

と element-level:

```text
H(Eα)=0
```

を区別。

Bridge rule:

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

Integration:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eα)=0
```

Phase 11-7:

```text
tests/test_hopf_rules.py
24 passed
```

Full suite:

```text
787 passed
```

### 状態

完了

---

# Phase 11-8：representative scenario

Same knowledge state で:

```text
Hopf composition branch
+
EHP branch
```

を統合。

Hopf:

```text
H(α)=Eδ
↓
HopfCompositionLawStatement
↓
H(α∘Eγ)=Eδ∘Eγ
↓
Suspension / functoriality / generic ZERO
↓
H(α∘Eγ)=0
```

EHP:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eγ)=0
```

Structural rules は explicit round で適用し、final finite stage は:

```text
FIXED_POINT
```

Phase 11-8:

```text
tests/test_hopf_rules.py
25 passed
```

Full suite:

```text
788 passed
```

### 状態

完了

---

# Phase 11-9：provenance regression

Final conclusion を逆追跡できることを独立 regression として固定。

Hopf branch:

```text
H(α∘Eγ)=0
↓
H(α∘Eγ)=Eδ∘Eγ
↓
HopfCompositionLawStatement(α,Eδ)
↓
H(α)=Eδ
↓
LiteratureReference
```

ZERO branch:

```text
Eδ∘Eγ=0
↓
Suspension ZERO
+
functoriality / symmetry
↓
δ∘γ=0
```

EHP branch:

```text
H(Eγ)=0
↓
EHPZeroCompositionStatement(E,H)
↓
Exactness(E,H)
```

各 derived step の:

```text
premises
inference_rule
ProofRule.INFERENCE
```

を確認。

Phase 11-9:

```text
tests/test_hopf_rules.py
26 passed
```

Full suite:

```text
789 passed
```

### 状態

完了

---

# Phase 11-10：theorem scope / inference termination boundary

新しい production rule は追加しない。

## Theorem scope

Regression で:

```text
H(x)=0
↛
x=0
```

```text
H(x)=y
+
z=0
(y != z)
↛
H(x)=0
```

```text
P∘H=0
↛
H(Eα)=0
```

を固定。

EHP bridge は `E→H` pair のみに限定。

## Phase 11-specific structural growth

Hopf rules 自体にも recursive growth がある:

```text
H(α)=β
↓
Law(α,β)
↓
H(α∘Eγ)=β∘Eγ
↓
Law(α∘Eγ,β∘Eγ)
↓
H((α∘Eγ)∘Eγ)=(β∘Eγ)∘Eγ
↓
...
```

したがって:

```text
hopf_composition_law_inference_rule
+
hopf_composition_formula_inference_rule
```

を unrestricted fixed-point-safe とは扱わない。

Bounded regression:

```text
max_rounds=4
↓
MAX_ROUNDS
```

Staged execution:

```text
explicit law round
↓
explicit formula round
↓
finite Hopf ZERO stage
↓
FIXED_POINT
```

Phase 11-10 focused:

```text
2 passed
```

Phase 11 suite:

```text
28 passed
```

Full suite:

```text
791 passed in 23.41s
```

### 状態

完了

---

# Phase 11 completion summary

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
Composition reasoning /
Suspension-composition functoriality
        ↓
Phase 11
Generalized Hopf invariant
+
Hopf composition formula
+
generic ZERO reconnection
+
EHP bridge
        ↓
traceable staged reasoning
```

Principal Hopf branch:

```text
H(α)=Eδ
↓
HopfCompositionLawStatement
↓
H(α∘Eγ)=Eδ∘Eγ
↓
δ∘γ=0
↓
Suspension / functoriality / generic ZERO
↓
Eδ∘Eγ=0
↓
H(α∘Eγ)=0
```

EHP bridge:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eα)=0
```

Phase 11 verified:

1. generalized Hopf values are expressions, not integer-only;
2. known facts preserve literature provenance;
3. composition-law applicability is explicit;
4. composition formula is structural;
5. generic ZERO values reconnect to Hopf statements;
6. Hopf vanishing is not confused with element vanishing;
7. Suspension / functoriality rules are reused unchanged;
8. EHP facts bridge to element-level Hopf facts only for `E→H`;
9. representative Hopf and EHP branches coexist;
10. provenance is traceable;
11. theorem boundary is regression-fixed;
12. recursive Hopf structural growth is regression-fixed;
13. staged execution reaches genuine fixed point;
14. generic engine remains unchanged;
15. full suite passes.

### 状態

完了

---

# Phase 11 completion boundary

Phase 11 で実装しないもの:

```text
H(x)=0 → x=0
H(x)=0 → x ∈ Im(E)
element-level Ker(H) / Im(E) membership
preimage witness generation
Hopf additivity
general Hopf algebra identities
automatic theorem-depth scheduling
semantic cycle detection
canonical composition normalization
composition associativity
composition bilinearity
NONZERO relation
Toda bracket
Steenrod operations
double EHP
odd-primary-specific theorem families
```

`max_rounds` は引き続き safety bound。

Structural rule family の scope は caller / scenario 側で明示する。

---

# Phase 12 boundary

次 Phase も speculative generic-engine work から開始しない。

Current representation needs:

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
Toda-bracket value set / indeterminacy
```

```text
α=kβ+γ
k odd
```

Other candidates:

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

# Current verified status

Phase 11 suite:

```powershell
python -m pytest tests/test_hopf_rules.py -v
```

```text
28 passed
```

Phase 11-10 focused:

```text
2 passed
```

Full suite:

```powershell
python -m pytest -v
```

```text
791 passed in 23.41s
```

No failures.

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
