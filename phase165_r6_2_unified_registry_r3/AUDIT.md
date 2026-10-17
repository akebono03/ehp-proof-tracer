# Phase 165 R6-2：統一規則台帳 R3

## このパッケージで実施する範囲

R8 の9モジュール以外に存在する `expand_` 系関数を棚卸しし、`shared_expansion_provider` 内の Provider 参照箇所と別々に記録する。名前が似ているという理由だけで `InferenceRule` と認定しない。

## 変更対象

- 新規 `r3_inventory.py`：`dotted`、`read_source`、`find_shared_providers`、`discover_factories`、`discover_other_provider_functions`、`audit`、`render`、`main`
- 新規 `test_r3_inventory.py`：6テスト
- 新規 `run.ps1`、`README.md`、`AUDIT.md`

本番ソースと既存テストは変更しない。型付き証人を自動生成しない。

## 完了条件と次段階

R8以外の接続箇所と未接続候補を一覧化する。R3 の実際の統一登録・接続は、各候補の契約・適用条件・証人の検証後のサブフェーズで行う。静的参照を実行成功と扱わない。全体 pytest は Phase 末尾まで実行しない。
