# Phase 169 R3U — 変更対象とコード全文

## 本番コード

`phase165_r14_r5_ehp_connection.py`:

- `expand_cited_ehp_terminal_goal()` — 全体を置換。実装全文は `full_functions/expand_cited_ehp_terminal_goal_FULL.py`。
- トップレベルの import は変更しない。追加の import は関数内部に全て記述してある。
- 他の既存関数、クラス、数学的推論規則を変更しない。

## 関連する既存テスト

次の関連テスト3ファイルについて同じ4関数を更新する。

- `phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py`

更新する関数:

- `test_r3i_only_exact_screened_claims_propose_cited_rules()`
- `test_r3i_derived_terminal_steps_have_exact_cited_ancestors()`
- `test_r3i_historical_inference_only_rules_remain_intact()`
- `test_r3i_real_recursive_proof_of_terminal_goals()`

変更後の各テスト関数全文は `full_functions/` に同名の `*_FULL.py` として収録。トップレベルの import は変更しない。4関数とも従来の `(Proposition 5.1)` のみを前提とする検査を `(Proposition 5.1, (5.1) の導出結果)` に修正する。

## 新規テスト・監査

`tests/test_phase169_r3u_delta_diagonal_dependency.py` — 5テスト関数全文と必要な import を収録。`audit.py` は実際の $\pi_5^3$ の証明を再構築する監査専用ファイル。

インストール時、変更前・変更後の本番ファイルおよび既存テストファイルは `output` に全文出力する。導出後は通常の Proof Narrative Model / 共通 Renderer を通るため、表示用の追加分岐は不要。
