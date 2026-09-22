# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

現在の標準計算経路:

```text
生の n,k 入力
→ standard production repository
→ TodaGroupQuery
→ 既知群 lookup
→ 必要なら既存 theorem-specific specialization
→ structured presentation
→ report
```

CLI:

```text
python main.py n k
```

Web:

```text
browser
→ Flask
→ thin Web adapter
→ existing calculation facade
→ existing structured presentation
→ existing LaTeX renderer
→ KaTeX
```

stable 7-stem の concrete indexed \(\sigma_n\) では、

```text
TodaGroupQuery(n,7), n >= 10
→ symbolic Proposition 5.15
→ concrete sigma_n specialization
→ group result
```

が接続済み。

例:

\[
\pi_{18}^{11}\cong
\mathbb Z/16\{\sigma_{11}\}.
\]

演算問い合わせ:

```text
operation query
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち exact E(nu_5) / E(sigma_11) のみ限定 handoff
→ structured presentation
→ query / query-proof
```

現在利用できる限定 handoff:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12}.
\]

現在の基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
LOOKUP_MISS != evaluator required
Web UI != new mathematical engine
```

Phase 117 は minimal TeX Web UI の実装・integration・browser smoke まで完了している。

最終 repository-wide regression はこのドキュメント更新後に1回だけ実行して closure を確定する。

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
```

Phase 114:

```text
existing symbolic E^(n-5)nu_5 = nu_n bridge
→ E(nu_5) = nu_6
→ operation-query minimal handoff
→ query-proof provenance
```

Phase 115:

```text
existing sigma-family definition
→ E(sigma_11) = sigma_12
→ operation-query / query-proof handoff
```

Phase 116:

```text
Web UI readiness audit
structured result / presentation boundary audit
Flask selection
KaTeX selection
thin Web adapter boundary
validation / TeX boundary audit
Phase 117 file / test boundary determination
```

Phase 117-1:

```text
Flask minimal Web app
Web group-query adapter
n,k form
KaTeX rendering
FOUND / NOT_FOUND / MULTIPLE_RESULTS presentation
focused Web tests
```

Phase 117-2:

```text
Web / CLI same-result regression
negative-k validation
missing-input boundary
MULTIPLE_RESULTS no-auto-selection
```

Phase 117-3:

```text
browser smoke audit
KaTeX live rendering confirmation
HTML min removal
Python domain-validation authority
```

Phase 117-4:

```text
current documentation update
completion boundary audit
final repository-wide regression remains
```

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

---

# 4. 現在の Web UI

起動:

```text
python -m flask --app web_app run --debug
```

現在の対象:

```text
n 入力
k 入力
group calculation
FOUND
NOT_FOUND
MULTIPLE_RESULTS
Python domain validation
KaTeX result rendering
```

代表例:

```text
n = 11
k = 7
```

\[
\pi_{18}^{11}\cong
\mathbb Z/16\{\sigma_{11}\}.
\]

現在の Web UI は group query のみを扱う。

未接続:

```text
operation query
query-proof
show-proof
explore
explore-proof
explore-applicable
execute
```

---

# 5. Web 設計原則

```text
existing repository / calculation / query / proof layer
→ thin Web adapter
→ Web endpoint
→ browser presentation
→ KaTeX
```

重要:

```text
Web UI != new theorem source
Web UI != general evaluator
Web UI != alternate proof engine
Web UI != CLI subprocess wrapper
TeX rendering != mathematical normalization
```

CLI 文字列や Markdown を Web で再解析しない。

structured result / presentation object を利用する。

---

# 6. Phase 117 完了境界

Phase 117 の機能条件:

```text
ブラウザから n,k を入力できる
既存計算経路と同じ結果を返す
数学式を KaTeX で表示する
CLI と Web の数学結果が一致する
NOT_FOUND を明示する
MULTIPLE_RESULTS を自動選択しない
既存 Python domain validation を維持する
repository / proof semantics を変更しない
focused Web tests が通る
browser smoke が通る
```

確認済み focused results:

```text
tests/test_phase117_web_app.py
→ 10 passed

tests/test_phase117_web_group_query.py
→ 4 passed

tests/test_phase113_sigma_group_query_integration.py
→ 7 passed
```

browser smoke:

```text
n=11, k=7
→ KaTeX rendering confirmed

n=0, k=7
→ n must be positive

n=11, k=-1
→ k must be nonnegative
```

残る closure 条件:

```text
repository-wide pytest
```

---

# 7. Phase 118: operation query / query-proof Web integration

Phase 118 は Phase 117 で確立した Web boundary を再利用する。

対象:

```text
operation query input
existing operation-query facade
existing structured operation-query presentation
query result Web rendering
query-proof selection
bounded replay depth
```

代表 query:

```text
H(nu_prime)
Delta(iota_9)
E(eta_2 o nu_prime)
E(nu_5)
E(sigma_11)
eta_2 o nu_prime
eta_2 o nu_prime o eta_6
```

設計:

```text
browser query
→ thin operation-query Web adapter
→ existing operation-query facade
→ existing structured presentation
→ HTML / KaTeX
```

query-proof:

```text
selected fact
→ existing proof replay
→ existing replay presentation
→ HTML / KaTeX
```

Phase 118 では新しい query grammar や general evaluator を追加しない。

```text
Web operation query
!= query semantics expansion
```

---

# 8. Phase 119: bounded proof replay Web presentation

候補:

```text
proof depth 切替
premise 階層表示
theorem / phase provenance
数式 TeX rendering
unsupported statement の安全な fallback
```

最初から graph visualization library を導入しない。

```text
proof presentation != new proof search
depth control != proof optimization
```

---

# 9. Phase 120: exploration / execution Web integration audit

再監査対象:

```text
explore
explore-proof
explore-applicable
show-proof
execute
```

`execute` は query / replay より意味論が複雑なので Phase 117–119 で先取りしない。

Phase 120 の監査結果に応じて、その後の Web Phase を決める。

---

# 10. Web UI 導入後の数学的 pressure

Web UI の導入は数学機能開発の終了を意味しない。

再評価候補:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

今後の循環:

```text
CLI / Web での実利用
→ capability pressure の確認
→ 既存数学の再利用可否を監査
→ 最小数学機能を選定
→ 実装
```

---

# 11. 長期保留機能

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
rich graph proof visualization
odd-primary integration
all-primary ordinary sphere-homotopy calculation
authentication
database persistence
deployment automation
rich SPA architecture
```

---

# 12. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい定理 root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の結果を分岐させない
focused regression で境界を固定する
repository-wide regression で Phase を閉じる
```

Phase 115 の最新確定 full regression:

```text
9111 passed in 432.54s (0:07:12)
```

Phase 117 の final repository-wide regression は documentation update 後に実行する。
