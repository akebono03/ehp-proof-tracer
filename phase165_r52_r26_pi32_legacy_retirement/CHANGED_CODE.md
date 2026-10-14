# R26 変更一覧

- `toda_rules.py`: `toda_pi3_2_free_cyclic_generator_inference_rule` の関数定義全体を削除。
- `toda_upstream_bootstrap.py`: 旧専用規則の import と `_build_phase49_result` 内の旧規則呼び出しを削除。
- `probes/probe_phase49_capabilities.py`: 同 import と旧規則呼び出しを削除。
- Phase 165 共通探索に変更なし。関連一般推論規則に変更なし。

実際の既存関数全文や import 全文はローカルリポジトリのバージョンが基準となります。インストーラは AST で厳密に対象を限定し、それ以外は変更しません。バックアップが自動生成されます。
