# Phase 169 R10E5-R2 — source anchor 修正

## 結果と原因

R10E5-R1 は HEAD / blob guard を通過したが、patch.py の置換アンカーが現行コードと一致せず、実装前に停止した。
実際の `shared_expansion_provider` は `expand_cited_stable_family(goal, tuple(available))` を呼ぶ。
旧パッチの `OLD` と `NEW` は第二引数 `tuple(available)` を省略していた。

## 変更対象

- `phase169_r10e5_composite_generator_image/patch.py` のモジュール定数 `OLD`, `NEW` を正しい既存呼び出しに修正。
- `phase169_r10e5_composite_generator_image/tests/test_r10e5r2_patch_anchor.py` にテスト2件追加（import とテスト関数は同ファイル全文に収録）。

## 非変更対象

- 既存本番 `phase165_r52_r9_shared_math.py` は ZIP 展開で直接変更しない（既存 run.ps1 がガード付きで適用）。
- 合成懸垂の数学的規則 `rule.py`、既存テスト、run.ps1、README 等は変更しない。

## 検証と完了条件

ZIP 整合性、構文、アンカーの単独変換と二重適用拒否を事前に確認。
実環境では run.ps1 が従来の限定 pytest と監査を実行する。
`R10E5_LIMITED_TESTS_AND_AUDIT=PASS` および `R10E5R1_HEAD_GUARD_RESULT=PASS` を必要とする。
全体 pytest は Phase 169 最終時のみ実施。
