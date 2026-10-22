# Phase 168 R2-8⑤ 逆向き証明探索接続監査

## 変更対象

- 新規: `phase168_r2_8_5_search_connection_audit/audit.py`（`summarize_result`, `inspect_case`, `main`）
- 新規: `phase168_r2_8_5_search_connection_audit/tests/test_phase168_r2_8_5_search_connection.py`（4関数）
- 新規: `run.ps1`, `README.md`, `AUDIT.md`

既存の本体コード、命題台帳、証明規則、出典順序を変更しない。

## 現行コードの確認

GitHub `akebono03/ehp-proof-tracer` の `develop` で `phase165_r55_nk_only_goal.py`, `phase165_r52_partial_proof.py`, `phase168_r2_5_prop53_audit/audit.py`, `phase166_r3t_goal_source_binding/goal_source.py`, `phase165_r57_r8_eta_specialization.py` と R2-8①のテストを確認した。

## 記録内容

引用 ID、引用先 locator、publication_position、component_position、`screen_shared_proof_context` の ProofStepLink、自己参照の有無、`search_group_from_registered_goal` の status、proven_steps 数、open_goals、diagnostics、references を9件について記録する。

`SEARCH_COMPLETE` は実際の結果からのみ記録する。単なる引用解決から証明完成を推定しない。監査中の例外は対象ケース別に記録し、他のケースの結果を失わない。

## 実行する pytest

`tests/test_phase168_r2_8_5_search_connection.py` 4件と既存 R2-8① `tests/test_audit.py` 4件。

## 完了条件と境界

9件の探索状態を報告できること。R2-8⑤では数学的な結論追加、証明規則追加、GIVEN 注入、表示変更を行わない。次段階は報告で特定した探索上の未解決原因のみを扱う。全体 pytest は Phase 168 終了時に限る。
