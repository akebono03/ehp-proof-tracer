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

# Phase 37：H-side equality closure

目的:

```text
H((2ι₂)η₂)=H(4η₂)
```

を Phase 35 / Phase 36 の actual final `ProofStep` と existing equality symmetry / transitivity だけから導出する。

---

## Phase 37-1：Phase 35 / Phase 36 final ProofStep compatibility check

確認:

```text
Phase 35 final:
H((2ι₂)η₂)=4ι₃

Phase 36 final:
H(4η₂)=4ι₃
```

両右辺は structural に同一の:

```text
4ι₃
```

一方 orientation は `A=C`, `B=C` なので direct transitivity は match しないことを固定。

production code 変更なし。

結果:

```text
5 passed Phase 37 focused
1692 passed full suite
```

### 状態

完了

---

## Phase 37-2：H(4η₂)=4ι₃ symmetry

existing:

```text
equality_symmetry_inference_rule()
```

を Phase 36 actual final に適用。

```text
H(4η₂)=4ι₃
↓
4ι₃=H(4η₂)
```

元 Phase 36 final step を direct premise に保持。

production code 変更なし。

結果:

```text
6 passed Phase 37 focused
1693 passed full suite
```

### 状態

完了

---

## Phase 37-3：transitivity closure

```text
H((2ι₂)η₂)=4ι₃
4ι₃=H(4η₂)
↓ equality transitivity
H((2ι₂)η₂)=H(4η₂)
```

を actual Phase 35 / Phase 36 proof steps から導出。

Phase 37 の数学的主結果が完成。

production code 変更なし。

結果:

```text
7 passed Phase 37 focused
1694 passed full suite
```

### 状態

完了

---

## Phase 37-4：end-to-end integration / provenance

final proof graph:

```text
Phase 37 final
├─ Phase 35 actual final
└─ symmetry-derived step
   └─ Phase 36 actual final
```

Phase 35 / Phase 36 の内部 proof graph が切れずに保持されることを確認。

synthetic `GIVEN` へ置き換えない。

production code 変更なし。

結果:

```text
8 passed Phase 37 focused
1695 passed full suite
```

### 状態

完了

---

## Phase 37-5：scope / non-goal regression

固定:

```text
Phase 37 final
= H((2ι₂)η₂)=H(4η₂)
```

```text
Phase 37
↛ (2ι₂)η₂=4η₂
```

さらに H-side equality 単独では:

```text
injective_map_reflects_equality_inference_rule()
```

が match しないことを確認。explicit `Injective(H)` premise は Phase 38 に残す。

production code 変更なし。

結果:

```text
10 passed Phase 37 focused
1697 passed full suite
```

### 状態

完了

---

## Phase 37-6：representative probe / final regression

追加:

```text
probes/probe_phase37_capabilities.py
```

表示:

```text
[1] Phase 35
H((2ι₂)η₂)=4ι₃

[2] Phase 36
H(4η₂)=4ι₃

[3] Equality symmetry
4ι₃=H(4η₂)

[RESULT]
H((2ι₂)η₂)=H(4η₂)
```

provenance confirmation:

```text
final includes Phase 35 = True
symmetry includes Phase 36 = True
```

boundary:

```text
Injective(H) application to the Phase 37 equality
(2ι₂)η₂=4η₂
```

final regression:

```text
tests/test_phase37_h_side_equality.py
11 passed
```

```text
full suite
1698 passed in 70.48s
```

probe:

```powershell
python -m probes.probe_phase37_capabilities
```

正常完走。

### 状態

完了

---

## Phase 37-7：Phase 37 完了整理

Phase 37 で完成:

```text
Phase 35 / Phase 36 final ProofStep compatibility check
H(4η₂)=4ι₃ symmetry
4ι₃=H(4η₂)
H((2ι₂)η₂)=H(4η₂) transitivity closure
end-to-end integration / provenance
scope / non-goal regression
representative executable probe
final integrated regression
```

production code:

```text
変更なし
```

Phase 37 completion status:

```text
tests/test_phase37_h_side_equality.py
11 passed
```

```text
tests/test_phase35_actual_h_calculation.py
53 passed
```

```text
tests/test_phase36_actual_h_multiple.py
14 passed
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
1698 passed in 70.48s
```

probe:

```powershell
python -m probes.probe_phase37_capabilities
```

正常完走。

### 状態

完了

---

# Phase 37 completion boundary

実装済み:

```text
H(η₂)=ι₃
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
4ι₃=H(4η₂)
H((2ι₂)η₂)=H(4η₂)
```

未実装:

```text
(2ι₂)η₂=4η₂
```

generalization として新規には実装していない:

```text
new theorem rule for Phase 37
new production algebra for Phase 37
new generic inference-engine feature for Phase 37
```

---

# 次の Phase

次は Phase 38:

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

Phase 28 / 29 の existing map-property machinery を第一候補として再利用する。

---

# Phase 38：Injective(H) reflection

目的:

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

Phase 28 / 29 の existing map-property machinery を再利用する。

## Phase 38-1：actual Isomorphism(H) → Injective(H) compatibility check
actual `EHP_H_MAP_ISOMORPHISM_FACT` が canonical `EHP_H_MAP` を保持し existing rule に match。production code 変更なし。

```text
4 passed Phase 38 focused
1702 passed full suite
```

### 状態
完了

---

## Phase 38-2：Phase 37 final H-side equality compatibility check
Phase 37 final の両辺が `MapApplication` で canonical `EHP_H_MAP` を共有し、actual `Injective(H)` と structural に一致することを確認。production code 変更なし。

```text
7 passed Phase 38 focused
1705 passed full suite
```

### 状態
完了

---

## Phase 38-3：Injective(H) + H(a)=H(b) reflection
existing `injective_map_reflects_equality_inference_rule()` に actual premises を与え:

```text
(2ι₂)η₂=4η₂
```

を actual `ProofStep` として導出。production code 変更なし。

```text
8 passed Phase 38 focused
1706 passed full suite
```

### 状態
完了

---

## Phase 38-4：end-to-end integration / provenance

```text
(2ι₂)η₂=4η₂
├─ Injective(H)
│  └─ Isomorphism(H)
└─ H((2ι₂)η₂)=H(4η₂)
   ├─ Phase 35 final
   └─ symmetry
      └─ Phase 36 final
```

Phase 35 / 36 / 37 provenance が切れないことを確認。production code 変更なし。

```text
9 passed Phase 38 focused
1707 passed full suite
```

### 状態
完了

---

## Phase 38-5：scope / non-goal regression

```text
Isomorphism(H) + H(a)=H(b) ↛ direct reflection
Injective(H) + H(a)=c ↛ reflection
Injective(H) + a=b ↛ reflection
```

Phase 38 は new H-specific reflection theorem を追加しない。production code 変更なし。

```text
12 passed Phase 38 focused
1710 passed full suite
```

### 状態
完了

---

## Phase 38-6：representative probe / final regression
追加 `probes/probe_phase38_capabilities.py`。

```text
[1] Actual Isomorphism(H)
[2] Existing isomorphism-to-injectivity
[3] Phase 37 H-side equality
[RESULT] (2ι₂)η₂=4η₂
```

初回 full regression は `InferenceRule` factory の closure function object を含む structural equality 比較で1件失敗。production / probe は正しく、test を `inference_rule.name` 比較へ最小修正。

最終:

```text
tests/test_phase38_injective_reflection.py
13 passed

full suite
1711 passed in 60.38s
```

probe 正常完走。

### 状態
完了

---

## Phase 38-7：Phase 38 完了整理

Phase 38 で完成:

```text
actual Isomorphism(H) compatibility
actual Isomorphism(H)→Injective(H) reuse
Phase 37 final H-side equality compatibility
Injective(H) + H(a)=H(b) reflection
(2ι₂)η₂=4η₂
end-to-end integration / provenance
scope / non-goal regression
representative executable probe
final integrated regression
```

production code:

```text
変更なし
```

completion:

```text
tests/test_phase38_injective_reflection.py
13 passed

full suite
1711 passed in 60.38s
```

```powershell
python -m probes.probe_phase38_capabilities
```

正常完走。

### 状態
完了

---

# Phase 38 completion boundary

実装済み:

```text
H(η₂)=ι₃
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
H((2ι₂)η₂)=H(4η₂)
Isomorphism(H)
Injective(H)
(2ι₂)η₂=4η₂
```

Phase 38 で新規には実装していない:

```text
new H-specific reflection theorem
new map-property production rule
new generic inference-engine feature
direct Isomorphism(H) reflection
unrestricted arbitrary-map equality reflection
```

---

# 次の Phase

Phase 35–38 の actual equality branch は完了。次の major candidate は `docs/roadmap.md` の Toda 4章 2-primary calculation branch。最初の Phase 番号と実装対象は current code / tests を確認して actual mathematical need に必要な minimum representation から決定する。



---

# Phase 39：PrimaryComponent minimum representation

目的:

```text
π_i(S^n;p)
```

を Toda 4章 2-primary calculation branch の土台となる minimum structural object として表現する。

---

## Phase 39-1：current group / subgroup representation compatibility check

現行 `AbelianGroup` / `Subgroup` / homotopy-group dimension representation を確認。

結論:

```text
AbelianGroup
= concrete group decomposition / calculation object

Subgroup
= concrete ambient group の actual element subset

PrimaryComponent
= π_i(S^n;p) structural group term
```

したがって `PrimaryComponent` を `AbelianGroup` / `Subgroup` と同一 layer にしない方針を確定。

production code 変更なし。

### 状態
完了

---

## Phase 39-2：PrimaryComponent minimum data model

新規:

```text
homotopy_groups.py
```

追加:

```text
PrimaryComponent(
  group_dimension: ScalarValue,
  sphere_dimension: ScalarValue,
  prime: int,
)
```

representative:

```text
π_8(S^5;2)
π_i(S^n;2)
```

known decomposition / subgroup elements は持たせない。

結果:

```text
tests/test_phase39_primary_component.py
5 passed

full suite
1716 passed in 96.23s
```

### 状態
完了

---

## Phase 39-3：structural equality / distinction regression

固定:

```text
π_i(S^n;2) != π_i(S^n;3)
π_i(S^n;2) != π_j(S^n;2)
π_i(S^n;2) != π_i(S^m;2)
```

さらに:

```text
PrimaryComponent != AbelianGroup
PrimaryComponent != Subgroup
```

known decomposition fields を持たないことも regression 固定。

production code 変更なし。

結果:

```text
11 passed Phase 39 focused
1722 passed full suite
```

### 状態
完了

---

## Phase 39-4：basic construction / typing compatibility

`PrimaryComponent` の dimension fields が既存 `HomotopyGroupMembershipStatement` と同じ `ScalarValue` representation を共有することを確認。

```text
concrete int dimensions
symbolic ScalarSymbol dimensions
compound ScalarExpression dimensions
```

を保持可能。

prime は `int` のまま。

production code 変更なし。

結果:

```text
16 passed Phase 39 focused
1727 passed full suite
```

### 状態
完了

---

## Phase 39-5：scope / non-goal regression

固定:

```text
PrimaryComponent != membership statement
PrimaryComponent ↛ finiteness automatically
PrimaryComponent ↛ Subgroup automatically
prime=2 ↛ Toda π_i^n automatically
PrimaryComponent has no theorem provenance
```

production code 変更なし。

結果:

```text
21 passed Phase 39 focused
1732 passed full suite
```

### 状態
完了

---

## Phase 39-6：representative probe / final regression

追加:

```text
probes/probe_phase39_capabilities.py
```

表示:

```text
[1] π_8(S^5;2)
[2] π_8(S^5;3)
[3] π_i(S^n;2)
```

structural distinction:

```text
same dimensions + different prime are distinct = True
```

boundary:

```text
known AbelianGroup decomposition = False
concrete Subgroup elements = False
finiteness fact = False
membership element = False
Toda primary group = False
theorem provenance = False
```

final regression:

```text
tests/test_phase39_primary_component.py
24 passed

full suite
1735 passed in 58.59s
```

probe 正常完走。

### 状態
完了

---

## Phase 39-7：Phase 39 完了整理

Phase 39 で完成:

```text
current group / subgroup compatibility check
PrimaryComponent minimum data model
concrete / symbolic dimension representation
structural equality / distinction
ScalarValue typing compatibility
AbelianGroup / Subgroup separation
membership / finiteness / provenance scope regression
representative executable probe
final integrated regression
```

production capability:

```text
π_i(S^n;p) minimum structural representation
```

production code で追加した数学 object は `PrimaryComponent` のみ。

generic inference engine:

```text
変更なし
```

completion:

```text
tests/test_phase39_primary_component.py
24 passed

full suite
1735 passed in 58.59s
```

```powershell
python -m probes.probe_phase39_capabilities
```

正常完走。

### 状態
完了

---

# Phase 39 completion boundary

実装済み:

```text
π_i(S^n;p) structural representation
PrimaryComponent(group_dimension,sphere_dimension,prime)
concrete dimensions
symbolic / compound scalar dimensions
prime distinction
structural equality / distinction
representative probe
```

未実装:

```text
Serre finiteness
primary decomposition calculation
PrimaryComponent membership
TodaPrimaryGroup π_i^n
PreimageSubgroup under E
WhiteheadProduct
Toda Lemma 4.1
Toda Prop.4.2
```

重要:

```text
PrimaryComponent
!= AbelianGroup
!= Subgroup
!= membership
!= finiteness fact
!= Toda π_i^n
```

---

# 次の Phase

次は `TodaPrimaryGroup π_i^n` minimum representation。

Toda (4.3) の場合分け theorem semantics を一度に実装せず、まず:

```text
π_i^n
```

を ordinary homotopy group / `PrimaryComponent` と区別できる structural object として表現する。

その後の Phase で critical degree:

```text
i=2n-1
π_i^n=E^-1(π_{2n}(S^{n+1};2))
```

に必要な `PreimageSubgroup` へ進む。

---

# Phase 40：TodaPrimaryGroup minimum representation

目的:

```text
π_i^n
```

を Toda (4.3) の theorem semantics とは分離した minimum structural object として表現する。

---

## Phase 40-1：current PrimaryComponent / homotopy-group representation compatibility check

確認:

```text
PrimaryComponent.group_dimension: ScalarValue
PrimaryComponent.sphere_dimension: ScalarValue
```

および current homotopy-group membership representation:

```text
HomotopyGroupMembershipStatement.group_dimension: ScalarValue
HomotopyGroupMembershipStatement.sphere_dimension: ScalarValue
```

が同じ dimension layer を再利用していることを確認。

concrete / symbolic dimensions の compatibility を固定。

この時点では `TodaPrimaryGroup` がまだ存在しないことも regression で確認。

production code 変更なし。

結果:

```text
tests/test_phase40_toda_primary_group.py
5 passed

full suite
1740 passed in 27.62s
```

### 状態
完了

---

## Phase 40-2：TodaPrimaryGroup minimum data model

`homotopy_groups.py` に追加:

```text
TodaPrimaryGroup(
  group_dimension: ScalarValue,
  sphere_dimension: ScalarValue,
)
```

representative:

```text
π_8^5
π_i^n
```

`prime` や Toda (4.3) の case semantics は持たせない。

Phase 40-1 の「未実装」regression を削除し、concrete / symbolic construction と structural equality を追加。

結果:

```text
tests/test_phase40_toda_primary_group.py
7 passed

full suite
1742 passed in 25.23s
```

### 状態
完了

---

## Phase 40-3：structural distinction regression

固定:

```text
TodaPrimaryGroup != PrimaryComponent
TodaPrimaryGroup != HomotopyGroupMembershipStatement
TodaPrimaryGroup has no prime
TodaPrimaryGroup has no element
```

したがって representation-level で:

```text
π_i^n != π_i(S^n;2)
```

を明確に分離。

production code 変更なし。

結果:

```text
tests/test_phase40_toda_primary_group.py
11 passed

full suite
1746 passed in 23.46s
```

### 状態
完了

---

## Phase 40-4：basic construction / dimension typing compatibility

`TodaPrimaryGroup` 自身について:

```text
group_dimension: ScalarValue
sphere_dimension: ScalarValue
```

を regression 固定。

確認:

```text
concrete int dimensions
symbolic ScalarSymbol dimensions
compound ScalarSum dimensions
```

`PrimaryComponent` / `HomotopyGroupMembershipStatement` と同じ dimension representation を再利用する。

新しい dimension arithmetic / simplification は追加しない。

production code 変更なし。

結果:

```text
tests/test_phase40_toda_primary_group.py
16 passed

full suite
1751 passed in 24.91s
```

### 状態
完了

---

## Phase 40-5：scope / non-goal regression

固定:

```text
TodaPrimaryGroup has no evaluated definition
TodaPrimaryGroup has no preimage representation
TodaPrimaryGroup has no Subgroup conversion
TodaPrimaryGroup has no automatic PrimaryComponent conversion
TodaPrimaryGroup has no theorem provenance
```

critical-degree example:

```text
TodaPrimaryGroup(
  group_dimension=9,
  sphere_dimension=5,
)
```

は `9=2·5-1` だが、自動的に:

```text
E^-1(π_10(S^6;2))
```

へ評価しないことを固定。

production code 変更なし。

結果:

```text
tests/test_phase40_toda_primary_group.py
21 passed

full suite
1756 passed in 23.59s
```

### 状態
完了

---

## Phase 40-6：representative probe / final regression

追加:

```text
probes/probe_phase40_capabilities.py
```

表示:

```text
[1] Concrete Toda primary group
    π_8^5

[2] Symbolic Toda primary group
    π_i^n

[3] Critical-degree structural object
    π_9^5
```

structural distinction:

```text
TodaPrimaryGroup != PrimaryComponent = True
TodaPrimaryGroup has prime = False
TodaPrimaryGroup has membership element = False
```

completion boundary:

```text
evaluated Toda (4.3) definition = False
preimage subgroup = False
automatic PrimaryComponent conversion = False
theorem provenance = False
```

final regression:

```text
tests/test_phase40_toda_primary_group.py
24 passed

full suite
1759 passed in 25.21s
```

probe:

```powershell
python -m probes.probe_phase40_capabilities
```

正常完走。

### 状態
完了

---

## Phase 40-7：Phase 40 完了整理

Phase 40 で完成:

```text
current PrimaryComponent / homotopy-group compatibility check
TodaPrimaryGroup minimum data model
concrete / symbolic construction
structural equality / distinction
ScalarValue dimension typing compatibility
compound dimension representation
PrimaryComponent separation
membership separation
critical-degree structural representation
Toda (4.3) non-evaluation boundary
PreimageSubgroup non-goal regression
automatic PrimaryComponent conversion non-goal regression
theorem provenance non-goal regression
representative executable probe
final integrated regression
```

production capability:

```text
π_i^n minimum structural representation
```

production code で追加した数学 object は `TodaPrimaryGroup` のみ。

generic inference engine:

```text
変更なし
```

completion:

```text
tests/test_phase40_toda_primary_group.py
24 passed

full suite
1759 passed in 25.21s
```

```powershell
python -m probes.probe_phase40_capabilities
```

正常完走。

### 状態
完了

---

# Phase 40 completion boundary

実装済み:

```text
π_i^n structural representation
TodaPrimaryGroup(group_dimension,sphere_dimension)
concrete dimensions
symbolic / compound scalar dimensions
structural equality / distinction
critical-degree structural object
representative probe
```

未実装:

```text
Toda (4.3) evaluated definition
PreimageSubgroup under E
preimage membership semantics
π_i^n membership
Toda (4.3) theorem provenance
WhiteheadProduct
Toda Lemma 4.1
Toda Prop.4.2
```

重要:

```text
TodaPrimaryGroup
!= PrimaryComponent
!= HomotopyGroupMembershipStatement
!= evaluated Toda (4.3)
!= PreimageSubgroup
```

---

# 次の Phase

次は `PreimageSubgroup minimum representation`。

Toda (4.3) critical degree:

```text
i=2n-1
π_i^n=E^-1(π_{2n}(S^{n+1};2))
```

に必要な structural object を先に導入する。

初期 Phase では:

```text
PreimageSubgroup(map=E, subgroup=A)
```

のような representation のみに留め、

```text
x∈E^-1(A) ↔ E(x)∈A
```

という membership semantics や Toda (4.3) の case evaluation は後続 Phase に残す。

---

# Phase 41：PreimageSubgroup minimum representation

目的:

Toda (4.3) critical degree:

```text
i=2n-1
π_i^n=E^-1(π_{2n}(S^{n+1};2))
```

に必要な subgroup preimage を theorem semantics から分離した minimum structural object として表現する。

---

## Phase 41-1：current Subgroup / map representation compatibility check

確認:

```text
SubgroupTerm
=
Subgroup
| ImageSubgroupReference
| KernelSubgroupReference
```

```text
ImageSubgroupReference / KernelSubgroupReference
→ GroupMap
```

proof-expression layer の suspension map は:

```text
SUSPENSION_MAP
=
MapSymbol(name="E")
```

であり `GroupMap` とは別であることを固定。

critical-degree target:

```text
π_10(S^6;2)
```

は既存 `PrimaryComponent` で表現可能。

production code 変更なし。

結果:

```text
tests/test_phase41_preimage_subgroup.py
8 passed

full suite
1767 passed in 26.87s
```

### 状態
完了

---

## Phase 41-2：PreimageSubgroup minimum data model

`homotopy_groups.py` に追加:

```text
PreimageSubgroup(
  map: MapSymbol,
  subgroup: PrimaryComponent,
)
```

代表:

```text
E^-1(π_10(S^6;2))
```

`SubgroupTerm` にはまだ追加しない。

membership semantics / Toda (4.3) evaluation / theorem provenance は持たせない。

結果:

```text
tests/test_phase41_preimage_subgroup.py
14 passed

full suite
1773 passed in 24.37s
```

### 状態
完了

---

## Phase 41-3：structural distinction regression

production code 変更なし。

固定:

```text
PreimageSubgroup
!= Subgroup
!= ImageSubgroupReference
!= KernelSubgroupReference
!= PrimaryComponent
!= element-preimage representation
```

`PreimageSubgroup` は `element` / `preimage_element` / `value` を持たない。

結果:

```text
tests/test_phase41_preimage_subgroup.py
19 passed

tests/test_set_rules.py
107 passed

full suite
1778 passed in 25.94s
```

### 状態
完了

---

## Phase 41-4：map / subgroup typing compatibility

production code 変更なし。

型を固定:

```text
PreimageSubgroup.map
→ MapSymbol

PreimageSubgroup.subgroup
→ PrimaryComponent
```

symbolic critical-degree target:

```text
π_2n(S^(n+1);2)
```

を既存 scalar tree:

```text
2n
→ ScalarProduct(2,n)

n+1
→ ScalarSum(n,1)
```

で lossless に保持できることを確認。

したがって:

```text
E^-1(π_2n(S^(n+1);2))
```

を structural に表現可能。

`PreimageSubgroup` 自体は suspension 専用 class にせず arbitrary `MapSymbol` を保持可能とする。

結果:

```text
tests/test_phase41_preimage_subgroup.py
25 passed

full suite
1784 passed in 26.75s
```

### 状態
完了

---

## Phase 41-5：scope / non-goal regression

production code 変更なし。

固定:

```text
PreimageSubgroup != MembershipStatement
PreimageSubgroup has no membership element
PreimageSubgroup has no membership theorem semantics
PreimageSubgroup has no membership equivalence
PreimageSubgroup has no Toda evaluated definition
PreimageSubgroup ↛ TodaPrimaryGroup conversion
TodaPrimaryGroup ↛ PreimageSubgroup conversion
PreimageSubgroup has no theorem provenance
```

途中、`TodaPrimaryGroup` の test import 漏れにより `NameError` が1件発生したが、test import のみ修正。production code / test semantics は変更していない。

最終:

```text
tests/test_phase41_preimage_subgroup.py
32 passed

tests/test_set_rules.py
107 passed

full suite
1791 passed in 24.30s
```

### 状態
完了

---

## Phase 41-6：representative probe / final regression

追加:

```text
probes/probe_phase41_capabilities.py
```

production objects を実際に組み合わせて表示:

```text
[1] Concrete suspension preimage
    E^-1(π_10(S^6;2))

[2] Symbolic critical-degree target
    E^-1(π_2n(S^n+1;2))
```

structural distinction:

```text
PreimageSubgroup != Subgroup = True
PreimageSubgroup != ImageSubgroupReference = True
PreimageSubgroup != KernelSubgroupReference = True
PreimageSubgroup != PrimaryComponent = True
```

completion boundary:

```text
membership element = False
membership equivalence = False
theorem provenance = False
automatic preimage conversion = False
evaluated Toda (4.3) definition = False
```

final regression:

```text
tests/test_phase41_preimage_subgroup.py
36 passed

tests/test_phase40_toda_primary_group.py
24 passed

tests/test_set_rules.py
107 passed

full suite
1795 passed in 23.68s
```

probe:

```powershell
python -m probes.probe_phase41_capabilities
```

正常完走。

### 状態
完了

---

## Phase 41-7：Phase 41 完了整理

Phase 41 で完成:

```text
current Subgroup / map representation compatibility check
PreimageSubgroup minimum data model
map: MapSymbol
subgroup: PrimaryComponent
concrete preimage representation
symbolic critical-degree target representation
compound ScalarValue compatibility
structural equality / distinction
Subgroup / Image / Kernel reference separation
element-preimage separation
scope / non-goal regression
representative executable probe
final integrated regression
```

production capability:

```text
E^-1(A) minimum structural representation
```

代表:

```text
E^-1(π_10(S^6;2))
E^-1(π_2n(S^(n+1);2))
```

production code で追加した数学 object は `PreimageSubgroup` のみ。

generic inference engine:

```text
変更なし
```

completion:

```text
tests/test_phase41_preimage_subgroup.py
36 passed

tests/test_phase40_toda_primary_group.py
24 passed

tests/test_set_rules.py
107 passed

full suite
1795 passed in 23.68s
```

```powershell
python -m probes.probe_phase41_capabilities
```

正常完走。

### 状態
完了

---

# Phase 41 completion boundary

実装済み:

```text
PreimageSubgroup(map,subgroup) structural representation
MapSymbol map identity
PrimaryComponent target
concrete dimensions
symbolic / compound scalar dimensions
structural equality / distinction
representative probe
```

未実装:

```text
PreimageSubgroup in SubgroupTerm
preimage membership semantics
x∈E^-1(A) ↔ E(x)∈A
Toda (4.3) evaluated definition
TodaPrimaryGroup automatic preimage conversion
π_i^n membership
Toda (4.3) theorem provenance
WhiteheadProduct
Toda Lemma 4.1
Toda Prop.4.2
```

重要:

```text
PreimageSubgroup
!= Subgroup
!= ImageSubgroupReference
!= KernelSubgroupReference
!= PrimaryComponent
!= MembershipStatement
!= evaluated Toda (4.3)
```

---

# 次の Phase

次は `WhiteheadProduct minimum representation`。

Toda Lemma 4.1 に必要な:

```text
[ι_{n-1},ι_{n-1}]
```

を `Composition` / `SmashProduct` と区別できる minimum structural object として先に導入する。

初期 Phase では:

```text
WhiteheadProduct(
  left=a,
  right=b,
)
```

のような representation のみに留め、

```text
Whitehead-product algebra
zero / nonzero theorem rules
Toda Lemma 4.1 case evaluation
```

は後続 Phase に残す。

---

# Phase 42：WhiteheadProduct minimum representation

目的:

Toda Lemma 4.1 に必要な:

```text
[ι_{n-1},ι_{n-1}]
```

を `Composition` / `SmashProduct` と区別できる minimum structural `Expression` として表現する。

---

## Phase 42-1：current Composition / SmashProduct / expression compatibility check

確認:

```text
Composition
├── Expression
├── left: Expression
├── right: Expression
└── current typing semantics あり
```

```text
SmashProduct
├── Expression
├── left: Expression
├── right: Expression
└── typing semantics なし
```

さらに:

```text
Composition != SmashProduct
```

を確認し、`WhiteheadProduct` がまだ production に存在しないことを regression 固定。

production code 変更なし。

結果:

```text
tests/test_phase42_whitehead_product.py
10 passed

tests/test_expression.py
145 passed

tests/test_phase41_preimage_subgroup.py
36 passed

full suite
1805 passed in 24.49s
```

### 状態
完了

---

## Phase 42-2：WhiteheadProduct minimum data model

`expression.py` に追加:

```text
@dataclass(frozen=True)
class WhiteheadProduct(Expression):
  left: Expression
  right: Expression
```

`SmashProduct` と同様、binary structural syntax のみに限定。

未追加:

```text
source
target
is_type_compatible()
zero / nonzero theorem semantics
bilinearity
antisymmetry
Toda Lemma 4.1
```

結果:

```text
tests/test_phase42_whitehead_product.py
13 passed

tests/test_expression.py
145 passed

tests/test_phase41_preimage_subgroup.py
36 passed

full suite
1808 passed in 24.03s
```

### 状態
完了

---

## Phase 42-3：structural distinction regression

production code 変更なし。

同一 operands に対しても:

```text
WhiteheadProduct(a,b)
!= Composition(a,b)

WhiteheadProduct(a,b)
!= SmashProduct(a,b)
```

を固定。

class identity も:

```text
WhiteheadProduct is not Composition
WhiteheadProduct is not SmashProduct
```

を確認。

結果:

```text
tests/test_phase42_whitehead_product.py
17 passed

tests/test_expression.py
145 passed

full suite
1812 passed in 24.87s
```

### 状態
完了

---

## Phase 42-4：basic construction / expression typing compatibility

production code 変更なし。

`left/right: Expression` により次を lossless に保持できることを確認。

```text
HomotopyElement
Multiple
Composition
SmashProduct
nested WhiteheadProduct
```

一方:

```text
source
target
is_type_compatible()
```

は持たないことを regression 固定。

重要:

```text
construction
!= mathematical typing
```

結果:

```text
tests/test_phase42_whitehead_product.py
26 passed

tests/test_expression.py
145 passed

full suite
1821 passed in 23.96s
```

### 状態
完了

---

## Phase 42-5：scope / non-goal regression

production code 変更なし。

固定:

```text
WhiteheadProduct
!= zero theorem
!= nonzero theorem
!= bilinearity
!= antisymmetry
!= Toda Lemma 4.1 evaluation
!= theorem provenance
```

したがって:

```text
[ι,ι] representation
↛ [ι,ι]=0

[ι,ι] representation
↛ [ι,ι]!=0
```

結果:

```text
tests/test_phase42_whitehead_product.py
32 passed

tests/test_expression.py
145 passed

full suite
1827 passed in 24.39s
```

### 状態
完了

---

## Phase 42-6：representative probe / final regression

追加:

```text
probes/probe_phase42_capabilities.py
```

representative:

```text
[ι₄,ι₄]
```

`ι₄` は:

```text
GeneratorSymbol(
  family="ι",
  index=4,
)
```

で保持。

symbolic generator index `ι_{n-1}` は Phase 42 では追加しない。

probe 表示:

```text
WhiteheadProduct != Composition = True
WhiteheadProduct != SmashProduct = True
WhiteheadProduct is not Composition = True
WhiteheadProduct is not SmashProduct = True
source typing = False
target typing = False
type compatibility = False
zero theorem semantics = False
nonzero theorem semantics = False
bilinearity = False
antisymmetry = False
Toda Lemma 4.1 evaluation = False
theorem provenance = False
```

final regression:

```text
tests/test_phase42_whitehead_product.py
36 passed

tests/test_expression.py
145 passed

tests/test_phase41_preimage_subgroup.py
36 passed

full suite
1831 passed in 23.58s
```

probe:

```powershell
python -m probes.probe_phase42_capabilities
```

正常完走。

### 状態
完了

---

## Phase 42-7：Phase 42 完了整理

Phase 42 で完成:

```text
current Composition / SmashProduct / Expression compatibility check
WhiteheadProduct minimum data model
WhiteheadProduct is Expression
left: Expression
right: Expression
structural equality
Composition / SmashProduct structural distinction
existing Expression operand compatibility
nested WhiteheadProduct representation
typing non-goal regression
zero / nonzero theorem non-goal regression
bilinearity / antisymmetry non-goal regression
Toda Lemma 4.1 non-evaluation regression
representative [ι₄,ι₄]
representative executable probe
final integrated regression
```

production capability:

```text
[a,b] minimum structural representation
```

production code で追加した数学 object は:

```text
WhiteheadProduct(Expression)
```

のみ。

generic inference engine:

```text
変更なし
```

completion:

```text
tests/test_phase42_whitehead_product.py
36 passed

tests/test_expression.py
145 passed

tests/test_phase41_preimage_subgroup.py
36 passed

full suite
1831 passed in 23.58s
```

```powershell
python -m probes.probe_phase42_capabilities
```

正常完走。

### 状態
完了

---

# Phase 42 completion boundary

実装済み:

```text
[a,b] structural representation
WhiteheadProduct(left,right)
structural equality / distinction
existing Expression operands
nested structure
representative [ι₄,ι₄]
representative probe
```

未実装:

```text
Whitehead-product source / target typing
Whitehead-product dimension formula
Whitehead-product operand compatibility theorem
symbolic generator index ι_{n-1}
Whitehead-product zero theorem fact
Whitehead-product nonzero theorem fact
bilinearity
antisymmetry
Toda Lemma 4.1 case evaluation
Toda Lemma 4.1 theorem provenance
Toda Prop.4.2
```

重要:

```text
WhiteheadProduct
= structural syntax

WhiteheadProduct
!= theorem semantics
```

---

# 次の Phase

次は Toda Lemma 4.1 branch。

最初に:

```text
[ι_{n-1},ι_{n-1}]=0
```

と:

```text
[ι_{n-1},ι_{n-1}]!=0
```

を theorem premise として保持できる minimum statement / existing relation compatibility を確認する。

その後:

```text
n odd

n even
+
Whitehead product nonzero

n even
+
Whitehead product zero
```

の case semantics を staged に追加する。

一般 Whitehead-product algebra は先取りしない。

