# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

運用計算:

```text
生の n,k 入力
→ python main.py n k
→ 標準運用 repository
→ 既知群 lookup
→ 必要なら既存 theorem-specific specialization
→ 証明レポート
```

stable 7-stem の concrete indexed $\sigma_n$ については、

```text
TodaGroupQuery(n,7), n >= 10
→ symbolic Proposition 5.15
→ concrete sigma_n specialization
→ group result
```

が接続済み。

例:

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\}.
$$

演算問い合わせ:

```text
operation query
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち exact E(nu_5) / E(sigma_11) のみ限定 handoff
→ 重複除去済み数学表示
→ 保持された provenance
→ python main.py query ...
```

現在利用できる限定 handoff:

$$
E(\nu_5)=\nu_6,
$$

$$
E(\sigma_{11})=\sigma_{12}.
$$

現在の境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
LOOKUP_MISS != evaluator required
```

最新:

```text
Phase 115 closure:
9111 passed in 432.54s (0:07:12)
```

Phase 115 は完了。

---

# 2. 完了済み機能

Phase 90–104:

```text
問い合わせ / 正規化
EHP / 証明 provenance
計算オーケストレーション / レポート
生成元探索
再帰的 proof scope
適用可能性探索
関連度分類
安全な候補引き渡し
有界実行 provenance
```

Phase 105–111:

```text
qualified execution
user-facing execute
known-group identity
indexed sigma specialization
show-proof
operation query / query-proof
CLI usability audit
3-term top-level composition query
replay --depth
```

Phase 112:

```text
nu_prime / nu_5 / sigma_11 end-to-end workflow audit
operation / workflow capability gap classification
lookup vs inference vs evaluator boundary audit
highest-pressure minimal capability selection
```

Phase 113:

```text
symbolic sigma_n specialization
→ TodaGroupQuery integration

n=10,11,12 の 7-stem で確認
空 repository では結果を生成しない
Toda Proposition 5.15 provenance を保持
```

Phase 114:

```text
existing symbolic E^(n-5)nu_5 = nu_n bridge
→ n=6 theorem-specific specialization
→ E(nu_5) = nu_6
→ operation-query minimal handoff
→ query-proof provenance

direct lookup priority を維持
general E/H/Delta evaluator は追加しない
```

Phase 115:

```text
post-Phase 114 operation / workflow pressure audit
→ existing mathematics reuse audit
→ exact E(sigma_11) を最小対象として選定
→ Toda Lemma 5.14 sigma-family definition を再利用
→ E(sigma_11) = sigma_12
→ operation-query / query-proof handoff
→ post-implementation boundary audit
```

Phase 115 でも general $E/H/\Delta$ evaluator は追加していない。

---

# 3. 現在の CLI

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py show-proof nu_prime
python main.py show-proof sigma_11 --depth 2
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "E(nu_5)"
python main.py query "E(sigma_11)"
python main.py query "eta_2 o nu_prime"
python main.py query "eta_2 o nu_prime o eta_6"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 1 --depth 2
python main.py query-proof "E(nu_5)"
python main.py query-proof "E(nu_5)" --depth 2
python main.py query-proof "E(sigma_11)"
python main.py query-proof "E(sigma_11)" --depth 2
```

stable 7-stem concrete query 例:

```text
python main.py 10 7
python main.py 11 7
python main.py 12 7
```

---

# 4. Capability gap の現在分類

Phase 112 以降、問い合わせ失敗を次のように区別する。

```text
parser boundary
repository lookup miss
existing inference capability but no query handoff
existing specialization but no workflow handoff
new inference required
presentation-only issue
execution boundary
```

Phase 113 で解消:

```text
python main.py 11 7
→ existing sigma_n specialization を TodaGroupQuery が再利用
```

Phase 114 で解消:

```text
query "E(nu_5)"
→ direct lookup miss
→ existing nu-family symbolic bridge
→ exact concrete specialization
→ E(nu_5) = nu_6
```

Phase 115 で解消:

```text
query "E(sigma_11)"
→ direct lookup miss
→ existing TodaSigmaFamilyDefinitionStatement
→ sigma_11 / sigma_12 concrete definition
→ E(sigma_11) = sigma_12
```

Phase 115-5 で残存 pressure を再分類した。

```text
H(nu_5)
→ new mathematical inference required

H(sigma_11)
→ related low-dimensional mathematics exists
→ reusable sigma-family H bridge is not currently present

Delta(sigma_11)
→ reusable concrete / family relation is not currently present

E(nu_prime)
→ E nu_prime appears inside existing expressions
→ no operation-result relation E(nu_prime) = ... is present

Delta(nu_prime)
→ direct / reusable family inference is not currently present

E(nu_5 o eta_8)
→ composition-operation inference boundary

E(a o b o c)
→ parser boundary

four-term composition
→ parser boundary

execute sigma_11
→ execution coverage boundary
```

これらを general evaluator が必要と決めつけない。

---

# 5. Phase 114 完了境界

Phase 114 の対象は

$$
E(\nu_5)=\nu_6
$$

だけであった。

source:

$$
E^{n-5}\nu_5=\nu_n.
$$

実装境界:

```text
query input
→ existing direct lookup
→ direct fact があれば従来どおり返す
→ lookup miss
→ exact E(nu_5) guard
→ theorem-specific concrete specialization
→ proof provenance
→ query / query-proof
```

Phase 115 の追加後も Phase 114 の $\nu_5$-specific guard 自体は $\sigma$-family を受理しない。

---

# 6. Phase 115 完了境界

Phase 115 は Phase 114 の handoff pattern を機械的に一般化せず、まず残存 pressure を分類した。

最小再利用対象として

$$
E(\sigma_{11})=\sigma_{12}
$$

を選定した。

既存 Toda Lemma 5.14 の family definition:

$$
\sigma_n=E^{n-8}\sigma_8
$$

から concrete definition

$$
\sigma_{11}=E^3\sigma_8,
\qquad
\sigma_{12}=E^4\sigma_8
$$

を利用し、operation-query 用 concrete `Relation`

$$
E(\sigma_{11})=\sigma_{12}
$$

を構成する。

provenance:

```text
concrete E(sigma_11) = sigma_12 step
→ symbolic TodaSigmaFamilyDefinitionStatement
→ TodaLemma514Sigma8Statement
→ n >= 8
```

実装境界:

```text
query input
→ existing direct lookup
→ direct fact があれば従来どおり返す
→ lookup miss
→ exact E(sigma_11) guard
→ theorem-specific definitional specialization
→ proof provenance
→ query / query-proof
```

変更:

```text
repository_sigma11_suspension_specialization.py
repository_operation_query_facade.py
tests/test_phase115_sigma11_operation_query_handoff.py
```

`repository_operation_query_lookup.py`、renderer、parser、repository root は変更していない。

意図的な非拡張:

```text
E(sigma_10)
E(sigma_12)
E(sigma_100)
H(sigma_11)
Delta(sigma_11)
E(sigma_11 o eta_18)
```

したがって:

```text
exact E(sigma_11) handoff
!= general E(sigma_n) evaluator
!= general E evaluator
!= arbitrary symbolic substitution
```

---

# 7. Phase 115 で先取りしなかったもの

```text
general E evaluator
general H evaluator
general Delta evaluator
general E(sigma_n) family handoff
任意の operation-query inference fallback
四項以上 composition
三項 map-operation operand
Unicode ∘
一般 expression parser
execute sigma_11
第3 qualified execution family
odd-primary integration
```

---

# 8. 保留中の機能

```text
operation-query grammar generalization
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
semantic theorem ranking
proof-cost optimization
producer ranking
unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
rich recursive proof visualization
Web UI
odd-primary integration
all-primary ordinary sphere-homotopy calculation
```

operation-query の具体的残件:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

これらは Phase 115 と同じ「既存 family definition の未接続」とは分類しない。

---

# 9. 表示上の既知残件

Phase 114 の query-proof で symbolic bridge が

```text
E^{n + -1\,5}ν_5 = ν_n
```

の形で表示される場合がある。

数学的内容は

$$
E^{n-5}\nu_5=\nu_n.
$$

これは inference handoff / proof correctness ではなく scalar LaTeX presentation の残件である。

Phase 115 の機能追加とは分離して保留する。

---

# 10. 次 Phase の方針

Phase 116 は、残存 operation miss のどれかを自動的に実装することから始めない。

まず、

```text
remaining mathematical pressure
presentation-only residual
parser / execution boundary
actual user workflow need
```

を比較し、次の最小対象を選定する。

候補:

```text
symbolic scalar LaTeX presentation
H(nu_5) の数学的 dependency audit
H(sigma_11) の suspension / Hopf relation audit
Delta(sigma_11) の dependency audit
E(nu_prime) / Delta(nu_prime) semantics audit
```

優先度は audit 前に固定しない。

---

# 11. 完了判断原則

Phase 116 以降も次を維持する。

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい定理 root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
focused regression で境界を固定する
repository-wide regression で閉じる
```

Phase 115 closure:

```text
Phase 115 dedicated:
14 passed

Phase 114 compatibility:
16 passed

related regression:
97 passed

repository-wide:
9111 passed in 432.54s (0:07:12)
```
