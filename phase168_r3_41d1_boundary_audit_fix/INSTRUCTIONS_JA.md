# Phase 168 R3-41D1 — 未完成証明の境界解析監査修正

## 対象

既存の製品コードは変更しません。R3-41D の監査コードの誤りをこの独立した監査パッケージで修正します。

- `audit_core.py`: `split_narrative_sections()` を追加し、`markdown_reference_text()`、`web_reference_text()`、`audit_citation_projection()` を修正。完成と未完成の Reference/証明境界を正しく識別します。
- `audit.py`: 実探索ごとの取得エラーを明示し、取得エラーがある場合はレポート保存後に実行失敗とします。
- `tests/test_phase168_r3_41d1_boundary_audit_fix.py`: 元の6件＋境界検証4件。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41d1_boundary_audit_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41d1_boundary_audit_fix\run.ps1"
```

## 完了条件

5群の実探索をエラーなく取得すること。実際の部分証明で使用した登録命題・Reference本文とWeb表示を照合し、取得できない項目は未検証として残すこと。`output/review_bundle.zip` を添付してください。全体pytestは実行しません。
