# ehp_proof 開発記録

current specification は `README.md` / `docs/design.md` を優先する。

---

# Phase 1–27 概要

Phase 1–17 で abelian-group calculation、generic inference、EHP、ORDER、Suspension、Freudenthal、Composition、Hopf invariant、additive / homomorphism / subgroup / modulo / symbolic scalar / indeterminacy reasoning を整備。

Phase 18–27 で unstable Toda bracket、indexed notation、typed homotopy elements、structured generators、theorem / generator facts、actual η₃ / ν′ / ν₇ typing、および actual ε₃ Toda chain を実装。

代表:

```text
η₃∘Eν′=0
ν′∘ν₆=0
Eν₆=ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
↓
ε₃∈{η₃,Eν′,ν₇}_1
```

### 状態

完了

---

# Phase 28：map-property equality reflection

```text
Isomorphism(f)
↓
Injective(f)

+

f(a)=f(b)
↓
a=b
```

### 状態

完了

---

# Phase 29：actual H facts / typing

production `H` identity、typing、isomorphism fact を既存 map-property machinery に接続。

```text
actual Isomorphism(H)
↓
Injective(H)
```

### 状態

完了

---

# Phase 30：Toda Prop.2.2 right

```text
H(a∘Eb)=H(a)∘Eb
```

を direct theorem rule として実装。

### 状態

完了

---

# Phase 31：SmashProduct minimum representation

```text
a∧b
c∧c
E(c∧c)
```

を structural に表現可能にした。

```text
representation
!=
typing
!=
Barratt–Hilton theorem knowledge
```

### 状態

完了

---

# Phase 32：Toda Prop.2.2 left

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

を direct theorem rule として実装。

### 状態

完了

---

# Phase 33：Barratt–Hilton prerequisite minimum representation

Toda Prop.3.1 を導入する前に、minimum scalar-expression tree、symbolic sign、symbolic IteratedSuspension exponent を追加。

```text
ScalarExpression
ScalarSum
ScalarProduct
ScalarPower
```

```text
n even → (-1)^n=1
n odd  → (-1)^n=-1
```

```text
(-1)^n=1 → (-1)^n X=X
(-1)^n=-1 → (-1)^n X=-X
```

Barratt–Hilton 2 formula を structural `Relation` として表現可能にした。

Phase 33 completion:

```text
73 passed Phase 33 focused suite
1585 passed full suite
```

### 状態

完了

---

# Phase 34：Toda Prop.3.1 Barratt–Hilton theorem rule

Phase 33 の structural formula を literature-backed theorem-derived `ProofStep` へ接続。

追加:

```text
HomotopyGroupMembershipStatement
barratt_hilton_first_inference_rule()
barratt_hilton_second_inference_rule()
```

provenance:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

代表:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓
Toda Prop.3.1
↓
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

Phase 33 sign machinery と generic equality transitivity を再利用して reduced equality まで接続。

Phase 34 completion:

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

```text
full suite
1620 passed in 23.32s
```

### 状態

完了

---

# Phase 35：actual H((2ι₂)η₂) calculation

目的:

Phase 30–34 の abstract theorem layer を concrete actual calculation:

```text
H((2ι₂)η₂)
```

へ接続し:

```text
H((2ι₂)η₂)=4ι₃
```

を end-to-end `ProofStep` として導出する。

---

## Phase 35-1：actual generator / identity typing check

確認:

```text
ι₁ : S¹→S¹
ι₂ : S²→S²
ι₃ : S³→S³
η₂ : S³→S²
```

を既存 `HomotopyElement` / `GeneratorSymbol` で表現可能。

```text
2ι₁
2ι₂
```

は既存 `Multiple` で表現可能。

current generator repository には:

```text
ι₁
ι₂
ι₃
η₂
```

の typing facts は未登録であることを regression 固定。

production code 変更なし。

結果:

```text
13 passed Phase 35 focused
1633 passed full suite
```

### 状態

完了

---

## Phase 35-2：H(η₂)=ι₃ fact

追加:

```text
hopf_facts.py
```

production fact:

```text
H(η₂)=ι₃
```

representation:

```text
HopfInvariantStatement
```

provenance:

```text
Toda Prop.5.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 5.1
```

既存 bridge により canonical actual `EHP_H_MAP` equality:

```text
H(η₂)=ι₃
```

へ接続。

結果:

```text
19 passed Phase 35 focused
1639 passed full suite
```

### 状態

完了

---

## Phase 35-3：Prop.2.2 left concrete application

production code 変更なし。

actual parameters:

```text
alpha=η₂
gamma=2ι₁
```

既存 Toda Prop.2.2 left rule から:

```text
H((E(2ι₁))∘η₂)
=
E((2ι₁)∧(2ι₁))∘H(η₂)
```

を theorem-derived `ProofStep` として生成。

Phase 35-2 の actual:

```text
H(η₂)=ι₃
```

と RHS が structural に接続することを確認。

boundary:

```text
E(2ι₁)
↛ 2ι₂ automatically

(2ι₁)∧(2ι₁)
↛ Barratt–Hilton automatically
```

結果:

```text
27 passed Phase 35 focused
1647 passed full suite
```

### 状態

完了

---

## Phase 35-4：2ι₁∧2ι₁ Barratt–Hilton concrete instantiation

actual `Multiple` を homotopy-group membership の element として保持するため:

```text
HomotopyGroupMembershipStatement.element
```

を `Expression` 対応へ拡張。

concrete theorem parameter:

```text
p=1
q=1
k=0
h=0
```

では applicability が actual:

```text
π₁(S¹)
```

と一致する必要があるため、Barratt–Hilton rule 内だけで concrete integer sum を評価。

symbolic case:

```text
p+k
q+h
```

は従来通り `ScalarSum` のまま。

concrete result:

```text
2ι₁∧2ι₁
=
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
```

sign はまだ reduction しない。

結果:

```text
33 passed Phase 35 focused
1653 passed full suite
```

### 状態

完了

---

## Phase 35-5：concrete parity / sign reduction

production code 変更なし。

explicit parity:

```text
1·0 is even
```

Phase 33 machinery:

```text
1·0 is even
↓
(-1)^(1·0)=1
```

signed Multiple reduction:

```text
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
=
E^1(2ι₁)∘E^1(2ι₁)
```

equality transitivity:

```text
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)
```

boundary:

```text
E(2ι₁)
↛ 2ι₂ yet

composition calculation
→ Phase 35-6
```

結果:

```text
39 passed Phase 35 focused
1659 passed full suite
```

### 状態

完了

---

## Phase 35-6：composition / multiple calculation

actual calculation に不足する narrow bridges を追加。

### Suspension multiple bridge

既存 generic homomorphism:

```text
E(kx)=kE(x)
```

を dedicated `Suspension` syntax へ接続。

### Actual suspension facts

追加:

```text
Eι₁=ι₂
Eι₂=ι₃
```

これにより:

```text
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
```

### E^1 bridge

constructor normalization は行わず:

```text
E^1x=Ex
```

を proof-level equality として追加。

### Equality under Multiple

```text
x=y
↓
kx=ky
```

を追加。

### Nested integer Multiple

concrete integer のみ:

```text
m(nx)=(mn)x
```

代表:

```text
2(2ι₃)=4ι₃
```

### Toda (2.1)

actual need の方向だけ:

```text
a∘(kb)=k(a∘b)
```

を staged direct rule として追加。

### Identity map

notation `ιₙ` から identity semantics を自動化せず:

```text
IdentityMapStatement
```

を explicit premise とする。

代表:

```text
2ι₃∘2ι₃
=
2((2ι₃)∘ι₃)
=
2(2ι₃)
=
4ι₃
```

結果:

```text
44 passed Phase 35 focused
1664 passed full suite
```

### 状態

完了

---

## Phase 35-7：H((2ι₂)η₂)=4ι₃ end-to-end

左辺 actualization のため narrow rule を追加:

```text
x=y
↓
H(x)=H(y)
```

ただし canonical:

```text
EHP_H_MAP
```

限定。

arbitrary map congruence には一般化しない。

chain:

```text
E(2ι₁)=2ι₂
↓
(E(2ι₁))∘η₂=(2ι₂)∘η₂
↓
H((E(2ι₁))∘η₂)=H((2ι₂)∘η₂)
```

Toda Prop.2.2 left:

```text
H((E(2ι₁))∘η₂)
=
E(2ι₁∧2ι₁)∘H(η₂)
```

Phase 35-4〜6:

```text
E(2ι₁∧2ι₁)=4ι₃
```

Phase 35-2:

```text
H(η₂)=ι₃
```

identity composition と equality transitivity を接続して:

```text
H((2ι₂)∘η₂)=4ι₃
```

を end-to-end `ProofStep` として導出。

結果:

```text
46 passed Phase 35 focused
1666 passed full suite
```

### 状態

完了

---

## Phase 35-8：scope / non-goal regression

production code 変更なし。

固定:

```text
actual H equality preservation
→ canonical EHP_H_MAP only
```

```text
actual H equality preservation
→ equality premise required
```

```text
Toda (2.1)
→ right integer multiple direction only
```

```text
identity composition
→ explicit IdentityMapStatement required
```

```text
H(4η₂)
↛ 4H(η₂) automatically
```

```text
H((2ι₂)η₂)=4ι₃
+
Injective(H)
↛
(2ι₂)η₂=4η₂
```

最後の boundary は injective reflection が:

```text
H(a)=H(b)
```

を要求するため。

結果:

```text
52 passed Phase 35 focused
1672 passed full suite
```

### 状態

完了

---

## Phase 35-9：representative probe / final regression

追加:

```text
probes/probe_phase35_capabilities.py
```

production rules を実際に組み合わせて representative proof を構築。

表示:

```text
[1] E(2ι₁)=2ι₂
[2] concrete Barratt–Hilton theorem
[3] explicit concrete parity
[4] sign reduction
[5] E(2ι₁∧2ι₁)=4ι₃
[6] Toda (2.1)
[7] H(η₂)=ι₃
[8] Toda Prop.2.2 left
[9] Prop.2.2 RHS calculation
[10] actual H equality transport
[RESULT] H((2ι₂)∘η₂)=4ι₃
```

provenance confirmation:

```text
Toda Prop.2.2 left
Toda Prop.3.1
Toda Prop.5.1
Toda (2.1)
```

boundary 表示:

```text
H(4η₂)=4ι₃
H((2ι₂)η₂)=H(4η₂)
injectivity reflection for this equality
(2ι₂)η₂=4η₂
general composition bilinearity
general symbolic scalar CAS
```

final regression:

```text
tests/test_phase35_actual_h_calculation.py
53 passed
```

```text
full suite
1673 passed in 23.33s
```

### 状態

完了

---

## Phase 35-10：Phase 35 完了整理

Phase 35 で完成:

```text
actual H(η₂)=ι₃ literature fact
actual identity suspension facts Eι₁=ι₂ / Eι₂=ι₃
concrete Barratt–Hilton membership / applicability
concrete integer theorem-parameter handling
explicit parity / sign reduction
Suspension Multiple bridge
E^1-to-E equality bridge
equality transport under Multiple
nested integer Multiple calculation
directed Toda (2.1)
explicit identity composition
canonical actual H equality preservation
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
E(2ι₁∧2ι₁)=4ι₃
H((2ι₂)η₂)=4ι₃
scope / non-goal regression
representative executable probe
final integrated regression
```

generic inference engine:

```text
変更なし
```

Phase 35 completion status:

```text
tests/test_phase35_actual_h_calculation.py
53 passed
```

```text
tests/test_hopf_rules.py
31 passed
```

```text
tests/test_homomorphism_rules.py
39 passed
```

```text
tests/test_relation_rules.py
50 passed
```

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

```text
full suite
1673 passed in 23.33s
```

probe:

```powershell
python -m probes.probe_phase35_capabilities
```

正常完走。

### 状態

完了

---

# Phase 35 completion boundary

実装済み:

```text
H(η₂)=ι₃
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)
E(2ι₁∧2ι₁)=4ι₃
H((2ι₂)η₂)=4ι₃
```

未実装:

```text
H(4η₂)=4ι₃
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

generalization として未実装:

```text
automatic compound parity inference
general symbolic scalar algebra
general SmashProduct typing / normalization
symbolic suspension source / target arithmetic
general composition bilinearity
unrestricted Toda (2.1)
universal arbitrary-map congruence
automatic identity semantics from ι notation
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 次の Phase

次は:

```text
H(4η₂)=4ι₃
```

を actual H homomorphism / multiple reasoning から導出する branch を推奨する。

想定:

```text
H(4η₂)
↓
4H(η₂)
↓ Toda Prop.5.1
4ι₃
```

その後:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
```

既存:

```text
Isomorphism(H)
↓
Injective(H)
```

と equality reflection を再利用して:

```text
(2ι₂)η₂=4η₂
```

へ進む。

次 Phase でも actual mathematical need に必要な最小変更だけを行う。


---

# Phase 36：actual H(4η₂) calculation

目的:

```text
H(4η₂)=4ι₃
```

を actual `EHP_H_MAP`、generic homomorphism machinery、Toda Prop.5.1 fact、equality under Multiple、transitivity から導出する。

---

## Phase 36-1：actual H homomorphism applicability check

確認:

```text
4η₂
```

は既存 `Multiple` で表現可能。

既存:

```text
homomorphism_preserves_multiple_inference_rule()
```

は explicit `HomomorphismStatement(map=EHP_H_MAP)` が premise にあれば:

```text
H(4η₂)=4H(η₂)
```

を生成可能。

一方 current actual map knowledge は:

```text
Isomorphism(H)
```

までで:

```text
Isomorphism(H)
↛ Homomorphism(H)
```

であることを確認。

production code 変更なし。

結果:

```text
4 passed Phase 36 focused
1677 passed full suite
```

### 状態

完了

---

## Phase 36-2：actual H homomorphism fact / bridge

`hopf_rules.py` に narrow actual-H materialization:

```text
ehp_h_homomorphism_proof_step()
```

を追加。

生成:

```text
GIVEN Homomorphism(EHP_H_MAP)
```

重要:

```text
Isomorphism(f)→Homomorphism(f)
```

という general rule は追加しない。

```text
arbitrary MapSymbol→Homomorphism
```

も追加しない。

結果:

```text
6 passed Phase 36 focused
1679 passed full suite
```

### 状態

完了

---

## Phase 36-3：H(4η₂)=4H(η₂)

production code 変更なし。

```text
Homomorphism(H)
+
homomorphism preserves multiple
↓
H(4η₂)=4H(η₂)
```

を `ProofStep` として生成。

結果:

```text
7 passed Phase 36 focused
1680 passed full suite
```

### 状態

完了

---

## Phase 36-4：H(η₂)=ι₃ substitution

Phase 35 の actual Toda Prop.5.1 fact:

```text
H(η₂)=ι₃
```

へ既存:

```text
x=y
↓
4x=4y
```

を適用。

結果:

```text
4H(η₂)=4ι₃
```

production code / new algebra rule 変更なし。

結果:

```text
8 passed Phase 36 focused
1681 passed full suite
```

### 状態

完了

---

## Phase 36-5：H(4η₂)=4ι₃ transitivity closure

```text
H(4η₂)=4H(η₂)
4H(η₂)=4ι₃
↓
equality transitivity
H(4η₂)=4ι₃
```

専用 theorem rule なし。

結果:

```text
9 passed Phase 36 focused
1682 passed full suite
```

### 状態

完了

---

## Phase 36-6：H(4η₂)=4ι₃ end-to-end integration

1本の representative test 内で:

```text
Homomorphism(H)
↓
H(4η₂)=4H(η₂)

Toda Prop.5.1
↓
H(η₂)=ι₃
↓
4H(η₂)=4ι₃

↓
H(4η₂)=4ι₃
```

を構築。

proof dependency も確認。

結果:

```text
10 passed Phase 36 focused
1683 passed full suite
```

### 状態

完了

---

## Phase 36-7：scope / non-goal regression

固定:

```text
actual Homomorphism(H)
→ EHP_H_MAP only
```

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↛ direct transitivity
```

```text
Injective(H)
+
H((2ι₂)η₂)=4ι₃
↛
(2ι₂)η₂=4η₂
```

Phase 37 / 38 を先取りしないことを regression 固定。

結果:

```text
13 passed Phase 36 focused
1686 passed full suite
```

### 状態

完了

---

## Phase 36-8：representative probe / final regression

追加:

```text
probes/probe_phase36_capabilities.py
```

表示:

```text
[1] Actual H homomorphism
[2] H multiple calculation
[3] Toda Prop.5.1
[4] Equality under Multiple
[RESULT] H(4η₂)=4ι₃
```

provenance:

```text
actual H homomorphism
homomorphism preserves multiple
Toda Prop.5.1
equality preserved under multiple
equality transitivity
```

boundary:

```text
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
automatic Isomorphism→Homomorphism
arbitrary-map automatic homomorphism inference
```

final regression:

```text
tests/test_phase36_actual_h_multiple.py
14 passed
```

```text
full suite
1687 passed in 25.70s
```

probe:

```powershell
python -m probes.probe_phase36_capabilities
```

正常完走。

### 状態

完了

---

## Phase 36-9：Phase 36 完了整理

Phase 36 で完成:

```text
actual H homomorphism applicability check
actual Homomorphism(H) materialization
H(4η₂)=4H(η₂)
Toda Prop.5.1 H(η₂)=ι₃ reuse
4H(η₂)=4ι₃
H(4η₂)=4ι₃ transitivity closure
end-to-end representative ProofStep
scope / non-goal regression
representative executable probe
final integrated regression
```

generic inference engine:

```text
変更なし
```

Phase 36 completion status:

```text
tests/test_phase36_actual_h_multiple.py
14 passed
```

```text
tests/test_homomorphism_rules.py
39 passed
```

```text
tests/test_hopf_rules.py
31 passed
```

```text
tests/test_relation_rules.py
50 passed
```

```text
tests/test_map_property_rules.py
26 passed
```

```text
full suite
1687 passed in 25.70s
```

probe:

```powershell
python -m probes.probe_phase36_capabilities
```

正常完走。

### 状態

完了

---

# Phase 36 completion boundary

実装済み:

```text
H(η₂)=ι₃
H((2ι₂)η₂)=4ι₃
Homomorphism(H) actual materialization
H(4η₂)=4H(η₂)
4H(η₂)=4ι₃
H(4η₂)=4ι₃
```

未実装:

```text
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

generalization として未実装:

```text
automatic Isomorphism→Homomorphism conversion
arbitrary-map automatic homomorphism inference
general symbolic scalar algebra
general composition bilinearity
universal arbitrary-map congruence
```

---

# 次の Phase

次は Phase 37:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↓ symmetry
4ι₃=H(4η₂)
↓ transitivity
H((2ι₂)η₂)=H(4η₂)
```

第一候補は existing equality symmetry / transitivity の再利用。

その後 Phase 38 で:

```text
Isomorphism(H)
↓
Injective(H)

Injective(H)
+
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

へ進む。
