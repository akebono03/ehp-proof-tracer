# ehp_proof 開発記録

この文書は Phase 24 完了時点までの開発履歴を、現在の実装と矛盾しない
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
- duplicate rejection
- fixed-point execution
- bounded execution
- per-round tracing
- branch / merge

### 状態

完了

---

# Phase 6：EHP domain inference foundation

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
↓
equality closure / ZERO propagation
↓
FIXED_POINT
```

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
```

Phase 7 completion:

```text
706 passed in 60.22s
```

### 状態

完了

---

# Phase 8：Suspension reasoning

追加:

```text
Suspension(expression)
```

Rules:

```text
x=y → E(x)=E(y)
x=0 → E(x)=0
nα=0 → nE(α)=0
```

Phase 8 completion:

```text
721 passed in 22.16s
```

### 状態

完了

---

# Phase 9：Freudenthal / stable-range reasoning

```text
stable range
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary は epimorphism only。

Phase 9 completion:

```text
750 passed in 22.66s
```

### 状態

完了

---

# Phase 10：Composition reasoning

```text
α∘β=γ
```

を structured equality として扱い、
Suspension-composition functoriality と接続。

Phase 10 completion:

```text
763 passed in 22.32s
```

### 状態

完了

---

# Phase 11：Generalized Hopf-invariant reasoning

```text
H(α)=β
```

の `β` は `Expression`。

Boundary:

```text
H(x)=0
↛
x=0
```

Phase 11 completion:

```text
791 passed in 23.41s
```

### 状態

完了

---

# Phase 12：Additive expression / reasoning

追加:

```text
Sum(left,right)
```

Inverse:

```text
-α = Multiple(-1,α)
```

Phase 12 completion:

```text
809 passed in 62.32s
```

### 状態

完了

---

# Phase 13：Homomorphism reasoning

追加:

```text
MapSymbol
MapApplication
HomomorphismStatement
```

Phase 13 completion:

```text
856 passed in 62.31s
```

### 状態

完了

---

# Phase 14：Set / subgroup reasoning

追加:

```text
MembershipStatement
SubsetStatement
SubgroupEqualityStatement
ImageSubgroupReference
KernelSubgroupReference
```

Phase 14 completion:

```text
921 passed in 62.89s
```

### 状態

完了

---

# Phase 15：Coset / modulo reasoning

追加:

```text
Coset
ModuloStatement
CosetEqualityStatement
```

Phase 15 completion:

```text
956 passed in 64.09s
```

### 状態

完了

---

# Phase 16：Symbolic scalar constraints

追加:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

Representative:

```text
k odd
↓
k≡1 mod 2

ord(β)=2
+
k≡1 mod 2
↓
kβ=β
```

Phase 16 completion:

```text
988 passed in 61.87s
```

### 状態

完了

---

# Phase 17：Indeterminacy

追加:

```text
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

Examples:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Candidate enumeration は行わない。

Phase 17 completion:

```text
tests/test_indeterminacy_rules.py
36 passed
```

```text
full suite
1024 passed in 66.01s
```

### 状態

完了

---

# Phase 18：Toda bracket minimum representation

追加:

```text
TodaBracket
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Bridge:

```text
a∘b=0
b∘c=0
↓
ZERO
↓
{a,b,c} defined
```

Boundary:

```text
definedness
↛
membership
```

```text
membership
↛
exact value
```

Verified:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

### 状態

完了

---

# Phase 19：Toda bracket membership / first theorem bridge

追加:

```text
TodaBracketMembershipTheoremStatement
```

Bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

Actual notation was:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Phase 19 では `_1` を lossless に保持できず、unindexed projection を使用した。

Verified:

```text
tests/test_toda_rules.py
36 passed in 3.06s
```

```text
full suite
1064 passed in 61.64s
```

### 状態

完了

---

# Phase 20：Indexed unstable Toda notation

Phase 19 の representation gap を解消。

追加:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
IndexedTodaBracketData.is_consistent()
```

Boundary:

```text
IteratedSuspension
!=
ordinary Suspension normalization
```

```text
suspension exponent
!=
bracket index
```

```text
is_consistent()
!=
theorem applicability
```

Verified:

```text
tests/test_expression.py
64 passed in 1.46s
```

```text
full suite
1098 passed in 61.30s
```

### 状態

完了

---

# Phase 21：Typed homotopy elements / source-target context

追加:

```text
HomotopyElement.source
HomotopyElement.target
Suspension source / target shift
concrete IteratedSuspension source / target shift
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Boundary:

```text
typed
!=
untyped
```

```text
constructible
!=
type-compatible
```

```text
type compatibility
!=
ZERO
!=
Toda definedness
```

Verified:

```text
tests/test_expression.py
90 passed in 0.33s
```

```text
tests/test_toda_rules.py
44 passed in 0.73s
```

```text
full suite
1125 passed in 22.75s
```

### 状態

完了

---

# Phase 22：Structured Generator Representation

追加:

```text
GeneratorSymbol
  family
  index
  decoration
```

`HomotopyElement` に:

```text
generator: GeneratorSymbol | None
```

を追加。

Representative:

```text
{η₃,Eν′,ν₇}_1
```

を generator structure 込みで lossless に保持。

Critical:

```text
generator notation
↛
automatic source / target typing
```

Verified:

```text
tests/test_expression.py
118 passed in 0.44s
```

```text
full suite
1153 passed in 24.83s
```

### 状態

完了

---

# Phase 23：Indexed Toda theorem / validity connection

Phase 20〜22 で揃えた:

```text
indexed Toda structure
typed entries
structured generator identity
```

を actual theorem fact と Toda membership inference に接続。

主な完了項目:

```text
indexed theorem fact preservation
bracket-index structural matching
structured-generator theorem matching
definedness dependency
canonical indexed consistency guard
canonical indexed typing guard
indexed guarded theorem bridge
actual ε₃ literature representative
provenance / boundary regressions
indexed / unindexed separation
```

General canonical bridge:

```text
matching theorem
+
matching definedness
+
structural consistency
+
typing compatibility
↓
membership
```

Specific actual bridge:

```text
ε₃ theorem fact
+
exactly matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Important:

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

```text
ν₇ ↛ ν₆
```

No generator lookup.

No automatic typing.

No universal theorem prover.

Verified:

```text
tests/test_toda_rules.py
66 passed in 1.01s
```

```text
full suite
1175 passed in 22.96s
```

### 状態

完了

---

# Phase 24：Theorem fact / knowledge-table integration

Phase 24 は、Phase 23 まで Python 上で直接組み立てていた
literature-backed theorem fact を、最小 repository layer から
proof graph に供給できるようにした。

重要方針:

```text
knowledge table
!=
universal theorem prover
```

```text
stored fact
!=
automatically applicable theorem
```

```text
repository integration
!=
generic inference engine change
```

---

## Phase 24-1：theorem fact repository の最小表現

追加:

```text
TheoremFactRepository
```

Initial shape:

```text
entries
```

Existing:

```text
TodaBracketMembershipTheoremStatement
```

を repository に保持できる最小構造を追加。

まだ lookup / provenance materialization / ProofStep conversion は入れない。

Verified:

```text
tests/test_theorem_facts.py
2 passed
```

```text
full suite
1177 passed in 70.01s
```

### 状態

完了

---

## Phase 24-2：LiteratureReference を含む fact entry

追加:

```text
TheoremFactEntry
  statement
  reference
```

既存:

```text
LiteratureReference
```

をそのまま再利用。

Repository は `TheoremFactEntry` を保持する形へ変更。

まだ:

```text
entry.reference
→ statement.source
```

の変換は行わない。

Verified:

```text
tests/test_theorem_facts.py
3 passed
```

```text
full suite
1178 passed in 71.32s
```

### 状態

完了

---

## Phase 24-3：Toda membership theorem fact の登録

Actual literature representative:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

を production fact:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
```

として登録。

Repository:

```text
THEOREM_FACT_REPOSITORY
```

に格納。

Preserved:

```text
ε₃ generator family/index
η₃ generator family/index
ν′ decoration
ν₇ generator family/index
Eν′ = Suspension(ν′)
Toda index = 1
LiteratureReference
```

No canonical `IndexedTodaBracketData` conversion.

Verified:

```text
tests/test_theorem_facts.py
4 passed
```

```text
full suite
1179 passed in 68.66s
```

### 状態

完了

---

## Phase 24-4：repository lookup の最小 API

追加:

```text
TheoremFactRepository.lookup(statement)
```

Semantics:

```text
matching structural statement
→ TheoremFactEntry

unknown structural statement
→ None
```

Whole statement structural equality を再利用。

Wrong bracket index は match しない。

Fact key / string ID は導入しない。

Verified:

```text
tests/test_theorem_facts.py
6 passed
```

```text
full suite
1181 passed in 66.81s
```

### 状態

完了

---

## Phase 24-5：lookup result → theorem statement 変換

追加:

```text
TheoremFactEntry.materialize_statement()
```

Behavior:

```text
stored statement
+
entry.reference
↓
new theorem statement
  source = entry.reference
```

Stored statement は mutate しない。

Preserved:

```text
element
bracket
note
index
generator structure
```

Verified:

```text
tests/test_theorem_facts.py
8 passed
```

```text
full suite
1183 passed in 62.36s
```

### 状態

完了

---

## Phase 24-6：theorem statement → ProofStep.GIVEN 接続

追加:

```text
TheoremFactEntry.to_proof_step()
```

既存:

```text
toda_bracket_membership_theorem_proof_step()
```

を再利用。

Chain:

```text
entry
↓
materialize_statement()
↓
source-backed theorem statement
↓
existing helper
↓
ProofStep.GIVEN
```

Result:

```text
rule = GIVEN
premises = ()
inference_rule = None
```

No new proof-step semantics.

Verified:

```text
tests/test_theorem_facts.py
10 passed
```

```text
full suite
1185 passed in 63.89s
```

### 状態

完了

---

## Phase 24-7：ε₃ Toda fact の repository representative

Production code:

```text
変更なし
```

Representative end-to-end:

```text
THEOREM_FACT_REPOSITORY
↓
lookup
↓
TheoremFactEntry
↓
ProofStep.GIVEN
+
matching TodaBracketDefinedStatement
↓
existing Toda theorem bridge
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Preserved:

```text
index = 1
structured generator identity
ordinary Suspension(ν′)
LiteratureReference
direct provenance
```

No repository-specific inference rule.

Verified:

```text
tests/test_theorem_facts.py
11 passed
```

```text
full suite
1186 passed in 67.22s
```

### 状態

完了

---

## Phase 24-8：duplicate / unknown / boundary

`TheoremFactRepository` に duplicate validation を追加。

Current repository invariant:

```text
known structural statement → entry
unknown structural statement → None
empty repository lookup → None
duplicate structural statement → ValueError
```

Duplicate identity:

```text
same statement
```

なので:

```text
same statement
+
different LiteratureReference
```

も duplicate。

一方:

```text
different statement
+
same LiteratureReference
```

は許容。

No fact-key system.

Verified:

```text
tests/test_theorem_facts.py
13 passed
```

```text
full suite
1188 passed in 64.58s
```

### 状態

完了

---

## Phase 24-9：provenance / regression / scope

Production code:

```text
変更なし
```

複数の異なる repository theorem fact が存在する scenario で:

```text
ε₃ theorem step
+
unrelated theorem step
+
matching definedness
```

から derived ε₃ membership の direct premises が:

```text
theorem_step
defined_step
```

だけであることを固定。

Unrelated repository theorem step:

```text
↛ membership provenance
```

また matching membership は1件だけで、run は:

```text
FIXED_POINT
```

へ到達。

Verified:

```text
tests/test_theorem_facts.py
15 passed in 0.89s
```

```text
full suite
1190 passed in 61.30s
```

### 状態

完了

---

# Phase 24 completion boundary

Implemented:

```text
TheoremFactEntry
TheoremFactRepository
LiteratureReference-backed fact entry
actual ε₃ production theorem fact
THEOREM_FACT_REPOSITORY
structural statement lookup
unknown / empty lookup boundary
duplicate structural statement rejection
non-mutating statement materialization
LiteratureReference → theorem source materialization
repository fact → ProofStep.GIVEN
actual ε₃ repository representative
existing Toda bridge integration
repository provenance regression
unrelated fact exclusion
fixed-point / duplicate-conclusion boundary
```

Actual Phase 24 chain:

```text
literature-backed theorem data
↓
TheoremFactRepository
↓
lookup
↓
TheoremFactEntry
↓
materialize_statement()
↓
source-backed TodaBracketMembershipTheoremStatement
↓
to_proof_step()
↓
ProofStep.GIVEN
+
matching TodaBracketDefinedStatement
↓
existing Toda theorem inference rule
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
↓
FIXED_POINT
```

Important boundaries:

```text
repository fact
!=
membership
```

```text
lookup success
!=
theorem applicability
```

```text
stored statement
!=
materialized statement object
```

```text
structural lookup
!=
general theorem unification
```

```text
same statement with another source
=
duplicate in current repository
```

```text
fact key
=
not implemented
```

```text
repository
!=
external JSON / YAML loader
```

```text
repository
!=
universal theorem prover
```

```text
GeneratorSymbol.index
↛
automatic typing
```

No repository-specific inference rule.

No generic engine change.

Current verified status:

```text
tests/test_theorem_facts.py
15 passed in 0.89s
```

```text
tests/test_toda_rules.py
66 passed
```

```text
full suite
1190 passed in 61.30s
```

No failures.

---

# Current verified status

```powershell
python -m pytest tests/test_theorem_facts.py -q
```

```text
15 passed in 0.89s
```

```powershell
python -m pytest tests/test_toda_rules.py -q
```

```text
66 passed
```

```powershell
python -m pytest -q
```

```text
1190 passed in 61.30s
```

No failures.

---

# Next boundary

Natural next candidate:

```text
Phase 25
Generator typing / ambient-group facts
```

Potential direction:

```text
GeneratorSymbol
+
explicit literature / table fact
↓
generator source / target / ambient-group knowledge
↓
typed theorem applicability
```

Do not silently derive:

```text
GeneratorSymbol.index
→ source / target
```

without an explicit fact layer.

Later candidates:

```text
general theorem representation
  only when actual quantified theorem need appears
stable homotopy representation
stable Toda bracket
higher Toda bracket
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
chronological history

docs/roadmap.md
=
future capability dependency
```

今後も historical limitation と current limitation を混同しない。
