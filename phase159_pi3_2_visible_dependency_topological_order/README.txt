Phase 159 pi3_2 visible dependency topological ordering

目的:
- 個別文を hard-code で移動する repair を追加しない。
- 既存 proof presentation の direct dependency edge を使う。
- 同一 argument の visible ProofStep 同士だけを対象にする。
- dependency edge がない文同士は既存順序を維持する stable topological sort にする。
- cycle や表示文の一意対応が取れない場合は安全側として既存順序を保持する。

変更対象:
1. toda_group_proof_narrative_contribution_renderer.py
   - 新規:
     order_toda_group_proof_narrative_visible_step_dependencies()
   - 接続:
     render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

2. tests/test_phase159_pi3_2_visible_dependency_topological_order.py
   - pi_3^2 の dependency order を focused test で確認する。

Phase 境界:
- renderer 全体の再設計はしない。
- proof graph に存在しない依存関係を推測しない。
- statement type の固定優先順位は導入しない。
- 全体テストは実行しない。
