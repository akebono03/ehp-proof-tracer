# Phase 165 R10 の変更

- 新規 `phase165_r10_rule_registry.py`：`RegisteredInferenceRule`、`RuleRegistrySnapshot`、`build_rule_registry()` を追加。Rule ID は `module.factory` とする。
- 既存 `phase165_r8_rule_provider.py`：`discover_inference_rules()` の関数全体を台帳への委譲に置換。import 節は変更しない。
- 新規 `phase165_rule_registry_r10/test_r10.py`：3テスト追加。
- R57 の接続コードは既存の公開 API 経由で台帳を使用するため変更しない。
- 全体 pytest は Phase 165 終了まで実行しない。
- `module.factory` の一意性は確保するが、数学的同値性の自動検証は行わない。
