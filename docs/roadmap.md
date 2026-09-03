# EHP Proof Tracer Roadmap

## 1. 文書の役割

```text
README.md
=
current capabilities / status

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

---

# 2. Phase 34 完了時点

Completed chain:

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left
Phase 33  Barratt–Hilton prerequisites
Phase 34  Toda Prop.3.1 Barratt–Hilton theorem rules
```

Current full regression:

```text
1620 passed in 23.32s
```

Focused Phase 34:

```text
35 passed
```

---

# 3. Phase 34 completed capabilities

```text
HomotopyGroupMembershipStatement
Toda Prop.3.1 first theorem rule
Toda Prop.3.1 second theorem rule
strict symbolic applicability
invalid-case rejection
unrelated-premise tolerance
structured literature provenance
Phase 33 sign-evaluation connection
generic equality-transitivity closure
scope / non-goal regression
Phase 34 representative probe
Phase 34 final integrated regression
```

theorem premises:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

first conclusion:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

second conclusion:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

provenance:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

---

# 4. Phase 34 completed inference chain

代表:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)

↓ Toda Prop.3.1

a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)

+

((p+k)h) is even

↓
(-1)^((p+k)h)=1

↓
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b

↓ equality transitivity

a∧b
=
E^q a∘E^(p+k)b
```

重要:

```text
Barratt–Hilton
!=
general SmashProduct normalization
```

```text
symbolic homotopy-group membership
!=
symbolic source / target solver
```

---

# 5. Phase 35+：actual H((2ι₂)η₂) calculation

NEXT。

Phase 34 までで:

```text
Toda Prop.2.2 left
+
SmashProduct
+
Barratt–Hilton theorem rules
+
sign machinery
+
H injectivity
```

が準備済み。

次は abstract symbolic formula ではなく、具体的に:

```text
H((2ι₂)η₂)
```

を計算する。

想定 target chain:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / concrete Barratt–Hilton
4ι₃
```

このために必要になる可能性がある concrete pieces:

```text
typing of ι₁, ι₂, ι₃, η₂
H(η₂)=ι₃
2ι₁ ∈ appropriate homotopy group
concrete Barratt–Hilton parameter instantiation
concrete parity/sign evaluation
composition of multiples / identity maps
```

ただし Phase 35+ では actual calculation に必要な順に1つずつ導入する。

一般的な symbolic arithmetic や Toda (2.1) 全体を先取りしない。

---

# 6. parallel calculation of H(4η₂)

もう一方:

```text
H(4η₂)
```

について:

```text
H(4η₂)
↓ H homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

が必要。

既存 homomorphism machinery を再利用できるかをまず確認する。

不足がある場合のみ、actual H map に必要な最小 fact / bridge を追加する。

---

# 7. equality target

両側を計算後:

```text
H((2ι₂)η₂)=4ι₃
```

```text
H(4η₂)=4ι₃
```

から:

```text
H((2ι₂)η₂)=H(4η₂)
```

を構成する。

その後 Phase 28 / 29 を再利用:

```text
Isomorphism(H)
↓
Injective(H)
```

```text
Injective(H)
+
H(a)=H(b)
↓
a=b
```

最終 target:

```text
(2ι₂)η₂=4η₂
```

---

# 8. Phase 35+ の候補分割

実装時は actual code を確認して最小単位に切る。

候補:

```text
Phase 35-1
actual generator / identity typing check
```

```text
Phase 35-2
H(η₂)=ι₃ fact representation
```

```text
Phase 35-3
concrete Prop.2.2-left application setup
```

```text
Phase 35-4
2ι₁∧2ι₁ Barratt–Hilton concrete instantiation
```

```text
Phase 35-5
concrete sign / parity reduction
```

```text
Phase 35-6
composition / multiple calculation to 4ι₃
```

```text
Phase 35-7
H((2ι₂)η₂)=4ι₃ representative chain
```

その後必要に応じて:

```text
H(4η₂)=4ι₃
H-side equality
Injective(H) reflection
```

へ進む。

この番号は actual code inspection 後に確定する。

---

# 9. Toda (2.1) future candidate

既知として利用候補:

```text
a∘(b₁±b₂)=a∘b₁±a∘b₂
```

```text
(a₁±a₂)∘Eb=a₁∘Eb±a₂∘Eb
```

```text
k(a∘b)=a∘(kb)
```

```text
k(a∘Eb)=(ka)∘Eb
```

ただし unrestricted bidirectional rewrite は導入しない。

Phase 35+ の actual `4ι₃` calculation で必要になった式だけ staged / directed rule として追加する。

---

# 10. Toda (5.1) future candidate

既知として利用候補:

```text
π_i(S¹)=0  (i>1)
π_i(S^n)=0  (i<n)
π_n(S^n)=Z{ι_n}
```

actual proof need が現れた時点で foundational fact layer として導入する。

---

# 11. Current deferred boundaries

未実装:

```text
automatic compound parity inference
general symbolic scalar simplification
general SmashProduct typing / algebra / normalization
symbolic suspension typing arithmetic
Toda (2.1) general rule set
actual H((2ι₂)η₂) evaluation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 12. Capability matrix

| capability | status | phase |
|---|---|---|
| map injectivity / equality reflection | IMPLEMENTED | 28 |
| actual H facts / typing | IMPLEMENTED | 29 |
| Toda Prop.2.2 right | IMPLEMENTED | 30 |
| SmashProduct | IMPLEMENTED | 31 |
| Toda Prop.2.2 left | IMPLEMENTED | 32 |
| ScalarExpression tree | IMPLEMENTED | 33 |
| parity → symbolic sign evaluation | IMPLEMENTED | 33 |
| symbolic sign → Multiple bridge | IMPLEMENTED | 33 |
| symbolic IteratedSuspension exponent | IMPLEMENTED | 33 |
| Barratt–Hilton structural formulas | IMPLEMENTED | 33 |
| symbolic homotopy-group membership | IMPLEMENTED | 34 |
| Toda Prop.3.1 first theorem rule | IMPLEMENTED | 34 |
| Toda Prop.3.1 second theorem rule | IMPLEMENTED | 34 |
| Toda Prop.3.1 literature provenance | IMPLEMENTED | 34 |
| Barratt–Hilton sign connection | IMPLEMENTED | 34 |
| Barratt–Hilton reduced equality closure | IMPLEMENTED | 34 |
| actual `H((2ι₂)η₂)` calculation | NEXT | 35+ |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | after actual H calculations |
| `(2ι₂)η₂=4η₂` | PLANNED | reuse equality reflection |
| Toda (2.1) | PLANNED | concrete need |
| Toda (5.1) | PLANNED | concrete need |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 13. Long-term dependency

```text
Phase 29
actual H equality-reflection foundation
↓
Phase 30
Toda Prop.2.2 right COMPLETE
↓
Phase 31
SmashProduct COMPLETE
↓
Phase 32
Toda Prop.2.2 left COMPLETE
↓
Phase 33
Barratt–Hilton prerequisites COMPLETE
↓
Phase 34
Toda Prop.3.1 Barratt–Hilton COMPLETE
↓
Phase 35+
actual H((2ι₂)η₂)
↓
H((2ι₂)η₂)=4ι₃
↓
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing Injective(H)
↓
(2ι₂)η₂=4η₂
```

---

# 14. Testing principle

各 layer で:

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

---

# 15. Phase 34 verified status

focused:

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

related:

```text
tests/test_phase33_barratt_hilton.py
73 passed
```

```text
tests/test_scalar_rules.py
18 passed
```

```text
tests/test_relation_rules.py
50 passed
```

full:

```text
1620 passed in 23.32s
```

probe:

```powershell
python -m probes.probe_phase34_capabilities
```

---

# 16. 次 Phase

```text
Phase 35+
actual H((2ι₂)η₂) calculation
```

最初に current generator typing / identity-map representation / `H(η₂)=ι₃` / multiple representation を確認し、actual calculation に不足する最小 capability だけを特定する。

不足がある場合のみ production code を追加する。
