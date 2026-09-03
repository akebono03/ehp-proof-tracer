# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の current architecture、semantics、design boundary を記録する。

historical な実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

---

# 1. 基本設計原則

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule
↓
existing generic inference engine
```

generic inference engine に数学固有の theorem knowledge を埋め込まない。

重要な区別:

```text
representation
!=
typing
!=
theorem knowledge
```

```text
structural equality
!=
mathematical equality
```

---

# 2. Layer separation

```text
literature-backed theorem / explicit facts
↓
domain-specific inference rules
↓
generic ProofStep / InferenceRule machinery
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

Phase 35–38 でも generic inference engine 自体は変更していない。

---

# 3. Expression layer

現在の主要 expression:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

constructor は theorem-aware normalization を行わない。

例えば:

```text
Suspension(Multiple(2,ι₁))
!= structural
Multiple(2,ι₂)
```

```text
IteratedSuspension(x,1)
!= structural
Suspension(x)
```

必要な数学的同値は `RelationType.EQUALITY` として proof-level に導出する。

---

# 4. Scalar-expression layer

Barratt–Hilton に必要な minimum scalar tree:

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

representable:

```text
p+k
q+h
(p+k)h
ph
(-1)^((p+k)h)
(-1)^(ph)
```

これは general-purpose CAS ではない。

自動では行わない:

```text
p+k=k+p
ph=hp
(p+k)h=ph+kh
(-1)^2=1
```

---

# 5. Parity / sign semantics

proof-level statements:

```text
OddScalarStatement
EvenScalarStatement
ScalarSignEvaluationStatement
```

rules:

```text
n even
↓
(-1)^n=1
```

```text
n odd
↓
(-1)^n=-1
```

重要:

```text
scalar expression structure
↛
automatic parity
```

Phase 35 concrete case でも:

```text
1·0 is even
```

を explicit premise として与える。

---

# 6. Symbolic Multiple

`Multiple.coefficient` は integer / symbolic scalar の両方を保持できる。

bridge:

```text
(-1)^n=1
↓
(-1)^n X=X
```

```text
(-1)^n=-1
↓
(-1)^n X=-X
```

Phase 35 では concrete Barratt–Hilton sign:

```text
(-1)^(1·0)
```

に同じ machinery を再利用する。

---

# 7. IteratedSuspension

symbolic exponent を保持できる:

```text
E^q a
E^(p+k)b
```

typing boundary:

```text
integer exponent
→ existing source / target shift
```

```text
symbolic exponent
→ source=None
→ target=None
```

Phase 35 では `E^1x=Ex` を constructor normalization にせず、明示的 equality bridge:

```text
iterated_suspension_one_bridge_inference_rule()
```

で接続する。

---

# 8. SmashProduct boundary

`SmashProduct(left,right)` は structural syntax。

一般には未実装:

```text
source / target typing
commutativity theorem
associativity theorem
normalization
general smash-product algebra
```

Toda Prop.3.1 の正しい premise がある場合にのみ Barratt–Hilton equality を導出する。

---

# 9. HomotopyGroupMembershipStatement

Phase 34 で symbolic applicability 用に導入した。

Phase 35 では actual multiple:

```text
2ι₁
```

も element として保持する必要が生じたため:

```text
element: Expression
```

へ拡張した。

representable:

```text
2ι₁ ∈ π₁(S¹)
```

重要:

```text
HomotopyGroupMembershipStatement
!=
automatic expression typing
```

membership fact から arbitrary nested expression の source / target を自動推論しない。

---

# 10. Barratt–Hilton concrete scalar sum policy

symbolic Toda Prop.3.1 では:

```text
p+k
q+h
```

を `ScalarSum` として保持する。

Phase 35 actual case では:

```text
p=1
k=0
```

のとき theorem applicability が:

```text
π₁(S¹)
```

と一致する必要がある。

そのため Barratt–Hilton rule 内だけで:

```text
concrete int + int
→ Python integer sum
```

を行う。

一方:

```text
symbolic + symbolic
→ ScalarSum
```

のまま。

これは general constant-folding / scalar normalization ではない。

---

# 11. Toda Prop.3.1 theorem rules

first:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

second:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

literature provenance:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

Phase 35 concrete instantiation:

```text
a=2ι₁
b=2ι₁
p=1
q=1
k=0
h=0
```

gives:

```text
2ι₁∧2ι₁
=
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
```

---

# 12. Actual Hopf fact layer

Phase 35 で `hopf_facts.py` に actual fact を追加した。

```text
H(η₂)=ι₃
```

representation:

```text
HopfInvariantStatement(
  expression=η₂,
  value=ι₃,
)
```

provenance:

```text
Toda Prop.5.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 5.1
```

既存 bridge により:

```text
HopfInvariantStatement
↓
Relation(
  MapApplication(EHP_H_MAP,η₂),
  ι₃,
  EQUALITY
)
```

へ接続する。

---

# 13. Suspension facts

Phase 35 actual calculation では identity suspension を explicit facts とする。

```text
Eι₁=ι₂
Eι₂=ι₃
```

general:

```text
Eι_n=ι_{n+1}
```

theorem solver は追加していない。

actual need に必要な `n=1,2` の facts のみ。

---

# 14. Suspension homomorphism / Multiple bridge

generic homomorphism layer には:

```text
f(kx)=k f(x)
```

がある。

一方 Phase 35 の formula は dedicated `Suspension(...)` syntax を使用する。

そこで:

```text
MapApplication(SUSPENSION_MAP,kx)
=
k MapApplication(SUSPENSION_MAP,x)
```

を:

```text
Suspension(kx)
=
k Suspension(x)
```

へ移す narrow bridge を追加した。

この bridge と explicit suspension facts により:

```text
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
```

を proof-level に導出できる。

---

# 15. Equality under Multiple

Phase 35 で generic equality transport の必要形を追加した。

```text
x=y
↓
kx=ky
```

これは symbolic algebra normalization ではなく、ordinary equality congruence の一方向 rule。

actual suspension facts:

```text
Eι₁=ι₂
```

から:

```text
2Eι₁=2ι₂
```

を作るために使用する。

---

# 16. Nested integer Multiple

Phase 35 actual `4ι₃` 計算のため:

```text
m(nx)=(mn)x
```

を concrete integer coefficient に限定して追加した。

代表:

```text
2(2ι₃)=4ι₃
```

symbolic coefficient multiplication は行わない。

---

# 17. Directed Toda (2.1)

Phase 35 actual calculation に必要な方向のみ追加:

```text
a∘(kb)
=
k(a∘b)
```

provenance:

```text
Toda (2.1)
```

重要:

```text
directed rule
!=
general composition bilinearity
```

未実装:

```text
(a₁+a₂)∘b
a∘(b₁+b₂)
general bidirectional distribution / collection
```

Phase 35 の具体例:

```text
2ι₃∘2ι₃
=
2((2ι₃)∘ι₃)
```

に使用する。

---

# 18. Explicit identity-map premise

`ιₙ` の notation だけから identity semantics を自動付与しない。

proof-level:

```text
IdentityMapStatement(
  element=ι₃
)
```

を explicit premise とする。

この premise から:

```text
x∘ι₃=x
```

を導出できる。

Phase 35 では:

```text
2ι₃∘ι₃=2ι₃
4ι₃∘ι₃=4ι₃
```

に利用する。

---

# 19. Actual H equality preservation

Phase 35-7 で canonical actual `H` に限定した congruence を追加した。

```text
x=y
↓
H(x)=H(y)
```

implementation は:

```text
EHP_H_MAP
```

に固定される。

重要:

```text
canonical actual H congruence
!=
universal arbitrary-map congruence
```

任意の `MapSymbol f` に自動一般化しない。

---

# 20. Concrete Phase 35 chain

まず:

```text
E(2ι₁)=2ι₂
```

よって:

```text
(E(2ι₁))∘η₂
=
(2ι₂)∘η₂
```

actual H congruence:

```text
H((E(2ι₁))∘η₂)
=
H((2ι₂)∘η₂)
```

Toda Prop.2.2 left:

```text
H((E(2ι₁))∘η₂)
=
E(2ι₁∧2ι₁)∘H(η₂)
```

Barratt–Hilton:

```text
2ι₁∧2ι₁
=
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
```

explicit parity:

```text
1·0 is even
↓
(-1)^(1·0)=1
```

therefore:

```text
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)
```

Suspension / functoriality:

```text
E(2ι₁∧2ι₁)
=
2ι₃∘2ι₃
```

Toda (2.1), identity, nested Multiple:

```text
2ι₃∘2ι₃
=
4ι₃
```

Toda Prop.5.1:

```text
H(η₂)=ι₃
```

したがって:

```text
E(2ι₁∧2ι₁)∘H(η₂)
=
4ι₃
```

最終的に:

```text
H((2ι₂)∘η₂)
=
4ι₃
```

---

# 21. Provenance design

Phase 35 representative proof graph では:

```text
Toda Prop.2.2 left
Toda Prop.3.1
Toda Prop.5.1
Toda (2.1)
```

を dependency として追跡する。

さらに:

```text
explicit parity
explicit suspension facts
explicit identity fact
homomorphism proof
generic equality transport
```

も `ProofStep.premises` に残る。

generic transitivity が作る final `Relation` にすべての literature metadata を複製しない。

proof graph を provenance の正本とする。

---

# 22. Phase 35 scope regression

固定した boundary:

```text
H equality preservation
→ canonical EHP_H_MAP only
```

```text
H equality preservation
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
↛
4H(η₂) automatically
```

```text
H((2ι₂)η₂)=4ι₃
+
Injective(H)
↛
(2ι₂)η₂=4η₂
```

理由:

injective reflection が要求するのは:

```text
Injective(H)
+
H(a)=H(b)
↓
a=b
```

であり:

```text
H(a)=4ι₃
```

だけではない。

---

# 23. Representative probe

Phase 35 probe:

```powershell
python -m probes.probe_phase35_capabilities
```

表示する主要 chain:

```text
[1] E(2ι₁)=2ι₂
[2] concrete Toda Prop.3.1
[3] explicit parity
[4] sign reduction
[5] E(2ι₁∧2ι₁)=4ι₃
[6] Toda (2.1)
[7] H(η₂)=ι₃
[8] Toda Prop.2.2 left
[9] Prop.2.2 RHS calculation
[10] actual H equality transport
[RESULT] H((2ι₂)∘η₂)=4ι₃
```

probe は production APIs / existing inference rules を再利用し、別の数学実装を持たない。

---

# 24. Test policy

各 mathematical layer で:

1. representation
2. structural distinction
3. applicability
4. invalid-case behavior
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. scope
10. full regression
11. executable probe

を確認する。

```text
pytest
=
correctness / regression
```

```text
probe
=
人間が目で追える mathematical capability
```

---

# 25. Phase 35 verified status

focused:

```text
tests/test_phase35_actual_h_calculation.py
53 passed
```

related:

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

full:

```text
1673 passed in 23.33s
```

probe:

```powershell
python -m probes.probe_phase35_capabilities
```

正常完走。

---

# 26. Phase 35 completion boundary

実装済み:

```text
actual H(η₂)=ι₃ fact
actual ι₁ / ι₂ Suspension facts
concrete Barratt-Hilton applicability
concrete scalar-sum handling inside theorem parameters
concrete parity / sign reduction
Suspension Multiple bridge
E^1-to-E proof bridge
equality transport through Multiple
nested integer Multiple
directed Toda (2.1)
explicit identity composition
canonical actual H equality preservation
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
E(2ι₁∧2ι₁)=4ι₃
H((2ι₂)η₂)=4ι₃
representative probe
final regression
```

未実装:

```text
H(4η₂)=4ι₃
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
general scalar CAS
automatic compound parity
general SmashProduct typing / algebra
general composition bilinearity
unrestricted Toda (2.1) rewrites
universal arbitrary-map congruence
automatic identity semantics from generator notation
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 27. 次の設計境界

次の数学的 branch:

```text
H(4η₂)
↓ H homomorphism / multiple calculation
4H(η₂)
↓ H(η₂)=ι₃
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

と:

```text
Injective(H)
+
H(a)=H(b)
↓
a=b
```

を再利用して:

```text
(2ι₂)η₂=4η₂
```

へ進む。

次 Phase でも actual need に必要な最小 capability だけを追加し、general algebra を先取りしない。


---

# 28. Actual H homomorphism materialization

Phase 36 では actual `EHP_H_MAP` に対する homomorphism property を proof graph に供給する必要が生じた。

既存 generic machinery:

```text
Homomorphism(f)
↓
f(kx)=k f(x)
```

はそのまま再利用する。

追加した narrow production API:

```text
ehp_h_homomorphism_proof_step()
```

返す statement:

```text
HomomorphismStatement(
  map=EHP_H_MAP,
)
```

これは actual `H` の既知 property の materialization であり、map-property inference の一般化ではない。

重要:

```text
Isomorphism(H)
↛
Homomorphism(H) automatically
```

```text
MapSymbol(f)
↛
Homomorphism(f) automatically
```

Phase 13 以来の automatic `Homomorphism(H)` / arbitrary-map homomorphism discovery を導入しない boundary を維持する。

---

# 29. Phase 36 actual H Multiple calculation

actual element:

```text
4η₂
```

は既存 `Multiple` で表現する。

actual homomorphism premise と generic rule:

```text
Homomorphism(H)
+
homomorphism_preserves_multiple_inference_rule(
  coefficient=4,
  expression=η₂,
)
```

から:

```text
H(4η₂)=4H(η₂)
```

を導出する。

専用 `H Multiple` expression / bridge は追加しない。`MapApplication(EHP_H_MAP, ...)` が actual `H` application の canonical representation である。

---

# 30. Toda Prop.5.1 substitution under Multiple

Phase 35 で実装済みの actual equality:

```text
H(η₂)=ι₃
```

に既存 generic equality congruence:

```text
x=y
↓
kx=ky
```

を `k=4` で適用し:

```text
4H(η₂)=4ι₃
```

を導出する。

新しい substitution engine / scalar normalization は追加しない。

---

# 31. Phase 36 transitivity closure

2 branch:

```text
H(4η₂)=4H(η₂)
```

```text
4H(η₂)=4ι₃
```

の middle expression は structural に同一:

```text
Multiple(
  coefficient=4,
  expression=MapApplication(
    map=EHP_H_MAP,
    expression=ETA_2,
  ),
)
```

したがって existing equality transitivity により:

```text
H(4η₂)=4ι₃
```

を得る。

専用 final theorem rule は追加しない。

---

# 32. Phase 36 provenance

代表 proof graph:

```text
actual Homomorphism(H)
↓
homomorphism preserves multiple
↓
H(4η₂)=4H(η₂)

Toda Prop.5.1
↓
H(η₂)=ι₃
↓
equality preserved under multiple
↓
4H(η₂)=4ι₃

↓ equality transitivity
H(4η₂)=4ι₃
```

Toda provenance の正本は Phase 35 の `ETA_2_HOPF_INVARIANT_FACT` に保持される。final transitivity Relation に literature metadata を複製しない。

---

# 33. Phase 36 scope regression

固定する boundary:

```text
actual Homomorphism(H)
→ canonical EHP_H_MAP only
```

```text
Isomorphism(H)
↛ Homomorphism(H)
```

```text
arbitrary MapSymbol
↛ automatic Homomorphism
```

```text
H((2ι₂)η₂)=4ι₃
+
H(4η₂)=4ι₃
↛
direct transitivity
```

```text
Injective(H)
+
H((2ι₂)η₂)=4ι₃
↛
(2ι₂)η₂=4η₂
```

Phase 37 でまず:

```text
H((2ι₂)η₂)=H(4η₂)
```

を構成する必要がある。

---

# 34. Phase 36 representative probe

```powershell
python -m probes.probe_phase36_capabilities
```

表示 chain:

```text
[1] Actual H homomorphism
    Homomorphism(H)

[2] H multiple calculation
    H(4η₂)=4H(η₂)

[3] Toda Prop.5.1
    H(η₂)=ι₃

[4] Equality under Multiple
    4H(η₂)=4ι₃

[RESULT]
    H(4η₂)=4ι₃
```

probe は production APIs / existing inference rules を再利用し、別の数学実装を持たない。

---

# 35. Phase 36 verified status

focused:

```text
tests/test_phase36_actual_h_multiple.py
14 passed
```

related:

```text
tests/test_homomorphism_rules.py
39 passed

tests/test_hopf_rules.py
31 passed

tests/test_relation_rules.py
50 passed

tests/test_map_property_rules.py
26 passed
```

full:

```text
1687 passed in 25.70s
```

probe:

```powershell
python -m probes.probe_phase36_capabilities
```

正常完走。

---

# 36. Phase 36 completion boundary

実装済み:

```text
actual Homomorphism(H) materialization
H(4η₂)=4H(η₂)
H(η₂)=ι₃
4H(η₂)=4ι₃
H(4η₂)=4ι₃
Phase 36 representative probe
scope / non-goal regression
final integrated regression
```

Phase 36 完了時点では未実装だったもの:

```text
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

---

# 37. Phase 37 final-step compatibility

Phase 35 final:

```text
H((2ι₂)η₂)=4ι₃
```

Phase 36 final:

```text
H(4η₂)=4ι₃
```

両者の右辺は structural に同じ:

```text
Multiple(4,IOTA_3)
```

一方 orientation は:

```text
A=C
B=C
```

なので direct transitivity は成立しない。

---

# 38. Phase 37 symmetry / transitivity closure

existing equality symmetry:

```text
H(4η₂)=4ι₃
↓
4ι₃=H(4η₂)
```

existing equality transitivity:

```text
H((2ι₂)η₂)=4ι₃
4ι₃=H(4η₂)
↓
H((2ι₂)η₂)=H(4η₂)
```

Phase 37 専用 theorem rule は追加しない。

```text
Phase 37 closure
=
existing equality symmetry
+
existing equality transitivity
```

---

# 39. Phase 37 provenance

proof graph の正本は `ProofStep.premises`。

```text
Phase 37 final
├─ Phase 35 actual final
└─ symmetry-derived step
   └─ Phase 36 actual final
```

Phase 35 / Phase 36 の内部 provenance はそのまま保持される。

Phase 37 final relation に literature metadata を複製しない。

---

# 40. Phase 37 scope boundary

実装済み:

```text
H((2ι₂)η₂)=H(4η₂)
```

Phase 37 では行わない:

```text
Injective(H) application
(2ι₂)η₂=4η₂
```

重要:

```text
H(a)=H(b)
↛
a=b
```

reflection には explicit:

```text
Injective(H)
```

premise が必要。これは Phase 38 の責務。

---

# 41. Phase 37 representative probe / verified status

probe:

```powershell
python -m probes.probe_phase37_capabilities
```

代表表示:

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

focused:

```text
tests/test_phase37_h_side_equality.py
11 passed
```

related:

```text
tests/test_phase35_actual_h_calculation.py
53 passed

tests/test_phase36_actual_h_multiple.py
14 passed

tests/test_relation_rules.py
50 passed

tests/test_map_property_rules.py
26 passed
```

full:

```text
1698 passed in 70.48s
```

production code:

```text
変更なし
```

---

# 42. Phase 37 completion boundary

実装済み:

```text
Phase 35 / Phase 36 final ProofStep compatibility
H(4η₂)=4ι₃ symmetry
4ι₃=H(4η₂)
H((2ι₂)η₂)=H(4η₂) transitivity closure
end-to-end integration / provenance
scope / non-goal regression
Phase 37 representative probe
final integrated regression
```

未実装:

```text
(2ι₂)η₂=4η₂
```

次の設計境界:

```text
Phase 38
Isomorphism(H)
↓
Injective(H)

Injective(H)
+
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

existing Phase 28/29 map-property machinery を第一候補として再利用する。

---

# 43. Phase 38 actual Isomorphism(H) compatibility

Phase 29 の actual map fact repository から canonical `EHP_H_MAP` に対する `Isomorphism(H)` を `ProofStep` として materialize できる。

existing Phase 28 rule:

```text
Isomorphism(f)
↓
Injective(f)
```

をそのまま適用し `Injective(H)` を得る。Phase 38 では production map-property rule を追加しない。

---

# 44. Phase 38 Phase 37 equality compatibility

Phase 37 final `H((2ι₂)η₂)=H(4η₂)` は structural に両辺とも `MapApplication(EHP_H_MAP, ...)` である。actual `Injective(H)` と両辺の map identity は同じ canonical `EHP_H_MAP` なので、existing injective-map reflection guard の要求を満たす。

---

# 45. Phase 38 equality reflection

existing Phase 28 rule:

```text
Injective(f)
+
f(a)=f(b)
↓
a=b
```

に actual premises:

```text
Injective(H)
H((2ι₂)η₂)=H(4η₂)
```

を与え、

```text
(2ι₂)η₂=4η₂
```

を導出する。Phase 38 専用 theorem rule は追加しない。

---

# 46. Phase 38 provenance

```text
(2ι₂)η₂=4η₂
├─ Injective(H)
│  └─ Isomorphism(H)
└─ H((2ι₂)η₂)=H(4η₂)
   ├─ Phase 35 final
   └─ symmetry
      └─ Phase 36 final
```

Phase 35 / Phase 36 内部の literature provenance は既存 `ProofStep.premises` graph に残る。final reflection relation に literature metadata を複製しない。

---

# 47. Phase 38 scope boundary

```text
Isomorphism(H) + H(a)=H(b)
↛ direct reflection

Injective(H) + H(a)=c
↛ reflection

Injective(H) + a=b
↛ reflection
```

actual H reflection は new H-specific theorem ではなく、existing generic map-property machinery の actual reuse である。

---

# 48. Phase 38 representative probe / verified status

```powershell
python -m probes.probe_phase38_capabilities
```

```text
[1] Actual Isomorphism(H)
[2] Existing isomorphism-to-injectivity
[3] Phase 37 H-side equality
[RESULT] (2ι₂)η₂=4η₂
```

provenance confirmation:

```text
Injective(H) includes Isomorphism(H) = True
final includes Injective(H) = True
final includes Phase 37 = True
Phase 37 includes Phase 35 = True
Phase 37 symmetry includes Phase 36 = True
```

focused:

```text
tests/test_phase38_injective_reflection.py
13 passed
```

full:

```text
1711 passed in 60.38s
```

production code:

```text
変更なし
```

---

# 49. Phase 38 completion boundary

実装済み:

```text
actual Isomorphism(H) compatibility
Isomorphism(H)→Injective(H) reuse
Phase 37 final H-side equality compatibility
Injective(H) reflection
(2ι₂)η₂=4η₂
end-to-end integration / provenance
scope / non-goal regression
Phase 38 representative probe
final integrated regression
```

Phase 38 で新規には実装していない:

```text
new H-specific reflection theorem
new map-property production rule
new generic inference-engine feature
direct Isomorphism(H) reflection
unrestricted arbitrary-map equality reflection
```

次の major design branch は `docs/roadmap.md` の Toda 4章 2-primary calculation infrastructure。



---

# 50. Phase 39 PrimaryComponent minimum representation

Toda 4章の 2-primary calculation branch の最初の minimum representation として、

```text
π_i(S^n;p)
```

を structural に保持する `PrimaryComponent` を導入した。

production object:

```text
PrimaryComponent
├── group_dimension: ScalarValue
├── sphere_dimension: ScalarValue
└── prime: int
```

重要なのは、既存の concrete group calculation layer を再利用して primary decomposition を計算するのではなく、まず group term 自体を lossless に表現することである。

```text
PrimaryComponent
!= AbelianGroup
!= Subgroup
```

`AbelianGroup` は具体的な group components / generators / orders を持つ calculation object、`Subgroup` は concrete ambient group の actual elements を持つ object である。`PrimaryComponent` はそれらを要求しない。

---

# 51. Phase 39 dimension compatibility

`PrimaryComponent` の dimension fields は既存の homotopy-group statement layer と同じ `ScalarValue` を使う。

```text
group_dimension: ScalarValue
sphere_dimension: ScalarValue
```

したがって次を同じ structural scalar layer で保持できる。

```text
π_8(S^5;2)
π_i(S^n;2)
π_(n+1)(S^n;2)
```

これは新しい dimension arithmetic system ではない。

```text
ScalarValue reuse
!= automatic dimension simplification
!= side-condition solver
```

---

# 52. Phase 39 structural equality

`PrimaryComponent` は dataclass structural equality により、次のいずれかが違えば別 object として扱う。

```text
group_dimension
sphere_dimension
prime
```

したがって:

```text
π_i(S^n;2) != π_i(S^n;3)
π_i(S^n;2) != π_j(S^n;2)
π_i(S^n;2) != π_i(S^m;2)
```

ここでいう equality / distinction は mathematical group isomorphism の判定ではなく structural identity の話である。

```text
structural equality
!= mathematical equality / isomorphism
```

---

# 53. Phase 39 scope boundary

`PrimaryComponent` は group term representation のみ。以下は encode しない。

```text
known AbelianGroup decomposition
components
orders
generators
elements
Subgroup conversion
finiteness
membership
theorem provenance
Toda π_i^n
```

特に:

```text
finite
!= known decomposition
```

```text
PrimaryComponent
!= HomotopyGroupMembershipStatement
```

```text
prime=2
↛ Toda π_i^n automatically
```

Toda (4.3) の `π_i^n` は critical degree で primary component と異なる定義を持つため、Phase 39 では先取りしない。

---

# 54. Phase 39 representative probe / verified status

probe:

```powershell
python -m probes.probe_phase39_capabilities
```

representative output:

```text
π_8(S^5;2)
π_8(S^5;3)
π_i(S^n;2)
```

さらに:

```text
same dimensions + different prime are distinct = True
```

および以下が未 encode であることを表示する。

```text
known AbelianGroup decomposition = False
concrete Subgroup elements = False
finiteness fact = False
membership element = False
Toda primary group = False
theorem provenance = False
```

focused:

```text
tests/test_phase39_primary_component.py
24 passed
```

full:

```text
1735 passed in 58.59s
```

Phase 39 で generic inference engine は変更していない。

---

# 55. Phase 39 completion boundary

実装済み:

```text
PrimaryComponent minimum representation
concrete primary-component construction
symbolic dimension construction
ScalarValue typing compatibility
structural equality / distinction
AbelianGroup / Subgroup separation
membership / finiteness / provenance non-goal regression
representative probe
final integrated regression
```

未実装:

```text
Serre finiteness theorem fact
PrimaryComponent membership
primary decomposition calculation
TodaPrimaryGroup π_i^n
critical-degree preimage subgroup
WhiteheadProduct
Toda Lemma 4.1
Toda Prop.4.2
```

次の設計境界は `TodaPrimaryGroup π_i^n` の minimum representation。

初期 Phase では critical-degree theorem semantics を constructor に埋め込まず、まず ordinary homotopy group / primary component と異なる structural group term として表現する。
