# Phase 165 R14-R6 — 一般同型規則

変更対象（新規ファイル）:
- `phase165_r14_r6_generic_iso.py` — `MapInjective`, `MapSurjective`, `MapIsomorphism`, `GeneratorImage` クラス全文と `map_isomorphism_rule()`, `free_cyclic_transport_rule()`, `expand_generic_iso_goal()`, `audit_generic_iso()` 関数全文
- `test_phase165_r14_r6_generic_iso.py` — 関連テスト関数全文
- `audit.py`, `run.ps1`, `README.md`

既存ソースは編集しません。R14-R6 は数学的推論規則を一般形で追加し、用意された型付き前提から ProofStep を組み立てるテストを追加します。テストの GIVEN 前提は検証用 fixture であり、Toda の命題を認証しません。

`π₃² = ℤ{η₂}` の根から同型写像そのものを発見する規則はまだありません。引き続き `UNRESOLVED` とし、旧 Narrative へ戻しません。

実行: `run.ps1` は R14-R6 の追加テストのみと診断を実施。全体 pytest は Phase 終了時のみ。

完了条件: injective + surjective -> isomorphism と、同型 + 自由巡回群構造 + 生成元の像 -> 群構造、両規則が型付き推論としてテストされること。別の写像や生成元を混ぜた推論が拒否されること。

次段階: EHP 完全列から単射・全射を導く登録済み前提、及び群構造 Goal から写像候補を選択する汎用探索の接続。
