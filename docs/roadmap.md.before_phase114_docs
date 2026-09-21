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
→ 既存 repository / proof-scope 事実検索
→ 重複除去済み数学表示
→ 保持された provenance
→ python main.py query ...
```

現在も

```text
query = lookup
lookup != inference != evaluator
```

である。

最新:

```text
Phase 113 closure:
9081 passed in 434.58s (0:07:14)
```

Phase 113 は完了。

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
python main.py query "eta_2 o nu_prime"
python main.py query "eta_2 o nu_prime o eta_6"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 1 --depth 2
```

stable 7-stem concrete query 例:

```text
python main.py 10 7
python main.py 11 7
python main.py 12 7
```

---

# 4. Phase 112 で確定した capability 分類

```text
parser boundary
repository lookup miss
existing inference capability but no query handoff
existing specialization but no workflow handoff
possible genuinely new inference / evaluator need
```

代表例:

```text
python main.py 11 7
→ Phase 113 で orchestration gap を解消済み

query "E(nu_5)"
→ lookup miss
→ 既存 nu-family stable transport に数学的情報あり
→ general evaluator を作る前に最小 handoff を検討

query "E(sigma_11)"
→ lookup miss
→ sigma-family definition に既存情報あり
→ general evaluator を作る前に最小 handoff を検討

H(nu_5), H(sigma_11), Delta(sigma_11)
→ 新 inference / evaluator 候補として保留
```

---

# 5. Phase 114 第一候補

次 Phase:

```text
Phase 114
operation query → existing inference minimal handoff
```

最初の代表対象は

$$
E(\nu_5)=\nu_6
$$

とする。

ただし最初から general operation evaluator を作らない。

想定する境界:

```text
query input
→ existing direct lookup
→ direct fact があれば従来どおり返す
→ lookup miss
→ Phase 114 で許可した最小既存 inference handoff
→ proof provenance
→ query / query-proof
```

---

# 6. Phase 114 で先取りしないもの

```text
general E evaluator
general H evaluator
general Delta evaluator
任意の operation-query inference fallback
四項以上 composition
三項 map-operation operand
Unicode ∘
一般 expression parser
execute sigma_11
第3 qualified execution family
```

---

# 7. 保留中の機能

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

---

# 8. 次 Phase の開始境界

Phase 114 開始前に、

```text
E(nu_5)
→ どの既存 ProofStep / symbolic relation を使うか
→ concrete n=6 specialization が既存 machinery だけで成立するか
→ query result と query-proof provenance をどう保持するか
```

を現行 GitHub コードと関連テストで確認する。

目的は「query を一般 evaluator に変えること」ではない。

```text
既存数学
→ 最小 handoff
→ provenance を保持した利用者向け query
```

に限定する。
