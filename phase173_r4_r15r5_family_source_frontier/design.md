# Phase 173 R4-R15R5：未解決懸垂系列の文献位置監査

## 目的

R4-R15R4 の実測値により、$\pi_{35}^{4}$ の左側（$\pi_{34}^{3}$ 由来）の記名生成元像候補は4件である。既存の出典付き推論で再構成できたのは1件で、残る3件に出典不足がある。監査で現れた系列 ID は56（$\bar\kappa$）および88（$\delta$）である。今回の目的は、新たな数学的等式を宣言することではなく、これらの出典候補の所在と未解決の因子を記録することである。

## 現在の理論的前提

Toda Proposition 4.4 と $H(\nu_4)=\iota_7$ から、$i\ge 7$ の対象について $\pi_i^4\cong\pi_{i-1}^3\oplus\pi_i^7$ を利用する。$i=35$ の抽象群の群構造は、先行2群が $(\mathbb Z/2)^4$ であることから $(\mathbb Z/2)^8$ となる。しかし個々の生成元との等式は独立に確認する必要がある。

`HyoujiGen.csv` の `kinds=0` や系列の記法は、出典付きの定義とは異なる。特に $\Delta$ と $\delta$ の表記上の対応も、未証明の等式を認可する理由とはしない。

## 変更対象・追加位置

既存のファイル、クラス、関数、メソッド、import は変更しない。リポジトリ直下に新規 `phase173_r4_r15r5_family_source_frontier/` ディレクトリを配置する。

- `source_scan.py`：`scan_text` と `scan_adopted_toda_sources` を新規追加。TeX の候補文字列を検索する。候補を固定命題に昇格しない。
- `audit.py`：`inspect_family_source_frontier` と `main` を新規追加。前回の ProofStep 再構成結果、因子別の未解決条件、テキスト候補を関連付ける。
- `preflight.py`：`git`、`is_allowed_committed`、`normalized_sha256`、`verify_source_head`、`main` を新規追加。Git と以前のレビュー済みコードを照合する。
- `tests/test_static.py`、`tests/test_scan.py`、`tests/test_integration.py`：新規の限定テストを追加。
- `run.ps1`：DryRun → 限定 pytest → 監査 JSON 出力。既存プログラムの書き換えは行わない。

コードとテストは `SOURCE_CODE.md` に全文を収録する。

## 監査上の区別

1. `DB_ONLY`：CSV に系列の記号が登録されている。
2. `TEXT_HIT_UNREVIEWED`：収録 TeX に候補となる文字列が見つかった。検証済み定義とは限らない。
3. `CITED_DEFINITION`：既存の出典付き定義レジストリで明示的に承認されている。
4. `PROOF_REPLAYED`：既存の推論エンジンが前提と推論を独立に再生できた。

この段階で3、4の新規登録は一切行わない。候補文字列が見つかった場合でも、文脈・数式・出典・出版順を人手監査する必要がある。

## テストと完了条件

作成環境で静的・分離テスト12件を実行する。通常実行では R15R5 の実リポジトリ検査と過去の限定テストを実行する。全体 pytest は Phase 終了時のみ。

- `HEAD_LINEAGE=PASS` と `SOURCE_GUARD=PASS`。
- $k=31$ の候補4件、出典付き再構成1件、未解決3件。
- ID 56・88 の未承認状態を維持。
- 出典候補を記録しても、追加の `GIVEN`・`ProofStep`・公開完成は発生しない。
- `family_source_frontier_report.json` を生成する。

## 次 Phase との境界

R4-R15R6 では R15R5 の候補箇所の原典・周辺証明を個別に読み、正確な出典付き懸垂関係がある場合だけ、その根拠に沿って汎用推論に登録する。候補がなければ、未解決状態を継続して別の同型や関係を検討する。今回の監査段階では数学的な新規完成証明を宣言しない。
