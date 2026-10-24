# Phase 168 R3-41D — 実探索部分証明の Reference 監査

**既存の実装ファイル、命題台帳、テストファイルは変更しません。**

## 監査対象

- 標準 Web の実検索 5件：`π₆⁴`、`π₆³`、`π₇⁵`、`π₇⁴`、`π₈⁵`
- 完成証明の対照 1件：`π₄³`

実際の状態が `COMPLETE`、`PARTIAL`、`SEARCH_FAILED` のどれになるかはコードの実行結果に従います。部分証明と仮定していません。部分証明でも出典付きのステップが得られなかった場合は、引用の実証が足りないと報告します。

## 新規ファイルと関数

- `audit_core.py`：純粋な照合関数 `normalize_visible()`、`web_line_text()`、`web_text()`、`web_reference_text()`、`markdown_reference_text()`、`section_bullets()`、`audit_citation_projection()` を新規追加。
- `audit.py`：実際の標準 Web を1回だけ呼ぶ `capture_live_case()`、各結果を調べる `one_case()`、報告を出力する `main()` を新規追加。
- `tests/test_phase168_r3_41d_live_partial_reference_audit.py`：限定テスト6関数を新規追加。
- `run.ps1`：限定 pytest と監査のみを実行。
- `README.md`：英語の使用説明。

すべての関数・テスト・import を ZIP 内のファイルに全文収録しています。既存 API は変更しません。

## Windows PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41d_live_partial_reference_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41d_live_partial_reference_audit\run.ps1"
```

## 完了条件

1. 限定 pytest に PASS する。
2. 実検索各件のステップ数、Reference 数、出典の本文数、未解決 Goal を出力する。
3. ProofStep と screened bridge の登録 Assertion ID を照合する。
4. Reference の**見出しと本文**の双方について Markdown と Web の存在を検査する。
5. 引用がない部分証明を「引用監査成功」と誤認しない。
6. 実行中に取得できなかった群や内容不足を明示し、数学的命題は補完しない。
7. 既存実装ファイルは一切変更せず、全体 pytest を実行しない。

## 次工程との境界

R3-41D は監査のみです。判明した不備を修正する場合に限り R3-41E を検討します。`legacy` および fallback の廃止は今回行いません。

監査後は `phase168_r3_41d_live_partial_reference_audit\output\review_bundle.zip` を添付してください。
