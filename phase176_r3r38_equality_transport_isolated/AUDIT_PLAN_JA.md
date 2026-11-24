# Phase 176 R3R38 — 等式移送の監査計画

## 目的

R3R35 で公開接続した合成懸垂の等式と、R3R37 で公開接続した Toda Proposition 2.2 の合成右因子の代入式を、**既存の一般推論規則だけで**局所的に接続する。

証明すべき出発点は以下の二つの独立した推論済み Relation である。

$$
H(\alpha\circ E\beta)=\delta\circ E\beta,
\qquad E\beta=\gamma.
$$

既存の等式保存規則と推移律から次の Relation を得る。

$$
H(\alpha\circ\gamma)=\delta\circ\gamma.
$$

型検査では、$\alpha,\delta$ と $\beta,\gamma$ の source/target を検証し、Hopf 像の標的次元も確認する。文字列だけによる別名の同一視はしない。

## 対象

既存ファイル・クラス・関数の変更は**なし**。今回の追加位置はプロジェクトルート直下の新規ディレクトリ `phase176_r3r38_equality_transport_isolated`。

追加するもの：

- `source.py::right_hopf_transport_inputs()`：型付き二前提を生成。
- `source.py::_derive_existing_step()`：既存推論規則を1回再生、結果を検証。
- `source.py::replay_right_hopf_transport()`：既存6規則を順に適用。
- `audit.py::source_guard()`：既存公開接続と import 対象の現状を検証。
- `audit.py::probe()`：Source-first 選別済みの GIVEN と公開候補から局所 ProofStep を再生。
- `audit.py::main()`：DryRun・報告ファイル出力。
- `tests/test_source.py`：一般化・拒否条件・前提保全の限定テスト。

## 実行順

1. DryRun で既存公開接続のアンカーと対象ファイル構文を監査する。
2. 本実行で登録済み根 Goal に対する screened（出典選別済み）Context を取得する。
3. Toda Proposition 2.2 の GIVEN、$H(\nu')=\eta_5$ の GIVEN、合成懸垂像の独立推論を取得する。
4. R3R37 の代入式と R3R35 の懸垂等式を別々に推論再生する。
5. 左合成の等式保存、Hopf による等式保存、対称律、左合成の等式保存、推移律、推移律の合計6段を再生する。
6. 限定 pytest および `git diff --check` を実施する。

## 完了条件

DryRun、本実行、限定 pytest のすべてが PASS。新規 GIVEN と新規数学規則は0件。以前の公開 Provider は未変更。すべての入力に独立した推論の ProofStep が存在する。

## 未完了・次の境界

これは **isolated local replay** であり、共有 DFS の引用・出典順序 Gate を検証したものではない。$\eta_5\eta_6\eta_7=4\nu_5$ の型付き等式、結合律による括弧の統一、Hopf 像の根 Goal と群構造の根 Goal の証明は対象外である。

README は英語、監査計画とコード全文は日本語で記録する。全体 pytest は Phase 176 終了時のみ実施する。
