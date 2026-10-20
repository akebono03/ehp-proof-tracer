# Phase 166 R3-B：失敗テスト2件の修正

## 変更対象

- `tests/test_phase166_r3b_publication_order_binding.py`
  - `test_only_exact_reference_ids_are_connected_no_locator_fallback()` 全体置換
  - `test_manifest_reference_id_change_does_not_silently_match_by_locator()` 全体置換

`import` は変更しない。既存の実装ファイル、クラス、関数、証明探索、Renderer は変更しない。追加したクラス・関数はない。テストファイルは ZIP に省略なしの全文を同梱する。

## 修正理由

- 現行 `build_registry_bridge()` に `fact:` かつ `Proposition 5.1` の参照が存在するとは限らない。実際に存在する `toda:` 参照を基準に、同じ locator で異なる ID の検証用参照を追加する。
- manifest の文献 ID を別 ID に改名しても、108件の位置列は変わらないため、エラーを要求するのは誤り。元 ID の型付き参照には位置が付かず、locator による代替照合も行われないことを検証する。

## 検証

`run.ps1` で対象限定 pytest を実行する。全体 pytest は Phase 166 完了時に限る。こちらの作成環境では構文検査だけを行い、Windows の現行リポジトリでの pytest 成功は未確認。

## 完了条件と次 Phase

17件の限定テスト PASS と監査の PASS。R3-C までは証明探索に掲載順を適用しない。
