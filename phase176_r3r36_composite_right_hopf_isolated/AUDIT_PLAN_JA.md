# Phase 176 R3R36 — 監査・実装計画

## 実装前に確認したコードとテスト

GitHub `akebono03/ehp-proof-tracer` の `develop` にある以下を確認した。

- `phase171_r2h_prop22_cited_hopf/source.py`：`_formula_parts()` は懸垂前の右因子を `HomotopyElement` に限定。
- `phase176_r3r30_generic_hopf_substitution_isolated/source.py`：一般的な右 Hopf 値代入と2つの独立した前提。
- `phase176_r3r34_composite_suspension_isolated/source.py`：証明済み `GeneratorImage` を合成懸垂の等式にする独立規則。
- `phase165_r52_r9_shared_math.py`：R3R31 と R3R35 の公開接続位置。
- `phase174_r3_r7_r7_composite_zero_audit/rule.py`：合成の型付き始域・終域検査 `expression_endpoints()`。
- `phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py`、`phase176_r3r30_generic_hopf_substitution_isolated/tests/test_source.py`、`phase176_r3r34_composite_suspension_isolated/tests/test_source.py`。

ユーザー環境で R3R35 の限定 pytest 13 件の成功を確認済み。ただし共有 DFS における Citation / Source-order Gate は未検証。

## 変更対象と追加位置

既存のファイル・クラス・関数・import は変更しない。**新規ディレクトリ** `phase176_r3r36_composite_right_hopf_isolated/` のみ追加する。

- `source.py`：`COMPOSITE_FORMULA_RULE_NAME`、`COMPOSITE_SUBSTITUTION_RULE_NAME`、`composite_right_formula_parts()`、`composite_right_formula_rule()`、`composite_hopf_substitution_inputs()`、`composite_hopf_substitution_rule()`、`expand_cited_composite_right_hopf()` をこの順に追加。
- `audit.py`：`run_git()`、`preflight()`、`probe()`、`report_path()`、`execute()`、`main()` を追加。
- `run.ps1`：DryRun、監査、4つの限定 pytest モジュールの起動を追加。
- `tests/test_source.py`：必要な import と7件のテスト関数、補助関数 `elements()` および `typed_goals()` を追加。
- `README.md`：全文新規（英語）。`AUDIT_PLAN_JA.md` と `CODE_FULL_JA.md`：全文新規（日本語）。

すべての追加ファイルの全文を `CODE_FULL_JA.md` に記録する。独立規則は既存単体規則の代替ではない。

## 数学的境界

Toda Proposition 2.2 を使って、

$$H(\nu'\circ E(\eta_5\eta_6))=H(\nu')\circ E(\eta_5\eta_6)$$

という型付きの公式候補を、出典付きの `TodaProp22RightFormula` を必要条件として生成する。

Hopf 値の代入では、独立した $H(\nu')=\eta_5$ の検証済み前提を要求する。

$$H(\nu'\circ E(\eta_5\eta_6))=\eta_5\circ E(\eta_5\eta_6)$$

ここでの局所的な推論再生は、群構造や $H(\nu'\eta_6^2)=4\nu_5$ の証明完了を意味しない。合成懸垂の等式を H の引数と値に移送し、Toda (5.5) に接続する義務は次段階に残す。

## 完了条件

1. DryRun が Source Guard とブランチ検査を通過する。
2. 既存の SOURCE アーカイブや GIVEN を改変しない。
3. 合成右因子に対して公式の候補1件と、2前提の代入候補1件を生成する。
4. 型不一致・出典欠落・偽の前提を拒否する。
5. 新規限定 pytest および関連する既存限定 pytest が成功する。
6. 全体 pytest は実行しない。

次の R3R37 では共有 Provider への公開接続を監査する。直接の群構造登録は禁止。
