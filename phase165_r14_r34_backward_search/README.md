# Phase 165 R14-R34 — Registered backward search

## 変更対象
- 新規 `phase165_r14_r34_backward_search.py`：`pi32_goal`, `_hopf_map`, `phase165_r34_expansions`, `trace_goal_frontier`, `audit_r34` （import・関数すべて全文収録）
- 新規 `test_phase165_r14_r34_backward_search.py`：6テスト全文
- 新規 `audit.py`, `run.ps1`。既存コードは変更しない。

## 方針
R33 で作った完成済み ProofStep を再生せず、最終目標から逆向きの `GoalExpansion` を供給して既存の `reconstruct_registered_goal` に渡す。`reverse_free_cyclic_transport_rule` と一般的な同型・EHP などの規則を再利用する。出典資格がない場合は必ず `RegisteredGoalUnresolved` として止める。

## 完了条件
対象6テストが成功し、逆向きの依存関係が得られること。117件の元マニフェストを保持し、未認証の `GIVEN` を作らず、認証されたかのような本番証明を生成しないこと。

## 次工程との境界
採用 TeX で作成できた R33 の試験的導出と、厳密に登録される Leaf ProofStep を接続するための既存引用資格の解消が必要。全体 pytest は Phase 165 終了時のみ。
