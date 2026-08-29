# ehp_proof 開発記録

この文書は Phase 12 完了時点までの開発履歴を、現在の実装と矛盾しない
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

theorem-level Suspension map metadata を導入。

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
Expression infrastructure に接続した。

Generic engine の変更は行わない。

## Phase 10-1〜10-5

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

## Phase 10-6

`E(α∘β)` の internal composition structure を lossless に保持。

## Phase 10-7

Suspension-composition functoriality:

```text
α∘β = γ
↓
E(α∘β)=Eα∘Eβ
```

## Phase 10-8

Generic Suspension preservation と equality closure を使い:

```text
E(α∘β)=Eγ
E(α∘β)=Eα∘Eβ
↓
Eα∘Eβ=Eγ
```

へ接続。

## Phase 10-9〜10-10

Representative EHP + Toda + Suspension scenario、provenance、
termination boundary を固定。

`functoriality + symmetry` で structural depth が増え得るため、
unrestricted fixed-point-safe とは扱わない。

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

## Phase 11-1

`HopfInvariantStatement` を導入。

## Phase 11-2

Known Hopf fact / literature provenance。

## Phase 11-3

```text
H(α)=β
↓
HopfCompositionLawStatement(α,β)
```

## Phase 11-4

```text
HopfCompositionLawStatement(α,β)
↓
H(α∘Eγ)=β∘Eγ
```

## Phase 11-5

```text
H(x)=y
y=0
↓
H(x)=0
```

かつ:

```text
H(x)=0
↛
x=0
```

を theorem boundary として固定。

## Phase 11-6

Suspension / composition functoriality と接続。

## Phase 11-7

EHP `E→H` zero-composition から:

```text
H(Eα)=0
```

へ bridge。

## Phase 11-8〜11-9

Representative Hopf + EHP scenario と provenance regression。

## Phase 11-10

Theorem scope / recursive structural growth / termination boundary を固定。

Phase 11 completion:

```text
791 passed in 23.41s
```

### 状態

完了

---

# Phase 12：Additive expression / reasoning

Phase 12 は proof-expression layer に最小 additive structure を導入した。

目的:

```text
α+β
-α
2α と α+α の関係
```

を structural syntax と theorem relation を分離したまま扱う。

Generic engine は変更しない。

---

# Phase 12-1：Sum minimum representation

追加:

```text
Sum(left,right)
```

Semantics:

```text
α+β
```

Binary tree structure を lossless に保持。

Phase 12-1 completion:

```text
792 passed
```

### 状態

完了

---

# Phase 12-2：Sum structural equality / nested representation

確認:

```text
Sum(α,β) == Sum(α,β)
```

一方:

```text
Sum(α,β) != Sum(β,α)
```

また:

```text
(α+β)+γ
!=structural
α+(β+γ)
```

nested Sum を binary tree のまま保持。

Phase 12-2 completion:

```text
795 passed
```

### 状態

完了

---

# Phase 12-3：Multiple / Zero boundary

固定:

```text
Multiple(2,α)
!=structural
Sum(α,α)
```

および:

```text
Multiple(0,α)
!=structural
Zero()
```

`nα` は `Multiple` のまま維持。

Repeated-Sum normalization は導入しない。

Phase 12-3 completion:

```text
797 passed
```

### 状態

完了

---

# Phase 12-4：inverse minimum representation

Production code は変更せず:

```text
-α
=
Multiple(-1,α)
```

を canonical current representation として固定。

専用 `Inverse` class / helper は導入しない。

Phase 12-4 completion:

```text
798 passed
```

### 状態

完了

---

# Phase 12-5：zero addition representation / boundary

表現可能:

```text
α+0
0+α
```

ただし:

```text
α+0 !=structural α
0+α !=structural α
```

constructor simplification は行わない。

Phase 12-5 completion:

```text
800 passed
```

### 状態

完了

---

# Phase 12-6：additive inverse rule

追加 rule:

```text
α+(-α)=0
```

`-α` は:

```text
Multiple(-1,α)
```

Conclusion は generic `RelationType.ZERO`。

Concrete premise-free rule factory として実装し、
unbound universal variable / expression enumeration は導入しない。

Phase 12-6 completion:

```text
801 passed
```

### 状態

完了

---

# Phase 12-7：commutativity

追加:

```text
α+β = β+α
```

Conclusion は generic `RelationType.EQUALITY`。

Structural equality は変更しない。

Reverse rule は作らず、generic equality symmetry を再利用。

Phase 12-7 completion:

```text
802 passed in 73.20s
```

### 状態

完了

---

# Phase 12-8：associativity

追加:

```text
(α+β)+γ = α+(β+γ)
```

Left / right nested Sum は structural に distinct。

Reverse direction は generic symmetry。

Flattening / canonical association は導入しない。

Phase 12-8 completion:

```text
803 passed in 60.33s
```

### 状態

完了

---

# Phase 12-9：ORDER reasoning integration

Phase 7 ORDER rule:

```text
ord(α)=n
↓
nα=0
```

は変更しない。

最小 bridge:

```text
α+α = 2α
```

のみを explicit equality として追加。

これにより:

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

へ到達。

General:

```text
nα = α+...+α
```

は未実装。

Phase 12-9 completion:

```text
805 passed in 69.50s
```

### 状態

完了

---

# Phase 12-10：representative scenario / provenance

新しい production rule は追加しない。

同一 inference environment に:

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

を配置。

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
+
commutativity
+
generic equality closure
```

を確認。

各 representative conclusion の:

```text
premises
inference_rule
ProofRule.INFERENCE
```

を regression 固定。

Finite scenario は `FIXED_POINT`。

Phase 12-10 completion:

```text
807 passed in 66.07s
```

### 状態

完了

---

# Phase 12-11：normalization / termination boundary

Production code は変更しない。

Normalization boundary:

```text
α+β                    !=structural β+α
(α+β)+γ                !=structural α+(β+γ)
2α                     !=structural α+α
α+0                    !=structural α
0+α                    !=structural α
```

Mathematical equivalence は explicit Relation で表す。

Active rule scope:

```text
bridge only
→ α+α=2α
```

ORDER rule を active にすると:

```text
2α=0
```

ZERO propagation を active にすると:

```text
α+α=0
```

まで到達。

Phase 12 additive rule family は concrete explicit rule scope で利用する。

Recursive normalization / arbitrary expression generation / general repeated
sum expansion は導入しない。

Phase 12-11 completion:

```text
809 passed in 62.32s
```

### 状態

完了

---

# Phase 12 completion summary

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
        ↓
Phase 11
Generalized Hopf reasoning
        ↓
Phase 12
Additive syntax
+
additive inverse
+
commutativity
+
associativity
+
ORDER / Sum bridge
        ↓
generic equality / ZERO reasoning
        ↓
traceable finite fixed point
```

Principal Phase 12 vertical slice:

```text
ord(α)=2
↓
2α=0
```

together with:

```text
α+α=2α
```

gives:

```text
α+α=0
```

through the existing generic ZERO propagation rule.

Separate additive branch:

```text
α+(-α)=0
↓
commutativity / symmetry
↓
(-α)+α=0
```

Associativity and commutativity remain theorem relations rather than AST
normalization.

Phase 12 verified:

1. `Sum` is a first-class Expression.
2. nested sums are structural.
3. additive inverse uses `Multiple(-1,α)`.
4. `Multiple` and repeated `Sum` remain distinct.
5. zero-addition forms remain structural.
6. additive inverse ZERO rule works.
7. commutativity equality rule works.
8. associativity equality rule works.
9. `α+α=2α` bridge works.
10. ORDER reasoning reconnects to additive syntax.
11. representative additive branches coexist.
12. provenance is traceable.
13. normalization boundary is regression-fixed.
14. active rule scope is regression-fixed.
15. finite concrete additive scenario reaches `FIXED_POINT`.
16. generic inference engine remains unchanged.
17. full suite passes.

### 状態

完了

---

# Phase 12 completion boundary

Phase 12 で実装しないもの:

```text
α+0=α theorem
0+α=α theorem
general nα repeated-Sum expansion
map additivity
f(α+β)=f(α)+f(β)
f(-α)=-f(α)
f(nα)=n f(α)
Hopf additivity
composition bilinearity
theorem-aware additive normalization
first-class ±α
first-class membership
subset reasoning
coset / modulo
symbolic odd/even scalar constraints
Toda bracket
Steenrod operations
double EHP
odd-primary-specific theorem families
```

`max_rounds` は引き続き safety bound。

Structural / recursively productive rule family の scope は caller /
scenario 側で明示する。

---

# Phase 13 boundary

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

Phase 12 で additive expression foundation が整ったため、
次の自然な Phase は Homomorphism reasoning。

Candidate actual rules:

```text
f(α+β)=f(α)+f(β)
f(-α)=-f(α)
f(nα)=n f(α)
f(0)=0
```

E, H, P を homomorphism として扱う場合も、actual map semantics と
applicability を domain rule として明示する。

Generic engine の変更は actual homomorphism rule が current rule language
で表現できないと実証された場合のみ。

---

# Current verified status

Full suite at Phase 12 completion:

```powershell
python -m pytest -v
```

```text
809 passed in 62.32s
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

docs/roadmap.md
=
future capability dependency
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
