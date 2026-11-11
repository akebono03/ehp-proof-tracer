# Phase 174 R60 — Reference 所有関係監査

## 現行コードと関連テスト

GitHub `akebono03/ehp-proof-tracer` `develop` HEAD `82d725d8649cd6307c2abd67024e3ef4f3cddfe2` を確認した。

- `phase168_r3_3_proof_narrative_model.py`：Reference と ProofStep の索引対応を生成する。
- `phase168_r3_12_body_binding.py`：本文行と出典索引の双方向一致を検証する。
- `phase168_r3_5_model_renderer.py`：出典表示の共通処理と残存する局所的な引用選択。
- `phase168_r3_37c_reference_projection.py`：出典に対応する文献本文の投影。
- `phase174_r3_r7_r56_cyclic_generator_bridge/audit.py`、`phase174_r3_r7_r57_narrative_source_cleanup/audit.py`：対象2群の独立証明および Reference 数を検証する。
- 関連テスト：`phase168_r3_12_testfix/probe.py`、`phase174_r3_r7_r57_narrative_source_cleanup/tests/test_static.py`、R59 の限定テスト。

## 今回の変更対象

Production ファイル・クラス・関数・import に変更なし。以下を新規作成。

- `phase174_r3_r7_r60_reference_ownership_audit/audit.py`：Source Guard、Citation 所有関係監査、公開証明回帰監査を行う新規関数群。
- `phase174_r3_r7_r60_reference_ownership_audit/tests/test_audit.py`：監査用テスト関数を新規追加。
- 同ディレクトリの `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`、`__init__.py`。

各関数の完全実装は ZIP 内の `audit.py` および `tests/test_audit.py` に収録し、`CODE_FULL_JA.md` にも全文掲載する。省略コードなし。

## 完了条件

1. Source Guard がレビュー済み Git blob 6件とローカル HEAD を検証し PASS。
2. DryRun と限定 pytest が PASS。全体 pytest は実行しない。
3. `(n,k)=(6,5)` は 7 Reference、`(7,5)` は 3 Reference を維持する。
4. Citation が root の証明木内の実際の ProofStep と双方向対応し、無関係な証明ステップへ紐付かない。
5. 文献の見出し番号が Model と一致し、`π_11^6` に Proposition 2.7 があり、`π_12^7` には存在しない。
6. 新 GIVEN・新数学規則・本体コード変更 0。

## 次段階との境界

本監査は **Reference 所有関係の整合性** を確認する。Renderer 内に残る `cited_general_ancestor_numbers`、`direct_given_premise_citation_numbers`、`single_source_ancestor_numbers` などの分散した出典選択をこの段階で書き換えない。本文ごとの引用の必要性・十分性を全面的に検証したという結論も出さない。今後の一般化実装は別の監査と変更 Phase に分離する。
