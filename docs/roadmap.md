# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

current specification は `README.md` / `docs/design.md` を優先する。

---

# 1. 開発原則

```text
actual mathematical need
↓
current code / test compatibility check
↓
minimum missing representation
↓
minimum theorem / fact semantics
↓
integration
↓
applicability / provenance
↓
representative probe
↓
full regression
```

---

# 2. Completed foundation

```text
Phase 1–27   generic proof / algebra / Toda bracket foundation COMPLETE
Phase 28–38  actual H / Prop.2.2 / Prop.3.1 equality branch COMPLETE
Phase 39     PrimaryComponent COMPLETE
Phase 40     TodaPrimaryGroup COMPLETE
Phase 41     PreimageSubgroup COMPLETE
Phase 42     WhiteheadProduct COMPLETE
Phase 43     Toda Lemma 4.1 premise representation COMPLETE
Phase 44     Toda Lemma 4.1 case semantics COMPLETE
Phase 45     Toda Proposition 4.2 EHP exactness COMPLETE
Phase 46     Toda (4.5) stable-range isomorphism COMPLETE
Phase 47     Toda Proposition 4.4 decomposition COMPLETE
Phase 48     Toda Proposition 4.4 E injectivity COMPLETE
```

---

# 3. Concrete low-dimensional branch

## Phase 49

Target:

```text
π_3^2=Z{η₂}
```

Result:

```text
H isomorphism
↓
η₂ = unique H-preimage of ι_3
↓
H(η₂)=ι_3
↓
π_3^2=Z{η₂}
```

verified:

```text
2557 passed in 56.45s
```

state:

```text
COMPLETE
```

---

## Phase 50

Target:

```text
π_4^3=Z/2{η₃}
```

Dependency:

```text
Toda Proposition 2.7 minimum consequence
H([ι_2,ι_2])=±2ι_3
```

Chain:

```text
H([ι_2,ι_2])=±2ι_3
+
H(η₂)=ι_3
+
H injective
↓
[ι_2,ι_2]=±2η₂
```

```text
π_5^5=Z{ι_5}
+
Δ(ι_5)=±[ι_2,ι_2]
+
[ι_2,ι_2]=±2η₂
↓
Im(Δ)=Z{2η₂}
↓
Ker(E)=Z{2η₂}
```

```text
π_4^5=0
+
E-H exact
↓
E surjective
```

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

Definition:

```text
η_n=E^(n-2)η₂
```

so:

```text
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

Representative:

```powershell
python -m probes.probe_phase50_capabilities
```

Counts:

```text
given = 11
derived = 9
rounds = 6
fixed point = True
```

verified:

```text
2703 passed in 65.69s
```

state:

```text
COMPLETE
```

---

# 4. Toda Proposition 2.7 boundary

Implemented only:

```text
H([ι_2,ι_2])=±2ι_3
```

Deferred:

```text
full Proposition 2.7 formalization
all indexed cases
general up-to-sign algebra
general sign solver
```

---

# 5. Next central direction

Phase 49–50 established:

```text
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
```

without using Proposition 5.1 as a premise.

Natural next step:

```text
Phase 51
Toda Proposition 5.1 proof dependency analysis
```

---

# 6. Phase 51 candidate：Toda Proposition 5.1 dependency analysis

確認すること:

```text
actual Proposition 5.1 statement
current proof target
current Phase 35 use of Prop.5.1-derived facts
which facts are now independently proof-derived
required low-dimensional groups
required composition relations
required suspension relations
required Hopf invariant relations
required prior Toda propositions
possible circular dependencies
```

特に Phase 49/50 の結果を Prop.5.1 proof の input として利用できるかを確認する。

production code は原則変更しない。

state:

```text
NEXT
```

---

# 7. Phase 52+ candidate：missing dependencies

Phase 51 の分析結果に応じて、必要な concrete groups / relations のみ追加する。

```text
必要と判明したものだけを追加
```

not:

```text
低次ホモトピー群 table を一括実装
```

---

# 8. Toda Proposition 5.1 proof completion

Dependency が揃った後にのみ proof completion に進む。

```text
Phase 49 / 50 low-dimensional results
↓
additional required low-dimensional groups
↓
required composition / suspension relations
↓
required prior Toda results
↓
Proposition 5.1 premises
↓
Proposition 5.1 conclusion
```

その後、既存 Phase 35–38 branch と再接続する。

---

# 9. Deferred generalizations

```text
general existential quantification
general witness / uniqueness framework
general inverse-map machinery
general cyclic-generator transport
generic typed map-property framework
general symbolic dimension solver
general symbolic map typing solver
general Whitehead-product algebra
general up-to-sign equality algebra
general sign variable / sign solver
general quotient simplification
general first-isomorphism theorem engine
general suspension normalization
general finite-cyclic direct-sum algebra
full Toda Proposition 2.7 formalization
stable homotopy group model
higher Toda brackets
general-purpose CAS normalization
```

---

# 10. Completion table

| Capability | State | Phase |
|---|---|---:|
| generic proof / algebra foundation | COMPLETE | 1–27 |
| actual H / Prop.2.2 / Prop.3.1 equality branch | COMPLETE | 28–38 |
| PrimaryComponent | COMPLETE | 39 |
| TodaPrimaryGroup | COMPLETE | 40 |
| PreimageSubgroup | COMPLETE | 41 |
| WhiteheadProduct | COMPLETE | 42 |
| Toda Lemma 4.1 premise semantics | COMPLETE | 43 |
| Toda Lemma 4.1 case semantics | COMPLETE | 44 |
| Toda Prop.4.2 EHP exactness | COMPLETE | 45 |
| Toda (4.5) stable-range isomorphism | COMPLETE | 46 |
| Toda Prop.4.4 decomposition | COMPLETE | 47 |
| Toda Prop.4.4 E injectivity | COMPLETE | 48 |
| π_3^2=Z{η₂} | COMPLETE | 49 |
| minimum Prop.2.7 consequence | COMPLETE | 50 |
| π_4^3=Z/2{η₃} | COMPLETE | 50 |
| Prop.5.1 dependency analysis | NEXT | 51 candidate |
| Prop.5.1 proof completion | PLANNED | later |
| stable homotopy | PLANNED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 11. Current immediate next step

```text
Phase 51-1
Toda Proposition 5.1 proof dependency compatibility check
```

最初に:

```text
current code
+
current tests
+
actual Proposition 5.1 proof path
```

を照合し、missing premise / theorem edge / low-dimensional group を確定する。
