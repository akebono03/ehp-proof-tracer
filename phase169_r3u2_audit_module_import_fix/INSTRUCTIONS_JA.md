# Phase 169 R3U2 — 監査 import 起動方法の修正

## 状況

R3U1 の限定 pytest は 5 + 8 + 8 + 8 + 10 = **39件 PASS**。
最後の `audit.py` は、パッケージ配下のファイルを直接実行したため、
リポジトリ直下の `homotopy_groups.py` が import できずに失敗した。
R3U1 の復元は成功しているため、今回の R3U2 はその変更を再適用する。

## 実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3u2_audit_module_import_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3u2_audit_module_import_fix\run.ps1"
```

## 実装変更箇所

R3U1 と同じ置換：

- `phase165_r14_r5_ehp_connection.py` の `expand_cited_ehp_terminal_goal()` 全体。
- R3I・R3I1・R3I2 の既存テストファイルの各4テスト関数全体。
- 追加の5件の R3U 限定テストは同梱（本番ファイル外）。

**R3U2 固有の修正は `run.ps1` の監査起動行のみ。**
`python -B "$Package\audit.py"` ではなく、リポジトリ直下から
`python -B -m phase169_r3u2_audit_module_import_fix.audit` を呼び出す。
`PYTHONPATH` は変更しない。

### 完了条件

限定 pytest 39件 PASS、最終監査の
`R3U2_DIAGONAL_INFERENCE=True`、`R3U2_DIAGONAL_SOURCE=(5.1)`、
`R3U2_REFERENCES` に `(5.1)` と `Proposition 5.1` を確認。
全体 pytest は Phase 169 の最後まで実行しない。

何らかのテストまたは監査失敗時は、変更した4ファイルをバックアップから自動復元する。
