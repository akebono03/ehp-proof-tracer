# R3-6 変更一覧

- 変更対象: `web_group_proof.py` の import 全文と `build_standard_web_group_proof_view()` 全文。
- 不変: `build_web_partial_group_proof_view()`、既存 Renderer、Search の数学的ロジック。
- 追加パラメータ: `citation_source="legacy"`（既定） / `"model"`（明示的）。
- `model` 指定時には同じ `RegistryBridgeResult` を Search と `build_linked_proof_narrative_model()` に使用する。
- `trace` の表示契約と従来の詳細証明を維持する。
- 追加テスト関数: `tests/test_phase168_r3_6_standard_web_entry.py` の4関数。import も全文収録。

`web_group_proof.py` およびテストファイルは ZIP に省略なしで全文収録。

## 実行

`python -m pytest -q phase168_r3_6_standard_web_entry/tests/test_phase168_r3_6_standard_web_entry.py`

## 完了条件

限定テスト4件の PASS、4群の診断実行、モデル指定時の π₄² の2文献保持。

## 次 Phase との境界

今回、既定経路の長文証明は変更しない。R3-7 以降で長文本文の各ステップと引用番号の対応を中間モデルへ移し、既定経路を切り替える。全体 pytest は Phase 168 終了時のみ。
