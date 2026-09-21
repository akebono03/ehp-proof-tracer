# EHP Proof Tracer — 証明記録

この文書は、代表的な数学的証明および証明基盤の記録索引である。

詳細な過去記録は内容を削除せず `docs/proof_records/` 以下へ保存する。

現在の設計は `docs/design.md`、開発履歴は `docs/development_log.md`、今後の計画は `docs/roadmap.md` を参照する。

---

# 数学的証明記録

## 初期記録 / Toda 式 (5.8)

`docs/proof_records/early_records_and_toda_5_8.md`

## Toda Lemma 5.7 から Lemma 5.10

`docs/proof_records/toda_5_7_to_5_10.md`

## Toda Proposition 5.11 から Lemma 5.16

`docs/proof_records/toda_5_11_to_5_16.md`

## 安定 stem $G_0$ から $G_7$

`docs/proof_records/stable_stems_g0_g7.md`

---

# 証明基盤の記録

## Phase 79–89

`docs/proof_records/proof_infrastructure_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的 定理 instance filtering の記録。

## Phase 90–101

Toda 群問い合わせ、群正規化、EHP / 証明 provenance、表示 / レポート、標準運用 repository、CLI、生成元探索 の記録。

## Phase 102

`docs/proof_records/production_proof_scope_exploration_102.md`

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
適用候補 != 証明成功
関連度カテゴリ != 定理事実
表示順 != 定理順位付け
```

## Phase 104

選択候補 を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行 へ接続。

```text
候補 rule
は validation.execution_entry.rule と同一
は search_result.final_rule と同一
は goal_step.inference_rule と同一
```

```text
8644 passed in 374.63s
```

## Phase 105

最初の標準 qualified family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/proof_records/performance_applicability_106.md`

```text
797573 全 scope 候補
→ 176616 生成元関連候補
```

```text
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107 multi-family qualified execution の provenance

Phase 107 は新しい数学的定理事実 を追加していない。

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

第2 family は既存の

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
$$

を導く2前提 production rule である。

複数前提候補 から companion premise を任意探索せず、同じ root / rule / goal / source identity を満たす既存 production application を一意に recovery する。

repository 全体:

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108 利用者向け実行 provenance

Phase 108 は新しい数学的定理事実 を追加していない。

生成元入力 から qualified execution と 実際の `ProofStep` provenance を利用できる 利用者向け経路 を追加した。

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性に安全な候補選択
→ qualified execution
→ 実行済み goal_step
→ 結果 + 証明
```

候補番号 は 1-based 指定 であり 定理順位付け ではない。

```text
候補番号 != 定理順位付け
```

Windows CP932 境界 を実 subprocess smoke で検出し、script entry point の stdout / stderr を UTF-8 に統一した。

repository 全体:

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109 既知群同一性 / 証明再生 provenance

Phase 109 は新しい独立した数学的定理 root を追加していない。

既存の Toda Proposition 5.15 symbolic proof、既存 repository proof scope、既存 qualified execution の意味論 を保持したまま、既知群同一性 と 証明再生 の 利用者向け経路 を追加した。

### 証明由来の ambient-group fallback

明示的 ambient-group 事実 がない generator でも、既存 proof scope の 群 relation が generator を 直接 generator として持ち、target 群 が一意なら 既知群同一性 に利用できる。

代表例:

```text
nu_5
sigma'''
sigma''
sigma'
sigma_8
sigma_9
```

### indexed sigma 具体化

Toda Proposition 5.15:

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

具体 integer index $n\ge 10$ に対して 定理固有の具体化 を導入した。

例:

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
$$

$$
\pi_{19}^{12}=\mathbb Z/16\{\sigma_{12}\}.
$$

具体化 step は symbolic higher step を 直接 premise とする。

```text
concrete specialization
→ symbolic Proposition 5.15 higher step
```

任意の symbolic AST 書き換え は行わない。

### Known-group 証明再生

```text
generator
→ unique 既知群同一性 node
→ existing ProofStep
→ 直接 ancestry
→ 表示
```

qualified execution wrapper を流用しない。

```text
show-proof != execute
```

repository 全体:

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110 operation query / 証明再生 provenance

Phase 110 は新しい数学的定理事実 を追加していない。

既存 repository / proof-scope にすでに存在する relation・map statement・合成を含む statement を 利用者向け query から検索し、その既存 `ProofStep` provenance を保持したまま表示・replay する経路を追加した。

### 演算問い合わせ parser

最小文法:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

代表:

```text
H(nu_prime)
Delta(iota_9)
E(eta_2 o nu_prime)
eta_2 o nu_prime
```

parser は evaluator 入力を作らない。

```text
query specification
!= 数学的評価要求
```

### 既存事実検索

`H` は既存 map-relation 探索 を再利用する。

`E` は既存 repository 表現の `MapApplication(E, ...)` と `Suspension(...)` を 検索 semantics で認識する。

$\Delta$ は既存 `TodaDeltaImageUpToSignStatement` を保持する。

合成問い合わせ は 正確な `Composition` containment を探索する。

代表結果:

$$
H(\nu')=\eta_5,
$$

$$
H(\nu')=E^2\eta_3,
$$

$$
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
$$

$$
\Delta(\iota_9)
=
\pm[\iota_4,\iota_4],
$$

$$
E\eta_2\nu'=0.
$$

重要:

```text
検索 != 推論 != evaluator
```

### 生 provenance の保持

同じ `ProofStep` が複数 repository root の ancestry に現れることは provenance 上正当である。

したがって 生 lookup 出現 は削除しない。

表示 layer のみ 同一 statement を グループ化する。

```text
生 match
→ equal mathematical statement grouping
→ 表示 item
```

各 表示 item は元の全 match を保持する。

```text
deduplicated 表示
!= 生 provenance の削除
```

### 表示優先順

主要表示順 は 最浅 proof-scope depth と 安定した source 順 に基づく。

これは 定理順位付け ではない。

### Operation-query 証明再生

`query-proof` は 選択事実 の 主要 match を使う。

再生 root:

```text
selected 表示 item
→ primary_match
→ scope_node.proof_step
```

包含する repository 定理 root ではない。

例えば

$$
H(\nu')=\eta_5
$$

を replay すると depth 0 はこの relation 自身であり、直接 premises として

$$
H(\nu')=E^2\eta_3,
\qquad
E^2\eta_3=\eta_5
$$

を保持する。

```text
operation-query 証明再生
!= repository 定理再生
```

### 複数事実の安全性

複数事実 では 暗黙の自動選択 をしない。

```text
1 事実
→ --事実 省略可

複数事実
→ --事実 N が必要
```

`--事実` は 1-based 指定 であり 定理順位付け ではない。

### Statement 表示

既存 汎用 renderer で数学表示できる statement はそのまま利用する。

Phase 110 で追加した narrow 表示:

$$
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
$$

$$
E^2\nu'\in2\iota_5\circ\pi_8^5,
$$

$$
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
$$

未知 aggregate は意味を推測せず 安全な型名 fallback とする。

```text
`TodaProp56FiniteDimensionalStatement`
```

生 dataclass repr を 利用者向け再生 に漏らさない。

### CLI

```text
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"

python main.py query-proof "H(nu_prime)" --事実 1
python main.py query-proof "H(nu_prime)" --事実 2
python main.py query-proof "E(eta_2 o nu_prime)"
python main.py query-proof "eta_2 o nu_prime" --事実 4
```

### 完了

最終 repository 全体 regression:

```text
9055 passed in 455.09s (0:07:35)
```

whitespace 確認:

```text
git diff --check
clean
```

代表 smoke では `query`、`query-proof`、`execute`、`show-proof`、`python main.py 5 3` が正常に動作した。

Phase 110 は完了。

---

# 記録原則

数学的な根拠は `ProofStep` と、その実際の premise ancestry である。

```text
証明記録 != 証明事実
表示 != proof truth
production repository の組み立て != 定理事実
探索結果 != 新しい定理事実
proof-scope 走査 != 定理探索
適用候補 != 成功した証明
関連度カテゴリ != 定理事実
candidate ordering != 定理順位付け
引き渡し検証 != 定理事実
有界探索 report != 実行済み証明
qualified 候補 != 一意な実行対象
execution-family representative != 定理順位付け
一般 qualification != 具体実行成功
production-application recovery != 新しい定理事実
family dispatch != 定理順位付け
性能最適化 != 定理事実
user-facing resolver != 定理順位付け
候補番号 != theorem priority
candidate-list 表示 != proof truth
実行済み conclusion の等値 != repository target の object identity
CLI 表示 != 新しい定理事実
既知群同一性 lookup != qualified execution
証明由来 ambient fallback != 新しい定理事実
symbolic 具体化 != 任意の AST 書き換え
proof-scope 具体化 != 定理実行
known-group 証明再生 != theorem application execution
show-proof != execute
演算問い合わせ検索 != evaluator
演算問い合わせ結果 != 新しい定理事実
deduplicated 表示 != provenance deletion
表示順 != 定理順位付け
query-proof 事実 number != theorem priority
query-証明再生 != enclosing theorem replay
安全な型 fallback != 推測した定理 branch
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
