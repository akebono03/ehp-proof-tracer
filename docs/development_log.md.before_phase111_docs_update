# EHP Proof Tracer 開発記録

この文書は開発履歴の索引である。

現在の仕様・設計は `README.md` と `docs/design.md` を優先する。
今後の計画は `docs/roadmap.md`、代表的な数学的証明・証明基盤の記録は `docs/proof_records.md` を参照する。

過去の詳細な開発記録は、内容を削除せず `docs/development_log/` 以下へ分割して保存する。

---

# 開発履歴アーカイブ

## Phase 1–48

`docs/development_log/phases_001_048.md`

可換群計算、汎用推論、EHP、Toda の基礎表現から Proposition 4.4 周辺まで。

## Phase 49–64

`docs/development_log/phases_049_064.md`

\(\pi_3^2\)、\(\pi_4^3\)、Toda Proposition 5.1、Lemma 5.2、\(\nu'\)、\(\nu_4\)、\(\nu\)-family、性能安定化まで。

## Phase 65–78

`docs/development_log/phases_065_078.md`

Toda Proposition 5.6 から Lemma 5.16、安定 \(G_0\) から \(G_7\) までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的 定理 instance 適合性 まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda 群問い合わせ、正規化済み 群結果、EHP provenance、flat / recursive 証明 provenance、計算オーケストレーションの記録。

## Phase 96–98

```text
Phase 96:
構造化表示 / 読みやすい完全証明レポート
7609 passed in 121.63s

Phase 97:
計算からレポートまでのオーケストレーション
7609 passed in 121.63s

Phase 98:
生の n,k 入力用簡易 facade
7643 passed in 123.73s
```

詳細:

```text
docs/development_log/phases_096.md
docs/development_log/phases_097.md
docs/development_log/phases_098.md
```

## Phase 99

元中心の repository 探索 を追加。

```text
GeneratorSymbol
→ 出現
→ 意味論的役割
→ グループ化表示
→ Markdown
→ 一括探索 facade
```

```text
7824 passed in 136.59s
```

## Phase 100

標準運用 repository、`build_standard_toda_report(n,k)`、`python main.py n k` を統合。

```text
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

生成元中心の探索 を標準 repository と `main.py explore` へ接続。

```text
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

再帰的 proof-scope 探索、Toda membership、既知の写像関係探索 を追加。

代表結果:

\[
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
\]

```text
8142 passed in 129.93s
```

## Phase 103

`docs/development_log/phases_103.md`

適用可能な定理 / 補題の探索 と 関連度分類 を追加。

```text
409 passed in 186.07s
```

## Phase 104

選択された適用候補 を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行 へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

第1 qualified production family を 標準 applicability workflow へ接続。

対象:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/development_log/phases_106.md`

適用可能性の性能 / 複雑性監査。

```text
797573 全 scope 候補
→ 176616 生成元関連候補
```

生成元関連 scope prefilter を実装。

```text
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107

`docs/development_log/phases_107.md`

第1 family 限定実行 を multi-family 実行 へ拡張。

第2 qualified family:

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

主要機能:

```text
正確な production application recovery
NONE / UNIQUE / AMBIGUOUS recovery 状態
正確な複数前提 seed
2前提有界実行の統合
明示的 root + source + family 選択
一般 qualified-family admission
family 名 dispatch
multi-family 標準 facade
```

repository 全体:

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108

Phase 107 の 内部 qualified execution を 利用者向け workflow と CLI へ接続。

主要機能:

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性処理
→ 候補一覧
→ 候補選択
→ qualified execution
→ 最終実行済み ProofStep
→ 結果 + 証明表示
→ CLI
```

CLI:

```text
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
```

Windows CP932 boundary を実 subprocess smoke で検出し、script entry point の stdout / stderr を UTF-8 化した。

repository 全体:

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109

Phase 108 後の 運用監査 から開始し、生成元問い合わせ の 利用者向け意味論 と 既知群の証明再生 を閉じた。

主要な流れ:

```text
既知群同一性
→ 証明由来の ambient fallback
→ indexed sigma 具体化
→ proof-scope 統合
→ qualified execution 境界監査
→ 既知群の証明再生
→ show-proof
→ statement 表示 coverage
→ 利用者向け表示順の確定
```

Toda Proposition 5.15:

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

concrete indexed 具体化 は \(n\ge 10\) に限定し、symbolic higher step を 直接 premise として保持する。

既知群の証明再生:

```text
generator
→ unique 既知群同一性 node
→ existing ProofStep
→ direct provenance
→ show-proof
```

qualified 定理実行:

```text
generator
→ 実行可能対象 resolver
→ qualified 定理適用
→ 有界実行
→ execute
```

確定した境界:

```text
show-proof != execute
候補番号 != 定理順位付け
concrete sigma_n specialization != 第3 qualified execution family
```

最終 repository 全体 regression:

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110

Phase 110 は 利用者向け数学演算問い合わせ の実需要監査から開始し、既存 repository / proof-scope にすでに表現されている数学的 演算事実 を直接検索・表示・証明再生 できる経路を追加した。

主要サブフェーズ:

```text
110-1:
利用者向け数学演算問い合わせ capability audit

110-2:
query 入力 / 構文境界監査

110-3:
既存 relation 検索設計

110-4:
最小演算問い合わせ実装境界監査

110-5:
最小演算問い合わせ core 実装

110-6:
演算問い合わせ CLI 統合

110-7:
演算問い合わせ結果の重複除去 / 表示優先順監査

110-8:
重複除去表示実装

110-9:
operation query 証明再生 / provenance detail audit

110-10:
operation query 証明再生 implementation

110-11:
証明再生 statement presentation audit

110-12:
証明再生 statement presentation implementation

110-13:
機能完了 / regression 監査
```

最小 query 文法:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

代表 CLI:

```text
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
```

代表結果:

\[
H(\nu')=\eta_5,
\qquad
H(\nu')=E^2\eta_3,
\]

\[
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
\]

\[
E\eta_2\nu'=0.
\]

operation query は evaluator ではない。

```text
検索 != 推論 != 評価
```

raw proof-scope 出現s は保持し、表示層 だけで 同一数学 statement を グループ化する。

```text
重複除去済み表示
!= provenance 削除
```

`query-proof` を追加。

```text
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 2
python main.py query-proof "E(eta_2 o nu_prime)"
python main.py query-proof "eta_2 o nu_prime" --fact 4
```

証明再生 root は 包含する定理 aggregate ではなく、選択された 事実自身の `ProofStep`。

\[
H(\nu')=\eta_5
\]

の 直接再生 は

\[
H(\nu')=E^2\eta_3,
\qquad
E^2\eta_3=\eta_5
\]

を表示する。

複数事実 のときは 暗黙の自動選択 を行わず `--fact N` を要求する。

証明再生 statement presentation では既知の意味論 を数学表示し、未知の aggregate は 生の Python repr ではなく 安全な型名 fallback にする。

代表:

\[
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
\]

\[
E^2\nu'\in2\iota_5\circ\pi_8^5,
\]

\[
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
\]

Phase 110 最終確認:

```text
python -m pytest -q
9055 passed in 455.09s (0:07:35)

git diff --check
clean
```

代表 smoke:

```text
query
query-proof
execute
show-proof
python main.py 5 3
```

すべて正常。

Phase 110 は完了。

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

現在機能 の確認では次を優先する。

```text
README.md
docs/design.md
docs/roadmap.md
docs/code_reference.md
docs/proof_records.md
```

次 Phase は Phase 110 の operation query / 証明再生 を前提に、CLI 全体の利用者視点での残課題と、次に実需要のある最小機能 を監査して開始する。
