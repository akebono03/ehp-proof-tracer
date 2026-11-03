# Phase 173 R4-R15R6 設計書

## 1. 監査結果と問題の切り分け

直前の R15R5 は限定 pytest 43件 PASS、$k=31$ で生成元像候補4件のうち出典付き再構成1件、未解決3件を報告した。欠けている系列の ID は56（$\bar\kappa$）および88（$\delta$）。Toda の登録された TeX に対する R15R5 の正規表現検索は0件だったが、これは文献に根拠が存在しないことを意味しない。

今回の目的は、出典不明の記名生成元像を証明したと装うことなく、Proposition 4.4 の抽象群への一般的な帰結を **独立した型付き結論** として表現できるようにすることである。

## 2. 数学的な一般規則

Toda Proposition 4.4 を $n=4$, $\alpha=\nu_4$ に特殊化する。

$$
\pi_{k+4}^{4}\cong\pi_{k+3}^{3}\oplus\pi_{k+4}^{7}.
$$

この特殊化には $H(\nu_4)=\iota_7$ が必要であり、既存 Lemma 5.4 の型付き推論を利用する。帰納的に採用される2つの先行 DB 群は、前提として明示し、文献による独立証明だと称さない。

得られる結論 `TodaProp44AbstractGroupResult` には、対象の `TodaPrimaryGroup` と、巡回群の位数からなる不変量だけを保持する。生成元の名前は保持しない。$k=31$ の場合、抽象的には $\bigoplus_{j=1}^8\mathbb Z/2$ となる。

## 3. 変更対象・追加位置

既存ファイル、既存クラス、既存関数、既存 import に変更はない。新規ディレクトリ `phase173_r4_r15r6_abstract_toda44_rule/` に下記を追加する。

- `abstract_rule.py`: クラス `TodaProp44AbstractGroupResult`、関数 `canonical_abstract_result`、`abstract_toda44_rule`、`expand_abstract_toda44`。
- `audit.py`: 関数 `inspect_k`、`main`。監査 JSON と識別用ログを出力する。
- `preflight.py`: Git による同一 HEAD、reviewed blob、直前 ZIP の内容検証。
- `run.ps1`: DryRun と限定 pytest のみ実施する。
- `tests/test_static.py`, `tests/test_integration.py`: それぞれ独立テストと型付き推論の限定テスト。

## 4. 出典と安全性の条件

`abstract_toda44_rule` は下記4前提を要求する。

1. **GIVEN**: 出典を審査済みの `TodaProp44UniversalStatement`。
2. 先行群 $\pi_{k+3}^3$ の `verified_db_step`。
3. 先行群 $\pi_{k+4}^7$ の `verified_db_step`。
4. **INFERENCE**: `TodaLemma54TypedSource` に由来する $H(\nu_4)=\iota_7$。

`expand_abstract_toda44` は出典審査済み claim の集合を引数に取り、条件の一致する場合だけ探索候補を返す。候補を得ることは、その4前提が実際の公開探索で満たされたことを意味しない。

今回の独立テストの `GIVEN` は **規則の安全契約のテスト専用** であり、公開証明の出典として採用しない。

## 5. 完了条件

- $k=31$ を含む任意の登録済み $k\ge3$ で、一般同型の抽象群結論を一貫して構成できる。
- $k=31$ は8つの位数2の巡回成分、`source_screened_rule_proposals=1`。
- `checked_general_inputs` は $k=31$ で依然不成立。記名生成元の未証明等式を採用しない。
- 型付き規則の4前提について推論エンジンの再生テスト PASS、偽造 DB／不正順序／不足した出典は拒否。
- 既存 API・DB・Renderer・公開検索は無変更、全体 pytest は未実施。

## 6. 次 Phase との境界

R15R7 では **抽象結論の公開探索への source-first 接続**を検討する。対象 `Group query` の結論文へ変換する場合は、生成元名のない抽象表現が必要である。従来の記名生成元付き complete を、未証明のまま完成へ昇格してはならない。

ID56・88の出典不足は記名生成元に限る別の未解決課題として保持する。`development_log.md`、`proof_records.md` 等のプロジェクトルートの文書を今回変更することはない。
