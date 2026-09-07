# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

現在の仕様は `README.md` / `docs/design.md` を優先する。

---

# 1. 開発原則

```text
実際の数学的必要
↓
現在のコード / テスト互換性確認
↓
不足している最小表現
↓
最小限の定理 / fact 意味論
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

# 2. 完了済み基盤

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

# 3. 具体的低次元 branch

## Phase 49

目標:

```text
π_3^2=Z{η₂}
```

結果:

```text
H isomorphism
↓
η₂ = ι_3 の一意な H-preimage
↓
H(η₂)=ι_3
↓
π_3^2=Z{η₂}
```

検証:

```text
2557 passed in 56.45s
```

状態:

```text
COMPLETE
```

---

## Phase 50

目標:

```text
π_4^3=Z/2{η₃}
```

依存:

```text
Toda Proposition 2.7 minimum consequence
H([ι_2,ι_2])=±2ι_3
```

推論経路:

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

定義:

```text
η_n=E^(n-2)η₂
```

したがって:

```text
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

代表 probe:

```powershell
python -m probes.probe_phase50_capabilities
```

件数:

```text
given = 11
derived = 9
rounds = 6
fixed point = True
```

検証:

```text
2703 passed in 65.69s
```

状態:

```text
COMPLETE
```

---

# 4. Toda Proposition 2.7 の境界

実装済みなのは次だけ:

```text
H([ι_2,ι_2])=±2ι_3
```

保留:

```text
full Proposition 2.7 formalization
all indexed cases
general up-to-sign algebra
general sign solver
```

---

# 5. 現在の中心方向

Phase 49–50 で:

```text
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
```

を Proposition 5.1 を premise に使わずに導出できるようになった。

Phase 51 では Proposition 5.1 の依存関係分析を完了した。

Phase 52–54 で不足していた有限次元側の edge を順に埋めた。

---

# 6. Phase 51：Toda Proposition 5.1 dependency analysis

分析した有限次元側の目標:

```text
π_3^2=Z{η₂}
π_{n+1}^n=Z/2{η_n}  (n≥3)
H(η₂)=ι₃
Δ(ι₅)=±2η₂
```

Toda p.39 には内部表記の不整合があり、proof text は `Δ(ι₅)=±2η₂`、printed proposition line は `±2η₃` となっている。

開発上は proof text と `Δ(ι₅)∈π_3^2` の次元に整合する:

```text
Δ(ι₅)=±2η₂
```

を採用する。

Proposition 5.1 から独立して利用可能と確認したもの:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
π_4^3=Z/2{η₃}
η_n=E^(n-2)η₂ structural definition
Toda (4.5) stable-range isomorphism
```

追加の低次元 group fact は不要と判断。

不足実装を次の4点に限定した:

```text
1. Δ(ι₅)=±2η₂ direct bridge
2. Toda (4.5) finite-cyclic transport
3. E^(n-3)η₃=η_n bridge
4. finite-dimensional Prop.5.1 integration / provenance
```

循環依存の境界:

```text
SAFE:
Phase 49 / 50 derived results
Toda Prop.2.7 / Prop.4.2 / (4.5) dependencies

UNSAFE AS PROP.5.1 PREMISE:
old H(η₂)=ι₃ literature GIVEN attributed to Prop.5.1
old Phase 35–36 traces carrying that provenance
```

状態:

```text
COMPLETE
```

---

# 7. Phase 52：Δ(ι₅)=±2η₂ direct bridge

目標:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

実装:

```text
既存 up-to-sign statement の再利用
Toda-specific direct bridge rule
wrong-instance rejection
Phase 50 chain integration
INFERENCE provenance
representative probe
```

代表実行:

```text
given = 11
derived = 10
rounds = 6
fixed point = True
```

検証:

```text
2731 passed in 26.67s
```

境界:

```text
theorem-specific direct bridge only
no general up-to-sign transitivity
no sign solver
```

状態:

```text
COMPLETE
```

---

# 8. Phase 53–55：Proposition 5.1 有限次元側の completion path

## Phase 53

```text
Toda (4.5) finite-cyclic transport

π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

代表実行:

```text
given = 14
derived = 11
rounds = 7
fixed point = True
```

検証:

```text
2769 passed in 25.60s
```

状態:

```text
COMPLETE
```

---

## Phase 54

higher η-family bridge:

```text
η_n=E^(n-2)η₂
+
η₃=Eη₂
↓
E^(n-3)η₃=η_n
```

Phase 53 transport との統合:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
+
E^(n-3)η₃=η_n
↓
π_{n+1}^n=Z/2{η_n}
```

実装:

```text
symbolic η_n minimum representation
η_n=E^(n-2)η₂ structural definition
η-family-specific bridge rule
wrong-instance rejection
specific finite-cyclic generator bridge
Phase 53 + Phase 54 same-run integration
derived provenance
representative probe
```

代表実行:

```text
given = 15
derived = 13
rounds = 8
fixed point = True
```

Phase 54 tests:

```text
tests/test_phase54_eta_family_bridge.py  20 passed
tests/test_phase54_integration.py         7 passed
tests/test_phase54_probe.py               8 passed
```

全体回帰:

```text
2804 passed in 26.50s
```

境界:

```text
η-family-specific bridge only
specific finite-cyclic generator bridge only
no generic iterated-suspension composition
no generic suspension normalization
no generic scalar normalization
no generic cyclic-generator rewrite
no stable homotopy model
```

状態:

```text
COMPLETE
```

---

## Phase 55（NEXT）

目的:

```text
Toda Proposition 5.1
finite-dimensional integration / provenance
```

現在、有限次元側で独立に導出済み:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

Phase 55 ではこれらを一つの Proposition 5.1 finite-dimensional result として統合し、provenance と循環依存がないことを固定する。

重要:

```text
Prop.5.1 自身を premise にしない
old literature GIVEN H(η₂)=ι₃ を premise にしない
old Phase 35–36 trace をそのまま premise にしない
```

Phase 55 の中心確認:

```text
Phase 49 derived:
π_3^2=Z{η₂}
H(η₂)=ι₃

Phase 52 derived:
Δ(ι₅)=±2η₂

Phase 54 derived:
π_{n+1}^n=Z/2{η_n}

↓
Toda Proposition 5.1 finite-dimensional integration
```

まだ先取りしない:

```text
(G_1;2)=Z/2{η}
stable homotopy group model
composition isomorphism (5.2)
generic cyclic-generator rewrite
generic scalar normalization
generic suspension normalization
```

---

# 9. 保留中の一般化

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
general iterated-suspension composition algebra
general scalar normalization
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
| Prop.5.1 dependency analysis | COMPLETE | 51 |
| Δ(ι₅)=±2η₂ direct bridge | COMPLETE | 52 |
| Toda (4.5) finite-cyclic transport | COMPLETE | 53 |
| higher η-family bridge | COMPLETE | 54 |
| π_{n+1}^n=Z/2{η_n} | COMPLETE | 54 |
| Prop.5.1 finite-dimensional integration / provenance | NEXT | 55 |
| Prop.5.1 stable `(G_1;2)` conclusion | DEFERRED | later |
| stable homotopy | PLANNED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 11. 現在の直近ステップ

Phase 54 まで完了。

現在 independently derived できる有限次元結果:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
π_4^3=Z/2{η₃}
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

次:

```text
Phase 55
Toda Proposition 5.1
finite-dimensional integration / provenance
```

Phase 55 の目的は新しい低次元 group fact を増やすことではなく、既存の独立導出済み結果を Proposition 5.1 の有限次元 statement として統合し、その依存関係を検証すること。

---

# 12. 具体的結果の保存・照合・検証方針

Phase 49–54 で:

```text
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
π_{n+1}^n=Z/2{η_n}
```

のような具体的結果を theorem / fact dependency から end-to-end で導出できるようになった。

今後は推論結果を probe 出力やテストだけに閉じず、再利用可能な fact として保存・照合できる層を検討する。

目標:

```text
定理・推論ルール
↓
推論された具体的 fact
↓
fact repository / database
↓
既存 table / 文献値との比較
```

重要:

```text
推論エンジン
!=
fact repository
!=
既存 table
```

各層を分離する。

---

# 13. Homotopy fact repository candidate

将来的な保存対象候補:

```text
group fact
π_n(S^k)=...

Toda group fact
π_i^n=...

primary component fact
π_i(S^n;p)=...

generator fact
π_3^2=Z{η₂}

element relation
H(η₂)=ι₃
Eη₂=η₃
E^(n-3)η₃=η_n

order fact
2η₃=0

map property
E injective
H isomorphism
```

結果だけでなく:

```text
result
+
source / provenance
+
premises
+
used inference rules
+
proof trace
```

を保持できる形を目標とする。

現在の `ProofStep` provenance を再利用し、別の一般的 proof engine は先取りしない。

---

# 14. Fact source の区別

将来 repository / database を導入する場合、fact の由来を区別する。

候補:

```text
LITERATURE_FACT
文献から直接与えた fact

TABLE_FACT
既存 homotopy-group table から読み込んだ fact

USER_IMPORTED_FACT
ユーザーが外部 table などから取り込んだ fact

DERIVED_FACT
EHP Proof Tracer が推論して得た fact
```

重要:

```text
table に書いてある
!=
proof により導出された
```

既存 table を検証対象にする場合、その table の値を同じ proof の premise として無条件に使わない。

循環する verification を避ける。

---

# 15. 既存 table との照合

将来、以前作成した homotopy-group table と推論結果を比較できるようにする。

基本方向:

```text
Inference
↓
Derived fact
↓
Existing table lookup
↓
comparison
```

初期段階では table は verification source として使い、推論そのものの根拠にはしない。

比較結果候補:

```text
MATCH
推論結果と table が一致

PARTIAL_MATCH
2-primary 部分など確認できた範囲のみ一致

CONFLICT
推論結果と table が矛盾

NO_ENTRY
table に対応する entry がない

NOT_DERIVED
table entry はあるが現在の engine ではまだ導出できない
```

これにより、以前作成した table の確認に利用できる。

---

# 16. Table verification の将来目標

将来的には table 各 entry に対して:

```text
VERIFIED
DERIVABLE
CONSISTENT_BUT_NOT_DERIVED
PARTIALLY_VERIFIED
CONFLICT
UNKNOWN
```

のような検証状態を持たせることを検討する。

例:

```text
π_3(S^2)=Z
→ VERIFIED

π_4(S^3)=Z/2
→ VERIFIED

odd-primary part が未実装
→ PARTIALLY_VERIFIED

必要 theorem が未実装
→ UNKNOWN
```

重要:

```text
UNKNOWN
!=
FALSE
```

現在の capability で導出できないことと、table が誤っていることを区別する。

---

# 17. Repository / database 導入時期

今すぐ SQLite 等の本格 database を先に設計しない。

まず:

```text
Phase 49
π_3^2

Phase 50
π_4^3

Phase 52
Δ(ι₅)=±2η₂

Phase 53–54
π_{n+1}^n=Z/2{η_n}

Phase 55
Prop.5.1 finite-dimensional integration / provenance
```

のような具体的結果を継続して蓄積し、

```text
どの種類の fact を保存する必要があるか
どの provenance が必要か
どの検索 key が必要か
どの比較単位が必要か
```

を実際の利用例から確定する。

その後:

```text
current concrete calculations
↓
common fact schema
↓
repository interface
↓
persistent storage if needed
```

の順で導入する。

重要:

```text
database first
```

ではなく:

```text
actual data need
↓
minimum schema
↓
repository
↓
persistent database
```

とする。

---

# 18. Repository candidate の実装境界

将来の candidate capability:

```text
HomotopyFactRepository
fact registration
fact lookup
derived-fact storage
provenance retention
table import
derived-vs-table comparison
conflict detection
verification status
```

まだ先取りしない:

```text
general SQL schema
general graph database
general theorem knowledge base
automatic literature scraping
automatic trust ranking
automatic correction of table data
full odd-primary database
general CAS-backed normalization
```

---

# 19. Concrete calculation と repository の関係

今後の基本 workflow candidate:

```text
必要な具体的ホモトピー群を選ぶ
↓
既存 fact を lookup
↓
不足 theorem / fact を推論
↓
新しい concrete result を導出
↓
DERIVED_FACT として保存
↓
既存 table があれば照合
↓
MATCH / CONFLICT / UNKNOWN 等を記録
```

将来的には:

```text
query:
π_n(S^k) は何か

↓
repository lookup

ある:
stored result + provenance を返す

ない:
current inference capability で導出を試す

↓
導出成功:
repository に追加

↓
table entry があれば比較
```

という利用形態を目標とする。

---

# 20. 更新後の長期方向

現在の中心 branch:

```text
Phase 49
π_3^2=Z{η₂}
COMPLETE
↓
Phase 50
π_4^3=Z/2{η₃}
COMPLETE
↓
Phase 51
Toda Proposition 5.1 dependency analysis
COMPLETE
↓
Phase 52
Δ(ι₅)=±2η₂ direct bridge
COMPLETE
↓
Phase 53
Toda (4.5) finite-cyclic transport
COMPLETE
↓
Phase 54
E^(n-3)η₃=η_n
π_{n+1}^n=Z/2{η_n}
COMPLETE
↓
Phase 55
Toda Proposition 5.1 finite-dimensional integration / provenance
NEXT
```

stable branch:

```text
(G_1;2)=Z/2{η}
DEFERRED
```

並行する将来 architecture branch:

```text
concrete derived facts accumulate
↓
fact schema becomes clear
↓
HomotopyFactRepository candidate
↓
previous table comparison
↓
table verification
↓
persistent database if needed
```

repository / database branch は具体的計算を妨げないタイミングで導入する。

---

# 21. 将来 backlog

具体的計算で必要になるまで保留する Toda 項目:

```text
Lem 1.1
Prop 1.2
Prop 1.3 の下の式
Prop 1.4
Prop 1.5
Prop 1.6
(2.1)
Prop 2.3
Prop 2.5 の 2-primary case
Prop 2.6
Cor 3.7
Lem 4.3
Lem 4.5
```

方針:

```text
DEFERRED UNTIL CONCRETE NEED
```

ただし:

```text
Prop 2.7
```

は Phase 50 の `π_4^3` 計算で minimum consequence が既に使用されたため、この backlog から除外する。

---

# 22. Phase 54 完了後の直近ステップ

Phase 54 は完了。

Phase 54 で追加された結果:

```text
η_n=E^(n-2)η₂
+
η₃=Eη₂
↓
E^(n-3)η₃=η_n
```

さらに:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
+
E^(n-3)η₃=η_n
↓
π_{n+1}^n=Z/2{η_n}
```

代表実行:

```text
given = 15
derived = 13
rounds = 8
fixed point = True
```

検証:

```text
2804 passed in 26.50s
```

次:

```text
Phase 55
Toda Proposition 5.1
finite-dimensional integration / provenance
```

Phase 55 の現在の input:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

目標:

```text
上記4結果を Proposition 5.1 finite-dimensional result として
同一 provenance chain 上で統合する
```

境界:

```text
no Proposition 5.1 GIVEN premise
no old literature-derived circular H premise
no stable (G_1;2) conclusion
no stable homotopy model
no composition isomorphism (5.2)
```
