# Phase 173 R15R17-R2R1: 起動ガード修正

## 対象と目的

R15R17-R2 の変更対象本体は `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` のみであり, 今回の R2R1 ではこの証明コードの修正内容を変えない.

R2 の PowerShell 実行で `Extract R15R17-R2 ZIP at the repository root` が発生したのは, Git が `C:/Users/...` と表記したパスと PowerShell の `C:\Users\...` を文字列として直接比較していたためと考えられる. 実際のルートの不一致ではない可能性が高い.

## 変更対象

- `run.ps1` 全体: `git rev-parse --show-toplevel` の結果と `$Root` を `[System.IO.Path]::GetFullPath()` で正規化し, `OrdinalIgnoreCase` で比較する. 新たに `R15R17R2_REPOSITORY_ROOT=PASS` を出力する.
- `install.py`: 検証済み GitHub `develop` HEAD を `11fdf0f5c52ce2de786e36c3a3d0abe7a0d0fa26` に更新する. 以前の2つのローカル HEAD は引き続き許可する. R2 対象ファイルのレビュー済み Blob `6dd75099bb2c71fb9873477cb36c11bdb7dad410` と R1 インストール済み状態の厳密検査は維持する.
- `tests/test_path_guard.py` 新規: Windows のパス正規化, Git HEAD と Blob の固定, DryRun/適用/復元の実行契約を確認する.
- `README.md`, `design.md`: この修正の説明を全文更新する.

## 安全条件

- 既存の証明・探索・表示本体, `patch.py`, `tests/test_patch_contract.py`, `tests/test_public_narrative.py` は変更しない.
- 元の R15R17-R1 の変更・Git index・他の未追跡ディレクトリを保持する.
- 本体変更の前に DryRun, 変更ファイルの検証, R1 状態チェックを実施する.
- R2 インストール後の限定 pytest が失敗した場合は R2 の Renderer 変更だけをバックアップから復元する.
- 全体 pytest は Phase 173 の最後だけ実行する.

## 完了条件

DryRun で `R15R17R2_REPOSITORY_ROOT=PASS` と `R15R17R2_DRY_RUN=PASS`, 通常実行で `R15R17R2_INSTALL=PASS`, `R15R17R2_FOCUSED_PYTEST=PASS`, `R15R17R2_APPLY=PASS` を確認する. 既存の5つの独立パッチテストに新規3つの静的な起動検査を追加する.
