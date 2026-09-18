# 28. Proof Record 13 — Phase 78 stable G_0 through G_7

## 28.1 Scope

Phase 78 consolidates the concrete low stable stems supported by the already-derived finite-dimensional Toda results.

## 28.2 Verified results

```text
G_0=Z{ι}

(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
(G_3;2)=Z/8{ν}
(G_4;2)=0
(G_5;2)=0
(G_6;2)=Z/2{ν²}
(G_7;2)=Z/16{σ}
```

Final machine statement:

```text
TodaStableG0ToG7Statement
ProofRule.INFERENCE
```

## 28.3 表現境界

```text
G_0 = StableHomotopyGroup(stem=0)
(G_k;2) = StablePrimaryComponent(StableHomotopyGroup(stem=k), prime=2)
```

`G_0` is not represented as `(G_0;2)`.

## 28.4 Stable identification

Positive stems use:

```text
Toda45StableTwoPrimaryIdentificationStatement
```

Zero stem uses:

```text
Toda33StableOrdinaryIdentificationStatement
```

Finite-stage `Toda45IsomorphismStatement` は引き続き separate.

## 28.5 G_0 branch

```text
π_3^3=Z{ι₃}
↓
π_3(S³)=Z{ι₃}
↓
π_3(S³)≅G_0
↓
ι₃↦ι
↓
G_0=Z{ι}
```

## 28.6 G_1 branch

```text
π_4^3=Z/2{η₃}
η₃↦η
↓
(G_1;2)=Z/2{η}
```

## 28.7 G_2 branch

```text
π_6^4=Z/2{η₄²}
η₄²=η₄∘η₅
η₄²↦η²=η∘η
↓
(G_2;2)=Z/2{η²}
```

## 28.8 G_3 branch

```text
π_8^5=Z/8{ν₅}
ν₅↦ν
↓
(G_3;2)=Z/8{ν}
```

## 28.9 G_4 / G_5 zero branches

```text
π_10^6=0 -> (G_4;2)=0
π_12^7=0 -> (G_5;2)=0
```

## 28.10 G_6 branch

```text
π_14^8=Z/2{ν₈²}
ν₈²=ν₈∘ν₁₁
ν₈²↦ν²=ν∘ν
↓
(G_6;2)=Z/2{ν²}
```

## 28.11 G_7 branch

```text
π_16^9=Z/16{σ₉}
σ₉↦σ
↓
(G_7;2)=Z/16{σ}
```

## 28.12 Final integration

The final aggregate has exactly 8 direct mathematical premises in canonical order `G_0,...,G_7`.

All direct branch steps are `ProofRule.INFERENCE`.

## 28.13 Provenance / non-circularity

Verified:

```text
all 8 branches reachable
exact branch ProofStep objects reused
aggregate INFERENCE
aggregate not GIVEN
aggregate not self-ancestor
aggregate conclusion absent from ancestors
upstream branches do not depend on aggregate
proof graph acyclic
```

## 28.14 代表 probe

```powershell
python -m probes.probe_phase78_capabilities
```

The proof-style derivation is hand-authored presentation code and is not automatic `ProofStep` narrative generation.

## 28.15 回帰テスト状況

```text
aggregate: 18 passed in 2.15s
probe: 10 passed in 1.64s
integrated stable suite: 164 passed in 2.99s
repository-wide: 6472 passed in 35.18s
```

## 28.16 Completion status

Phase 78 mathematics / representation / integration / provenance / non-circularity / 代表 probe are COMPLETE.

Formal proof record corpus now contains 13 records.

---

# 29. 現在の proof-記録状態 after Phase 78

```text
1  Phase 66   Toda Equation (5.8)
2  Phase 67   Toda Lemma 5.7
3  Phase 68   Toda Proposition 5.8
4  Phase 69   Toda Equation (5.10)
5  Phase 70   Toda Proposition 5.9
6  Phase 71   Toda Equation (5.12)
7  Phase 72R  Toda Lemma 5.10 canonical revision
8  Phase 73   Toda Proposition 5.11 finite-dimensional
9  Phase 74   Toda Lemma 5.12
10 Phase 75   Toda Proposition 5.15 finite-dimensional
11 Phase 76   Toda Equation (5.16)
12 Phase 77   Toda Lemma 5.16
13 Phase 78   stable G_0 through G_7 integration
```

Low-stem stable homotopy results through stem 7 are no longer deferred.


---

