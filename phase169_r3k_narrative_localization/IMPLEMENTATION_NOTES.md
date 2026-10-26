# Phase 169 R3K — 実装境界と検証

## 変更対象

- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` 全体。全文は適用後 `output/render_model_backed_narrative_markdown.full.py` に出力する。
- 新規 `phase169_r3k_narrative_projection.py` に `project_proven_map_property()` と `duplicate_group_relation_notice()` を追加する。
- 新規 `tests/test_phase169_r3k_narrative_localization.py` に限定検証関数を追加する。
- 本番 import 節、他のクラス・関数、文献台帳、ProofStep、EHP 規則は変更しない。

## 成果と保留

- 証明済み Step の LaTeX `\text{ is surjective}` 等を日本語文章化する。数式部分と出典対応はそのまま。
- 同一群構造の繰り返しの数式を省く。2件目が出典を持つ場合は出典を短文として表示し、Reference 対応を維持。
- `Chapter V, i)` の Reference と、型付き導出が未確認の $E(\eta_2^2)=\eta_3^2$ の追記は今回行わない。別途証明祖先を監査する。
- $\pi_3^2$, $\pi_4^3$, $\pi_5^4$ の現行 frozen criteria の限定テストを実行する。

## 完了条件

限定 pytest PASS、$\pi_5^3$ の探索 `complete`、英語文0、$\pi_4^2$ の表記1回、引用カバレッジ PASS、両 EHP 終端 Step の維持。全体 pytest は Phase 169 の最終段階のみ。
