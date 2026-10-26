# Phase 169 R3Z — 実行手順

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3z_reference_only_generic_eta.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3z_reference_only_generic_eta\run.ps1"
```

## 変更対象

- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` 全体。インストーラーは関数全体を AST で取り出して変換・置換します。変更後の関数全文は `output/render_model_backed_narrative_markdown_FULL.py`、変更後のモジュール全文は `output/phase168_r3_5_model_renderer.py.FULL.py` に出力します。
- 新規 `tests/test_r3z_reference_only_generic_eta.py` にテスト関数3件を追加します。既存テストは変更しません。
- 新規 `audit.py` に `examine()` と `main()` を追加します。読み取り専用です。
- import は `render_model_backed_narrative_markdown()` 内の局所 import だけを追加します。モジュール先頭の import 節は変更しません。

## 実装境界

数式の文字列一致だけで隠すのではなく、一般型付き命題の直接の子となる検証済み数値特殊化が Narrative Model に存在し、表示対象の場合だけ一般 GIVEN の本文表示を抑えます。出典、ProofStep、文献順判定、引用番号、特殊化の表示はそのまま残します。

限定 pytest は新規3件、R3Y4件、R3U5件、R3I8件、1-stem10件の計30件です。全体 pytest は実行しません。
