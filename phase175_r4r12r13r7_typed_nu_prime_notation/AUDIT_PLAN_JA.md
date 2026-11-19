# R13R7 型付き ν′ 記法橋渡し

## 根拠

R13R6 では先行 DB の `IteratedSuspension(HomotopyElement(ν'), 1)` と Toda (5.8) の `Suspension(HomotopyElement(ν′))` が異なる実装表現であることを確認した。

## 変更範囲

- `phase175_r4r12r13r2_delta_injective_e_surjective/rule.py`: import 全文と `_linear_coordinates` 関数の置換。数学的な非零自由座標規則は維持。
- 新規 `notation.py`: 型・次数・生成元添字を完全確認した ν′ の文字表記と1回懸垂の同一記法だけを比較。
- 新規 `installer.py`, `audit.py`, `tests/test_r13r7_notation.py`, `run.ps1`。

## ガード

入力の非零自由座標、同じ群、同じ Δ 写像、引用された (5.8)、前提3件の証明はすべて依然必須。次数、装飾、族、懸垂指数が違えば拒絶。無条件の等式や別の GIVEN を導入しない。

## テスト・完了条件

限定 pytest 13R7 4件、13R2 5件、13R3 5件。DryRun・本実行 PASS、出典認証、実 DB で候補1件。群全体の完成証明は別 Phase 段階で確認。全体 pytest は Phase 終了時のみ。
