# R27 変更記録

- 既存実装 `toda_rules.py` の2つの $$pi_3^2$ 専用規則を削除。
- `toda_upstream_bootstrap.py` および `probes/probe_phase49_capabilities.py` の専用規則の import／呼び出しを削除。
- `standard_production_applicability_catalog.py` の該当2件の登録を削除。
- `toda_prop56_zero_bootstrap.py` の `_build_prop51_step()` において $H(\eta_2)=\iota_3$ の取得を、既存の Phase 50 の前提へ切り替える。新たな `GIVEN` は作成しない。
- 一般規則・型付き命題台帳は変更しない。
- テスト: 同梱の `test_retirement.py` と `test_phase165_r52_r9_shared_math.py` のみ。全体テストは未実施。

## 完了条件

旧2規則の定義・呼び出し・Catalog 登録が無くなり、共通探索と公開 Narrative の対象テストが全件 PASS すること。

## 次 Phase との境界

旧 Bootstrap 全体や他のホモトピー群専用規則の削除、Phase 50 文献出典の独立検証は本作業に含まない。
