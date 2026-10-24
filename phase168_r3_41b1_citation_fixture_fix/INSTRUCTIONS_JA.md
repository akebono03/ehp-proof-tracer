# Phase 168 R3-41B1 — 既存引用テストのデータ修正

## 原因

既存の `test_unknown_citation_number_is_rejected()` が参照番号2を存在しない番号として投入する一方、対応する引用番号1を残していた。`build_narrative_body_lines()` が先に双方向整合性の失敗を返すのは正しい挙動であり、テストの期待する後段のエラーとは一致しない。

## 変更対象（全ファイル・関数）

1. `phase168_r3_12_body_binding/tests/test_phase168_r3_12_body_binding.py` の `test_unknown_citation_number_is_rejected()` 全体。テスト入力 `replace(model, citations=(), step_citation_numbers=((2,),))` に変更し、期待エラー文言を維持。import 変更なし。同ファイル全文は `full_files/test_phase168_r3_12_body_binding_AFTER.py`、関数全文は `full_functions/test_unknown_citation_number_is_rejected_FULL.py`。
2. `phase168_r3_3_proof_narrative_model.py` の `ProofNarrativeModel` クラスと `build_proof_narrative_model()` 関数。変更内容は前回 R3-41B と完全同一。
3. `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` 関数。変更内容は前回 R3-41B と完全同一。
4. 新規の補助ファイル `phase168_r3_41b1_citation_fixture_fix/fix_test.py`（追加位置：新規 Package 直下）と `tests/test_phase168_r3_41b1_citation_fixture_fix.py`（追加位置：Package の tests 直下）。

既存の `build_narrative_body_lines()`、推論規則、Reference は変更しない。

## 実行手順

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41b1_citation_fixture_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41b1_citation_fixture_fix\run.ps1"
```

## 完了条件

- 限定 pytest の既存関連テストと新規3件すべてが PASS。
- 完成4群（π₃²、π₄³、π₅⁴、π₆⁵）の Narrative が変更前後でバイト単位一致。
- 未完成3状態の探索状態・未解決 Goal・診断・確認済みステップを共通 Renderer が保持。
- 未完成の `□` を抑制、未確認の Reference を付与しない。
- 失敗時はテストと実装2ファイルをバックアップから復元。
- 全体 pytest は Phase 168 の最後にのみ実行。

## 次 Phase との境界

この Phase は既存テストのデータ誤りと R3-41B の再実行だけ。旧 fallback の削除、Web の切り替え、新数学推論、無関係のリファクタリングをしない。
