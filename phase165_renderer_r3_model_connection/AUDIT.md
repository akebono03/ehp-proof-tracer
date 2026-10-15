# Phase 165 Renderer R3 監査・変更境界

## 事前確認

- GitHub `akebono03/ehp-proof-tracer` にある `phase165_r52_partial_proof.py`、`toda_group_proof_narrative_renderer.py`、`phase165_r56_presentation_adapter.py`、`toda_group_proof_presentation.py`、既存の関連テストを確認した。
- 直近のローカル実行結果から、R2 `phase165_renderer_narrative_model.py` が導入済みであることを確認した。
- R1 監査では正規 Renderer 内の同名関数二重定義と旧 Generic 名の依存40件を検出した。
- 復旧済み完成証明は `phase165_r56_presentation_adapter` の特別分岐を含む。その数学的妥当性・分岐動作を R3 で変更しない。
- GitHub はローカルの直近 ZIP 導入状態と一致しないため、インストーラーは現地コードの署名を照合して不一致では停止する。

## 変更ファイル・関数

1. `toda_group_proof_narrative_renderer.py`：ファイル末尾へ新規 `render_narrative_proof_model(model)` を追加。import 節は変更しない。
2. `phase165_r52_partial_proof.py`：`render_partial_proof_markdown(result)` 全体を置換。import 節は変更しない。
3. 追加パッケージ：`install.py`、`restore.py`、`snapshot.py`、`test_r3.py`、`run.ps1`、文書類。

## R3 完了条件

- R2 モデルから正規 Renderer の共通 Dispatcher を呼べる。
- 完成証明・未完成証明の公開入口がモデルを通る。
- `pi3_2` 完成、`pi4_3` 未完成の公開 Markdown と完成 Adapter 出力が変更前と完全一致する。
- 限定 pytest 7件が成功する。
- 既存 ProofStep、Reference、Backward Search に変更がない。

## R4 と区別する作業

- 同名 `render_toda_group_proof_narrative_markdown` の重複定義の解消。
- 旧 Generic import 40件の移行および互換パッケージ削除。
- 各歴史的 renderer helper と outline/trace の廃止可否。

全体 pytest は Phase 165 完了時のみ実施する。
