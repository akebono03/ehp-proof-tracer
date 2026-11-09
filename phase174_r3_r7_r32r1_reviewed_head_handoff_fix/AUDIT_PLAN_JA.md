# Phase 174 R3-R7-R32R1 — Source Guard の HEAD 引き継ぎ修正

## 変更対象（実装前に列挙）

既存ファイルの変更は次の2件だけ。数学的な推論規則・本番 Provider・GIVEN・共通 Renderer を変更しない。

1. `phase174_r3_r7_r32_lower_delta_kernel_audit/audit.py`
   - 定数 `REVIEWED_R31_MERGE_HEAD` を `REVIEWED_HEAD` の直後に追加。
   - **関数全体** `verify_checkout()` を置換。R31 が未統合のローカル HEAD `25118e281445ca17b30c60c8fd02d00acaa25ea5` と、R31 統合済み HEAD `02f694b27a4239052bfa9d27a116fca6bbbff6b5` の両方を許可。ただし GitHub 側は後者を必須とする。
   - R31 の `audit.py` SHA256 と、既存数学ソースの全 blob SHA 検査は保持する。
2. `phase174_r3_r7_r32_lower_delta_kernel_audit/run.ps1`
   - スクリプト全文置換。既に HEAD の古い固定値を前提とする R31 テスト2件を通常の R32 検査から外し、独立して有効な8件に限定する。
   - R32/R18/R5 の限定 pytest を引き続き実行する。

新規ファイルは `phase174_r3_r7_r32r1_reviewed_head_handoff_fix/` 内のみ。`install.py`、`tests/test_patch.py`、`run.ps1` と各説明書を追加する。新規関数は各モジュールの import の後に定義。既存 import は変更せず、全文を `IMPORTS_FULL.txt` に収録。

## GitHub 現行コードと関連テストの確認

- 旧 HEAD：`25118e281445ca17b30c60c8fd02d00acaa25ea5`。現行 GitHub `develop`：`02f694b27a4239052bfa9d27a116fca6bbbff6b5`。
- GitHub commit 比較：**1コミット、R31 ディレクトリだけ9ファイル追加**。本番ソースのコミット変更なし。
- R32 `audit.py`、`run.ps1`、`tests/test_audit.py` と R31 `audit.py`、`tests/test_audit.py`、`tests/test_static_helpers.py` を確認した。
- R32 と R31 の固定 Source Guard を比較した結果、R31 の `test_source_guard_preserves_reviewed_r30_handoff`、`test_r31_reports_no_unsupported_completion` は新しい GitHub HEAD のもとでは成立しない。R31 の歴史的監査パッケージは変更せず、この2件だけ現行 R32 の限定テスト対象から除外する。

## 安全条件と完了境界

- `-DryRun` は書き込みなし。インストーラは **旧版・修正版の全文 SHA256 に一致する場合に限り**2ファイルを置換する。
- ローカル HEAD は旧版または R31 統合後の版に限定。GitHub HEAD は検証済みの R31 統合後の版に限定。
- R31 ファイル SHA256 不一致、未知の HEAD、既存の追跡ファイル変更、不明な R32 変更はすべて失敗とする。
- `git reset`、`git checkout`、`git pull`、`git fetch` は実施しない。R30 と R31 を上書きしない。
- R32 の数式自体は未完成を維持。`LOWER_DELTA_KERNEL_PROVED=False`、`ROOT_COMPLETE=False`。
- 全体 pytest は Phase 174 最終段階でのみ行う。

## 実行順序

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase174_R3_R7_R32R1_REVIEWED_HEAD_HANDOFF_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32r1_reviewed_head_handoff_fix\run.ps1' -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R32R1 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32r1_reviewed_head_handoff_fix\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'R32R1 audit failed' }
git status -sb
git diff --stat
Write-Output '(END)'
```

本実行で R32 の報告と限定 pytest が成功したとき初めて R32 完了を宣言する。
