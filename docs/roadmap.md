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

# 2. Phase 33 完了時点

Completed chain:

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left
Phase 33  Barratt–Hilton prerequisites
```

Current full regression:

```text
1585 passed in 23.09s
```

---

# 3. Phase 33 completed capabilities

```text
ScalarExpression
ScalarSum
ScalarProduct
ScalarPower
symbolic Multiple coefficient
symbolic IteratedSuspension exponent
explicit parity → sign evaluation
sign evaluation → Multiple bridge
Barratt–Hilton 2 formula structural representation
Phase 33 representative probe
```

representable:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

boundary:

```text
Relation
!=
theorem-derived ProofStep
```

---

# 4. Phase 34：Toda Prop.3.1 Barratt–Hilton theorem rule

NEXT。

Phase 33 で conclusion syntax は完成済み。

Phase 34 の中心課題:

```text
[Toda] Prop.3.1
↓
explicit theorem-derived equality
```

candidate assumptions:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

conclusions:

```text
a∧b
=
(-1)^((p+k)h)
E^q a∘E^(p+k)b
```

```text
a∧b
=
(-1)^(ph)
E^p b∘E^(q+h)a
```

重要:

```text
Barratt–Hilton
!=
general smash-product normalization
```

Phase 34 は applicability / theorem provenance に必要な最小表現だけ追加する。

---

# 5. Phase 35+：actual H calculation

Phase 34 後:

```text
H((2ι₂)η₂)
```

の actual evaluation を進める。

想定:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / concrete reasoning
4ι₃
```

一方:

```text
H(4η₂)
↓ homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

よって:

```text
H((2ι₂)η₂)=H(4η₂)
```

---

# 6. equality reflection reuse

Phase 29 / 28 を再利用:

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
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

---

# 7. Toda (2.1) future candidate

必要になった時点で staged / directed rule として検討:

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

unrestricted bidirectional rewrite は導入しない。

---

# 8. Toda (5.1) future candidate

```text
π_i(S¹)=0  (i>1)
π_i(S^n)=0  (i<n)
π_n(S^n)=Z{ι_n}
```

actual proof need が現れた時点で foundational fact layer として導入する。

---

# 9. Current deferred boundaries

未実装:

```text
general symbolic scalar simplification
automatic compound parity inference
general smash-product typing / algebra
symbolic suspension typing arithmetic
Toda Prop.3.1 theorem inference
actual H((2ι₂)η₂) evaluation
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 10. Capability matrix

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
| Toda Prop.3.1 theorem rule | NEXT | 34 |
| actual H calculation | PLANNED | 35+ |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | after actual H calculation |
| `(2ι₂)η₂=4η₂` | PLANNED | reuse equality reflection |
| Toda (2.1) | PLANNED | concrete need |
| Toda (5.1) | PLANNED | concrete need |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 11. Long-term dependency

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
Toda Prop.3.1 Barratt–Hilton
↓
Phase 35+
actual H((2ι₂)η₂)
↓
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

---

# 12. Testing principle

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

# 13. Phase 33 verified status

```text
tests/test_phase33_barratt_hilton.py
73 passed in 0.31s
```

```text
full suite
1585 passed in 23.09s
```

probe:

```powershell
python -m probes.probe_phase33_capabilities
```

---

# 14. 次 Phase

```text
Phase 34
Toda Prop.3.1 Barratt–Hilton theorem rule
```

最初に current typed HomotopyElement / membership representation で theorem applicability をどこまで lossless に表現できるか確認する。

不足がある場合のみ、Phase 34 の theorem applicability に必要な最小表現を追加する。
