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


---

# 12. 具体的結果の保存・照合・検証方針

Phase 49–50 で:

```text
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
```

のような具体的結果を、EHP exactness と theorem / fact dependency から end-to-end で導出できるようになった。

今後は、推論結果を probe 出力やテストだけに閉じず、再利用可能な fact として保存・照合できる層を検討する。

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

order fact
2η₃=0

map property
E injective
H isomorphism
```

結果だけではなく:

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

既存 table を検証対象とする場合、その table の値を同じ proof の premise として無条件に使用しない。

circular verification を避ける。

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
table entry はあるが current engine ではまだ導出できない
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

current capability で導出できないことと、table が誤っていることを区別する。

---

# 17. Repository / database 導入時期

今すぐ SQLite 等の本格 database を先に設計しない。

まず:

```text
Phase 49
π_3^2

Phase 50
π_4^3

Phase 51+
Prop.5.1 dependency に必要な具体的群・relation
```

を継続して計算し、

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

# 20. Updated long-term direction

現在の central branch:

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
NEXT
↓
必要な concrete low-dimensional calculations
↓
Toda backlog から必要 theorem のみ昇格
↓
Toda Proposition 5.1 proof completion
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

repository / database branch は concrete calculation を妨げないタイミングで導入する。

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

# 22. Updated immediate next step

```text
Phase 51-1
Toda Proposition 5.1 proof dependency compatibility check
```

確認:

```text
current code
+
current tests
+
Phase 49 / 50 derived facts
+
actual Proposition 5.1 proof path
```

から:

```text
missing low-dimensional fact
missing relation
missing theorem dependency
possible circular dependency
```

を確定する。

repository / database は Phase 51 のために先取り実装しない。

ただし Phase 51 以降で concrete fact がさらに増え、同じ保存・lookup・比較処理が繰り返し必要になった時点で:

```text
HomotopyFactRepository compatibility check
```

を新しい Phase candidate として昇格する。
