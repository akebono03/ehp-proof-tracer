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

Phase 35 でも generic inference engine 自体は変更していない。

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
