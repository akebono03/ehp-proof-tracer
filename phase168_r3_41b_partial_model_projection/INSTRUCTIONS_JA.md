# Phase 168 R3-41B — 未完成証明の共通 Narrative Model 接続

## 現行コードとテストの確認

GitHub `akebono03/ehp-proof-tracer` の `develop` にある次のファイルと関連テストを確認した。

- `phase168_r3_3_proof_narrative_model.py`
- `phase168_r3_5_model_renderer.py`
- `phase168_r3_12_body_binding.py`
- `phase165_r52_partial_proof.py`
- `phase165_r52_r3_web_adapter.py`
- `phase168_r3_3_narrative_model/tests/test_phase168_r3_3_proof_narrative_model.py`
- `phase168_r3_12_body_binding/tests/test_phase168_r3_12_body_binding.py`
- `phase168_r3_5_model_web_boundary/tests/test_phase168_r3_5_model_web_boundary.py`
- `test_phase165_r52_r3_web_adapter.py`

## 変更対象

1. `phase168_r3_3_proof_narrative_model.py`
   - import 全文を `full_imports/phase168_r3_3_proof_narrative_model_IMPORTS.py` に収録。
   - `ProofNarrativeModel` クラス全文を置換し、末尾にデフォルト値付きの `status`, `target`, `open_goals`, `diagnostics` を追加。
   - `build_proof_narrative_model()` 関数全文を置換し、`PartialProofResult` の既存値をコピー。
2. `phase168_r3_5_model_renderer.py`
   - import 変更なし。既存 import 全文を `full_imports/phase168_r3_5_model_renderer_IMPORTS.py` に収録。
   - `render_model_backed_narrative_markdown()` 関数全文を置換。
   - 完成証明の文章経路は変更せず、未完成状態に限定して状態、確認済みステップ、未解決 Goal、診断を表示。
3. 追加テスト `tests/test_phase168_r3_41b_partial_model_projection.py`
   - テスト関数全文と import を同ファイルに収録。

全関数・全クラスの置換単位を `full_functions` に収録。適用後の実装ファイル全文は `full_files` に出力する。

## PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41b_partial_model_projection.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41b_partial_model_projection\run.ps1"
```

## 検証と完了条件

- 新規限定テストと既存関連テストが PASS。
- `NOT_SEARCHED`, `PARTIAL`, `SEARCH_FAILED` の状態・Goal・診断・観測済みステップを共通 Renderer が保持。
- 出典未確認の `result.references` を Reference として付与しない。
- 未完成状態で `□` を出さない。
- 完成した4群（π₃²、π₄³、π₅⁴、π₆⁵）の Narrative が変更前後でバイト単位完全一致。
- 旧 fallback、明示 `legacy` 経路、`after_indices` は維持。
- 全体 pytest は Phase 168 終了時のみ実行。

## 次工程との境界

R3-41B は Model と Renderer の未完成状態対応だけ。Web の既定経路切り替え・旧 fallback 撤去・推論規則追加は行わない。正常終了後に `output/review_bundle.zip` を提供し、次の切り替え判断へ進む。
