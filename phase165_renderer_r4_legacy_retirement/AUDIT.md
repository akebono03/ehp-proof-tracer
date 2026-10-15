# Phase 165 R4 — 監査と移行範囲

## R1 実測

- Python ファイル：1,236、本番コード：428
- 旧 Generic モジュールへの静的 import：40件
- 正規 Narrative Renderer の重複公開定義：2個（11104行、11766行、R1 時点）
- 旧 Generic 実装ファイルは削除済みだが、互換パッケージが残存

## R4 の対象

- `toda_group_proof_narrative_renderer.py`：先行公開定義を `_phase160_r7_pre_transport_narrative` に変更し、既存 `_phase160_r7_previous_public_narrative_renderer` の参照先だけ更新。後行の公開定義は維持。
- 旧 Generic 名を import する各ファイル：低レベル描画関数は `toda_group_proof_narrative_shared_components` に、公開部分証明関数は正規 Renderer に接続。
- `toda_group_proof_generic_narrative_renderer/__init__.py`：依存の消滅を検査後、互換パッケージを削除。
- 関連テスト内の旧 import も移行する。テスト内容そのものは書き換えない。

## 境界

- `toda_group_proof_narrative_shared_components.py` の内容、推論規則、ProofStep、Backward Search、Web 接続は変更しない。
- 63個の名称一致ファイルを一律削除することはしない。数式描画や Reference/Reason の補助モジュールは引き続き必要。
- 実行時の動的 import、実行されない過去のコード経路までは静的監査で完全証明できない。限定回帰と Markdown 完全一致で主要経路を検査。
- 全体 pytest は Phase 165 終了時のみ。

## R4 完了条件

1. 静的旧 import が 0。
2. 正規公開 `render_toda_group_proof_narrative_markdown` 定義が 1。
3. 旧互換パッケージが削除される。
4. 完成・未完成 Markdown が実行前と完全一致。
5. 限定 pytest が成功。
