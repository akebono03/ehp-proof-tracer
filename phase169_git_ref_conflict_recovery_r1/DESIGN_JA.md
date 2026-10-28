# Phase 169 Git ref 競合コピー復旧 R1

## 調査対象と根拠

VS Code の Git ログには `refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)` と `refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)` という無効な ref が記録された。従来の修復スクリプトは `CONFLICT_COUNT=0` であったが、後続の `git fetch` は同一 ref に関する `fatal: bad object` で失敗した。

この矛盾は、従来の PowerShell における限定的なディレクトリ直下検索と名前の完全一致による検出からは解消できない。R1 では Python の `os.walk` で Git common directory 配下の `refs` を再帰走査し、候補名と実パスを報告する。`packed-refs` の異常は診断専用とし、編集しない。

## 変更対象と修復の境界

新規 `phase169_git_ref_conflict_recovery_r1/recovery.py`、`run.ps1`、`tests/test_recovery.py`、`README.md`、`DESIGN_JA.md` のみ。既存の本番ファイル、テスト、ドキュメントは変更しない。新規関数とその import の全文は各ファイル内に記載した。

標準実行は `DRY_RUN`。`-Repair` は `refs/heads` と `refs/remotes/origin` 直下の `develop` で始まり `競合コピー` を含む無効な loose ref に限って外部へ退避する。通常の `develop` と `origin/develop` は一切移動せず、HEAD を含む3つのコミット ID を保存・照合する。複数の予期しない候補、packed-refs の疑い、警告が継続する場合は成功扱いにしない。

## テスト・完了条件・次工程

限定 pytest: `python -B -m pytest -p no:cacheprovider -q phase169_git_ref_conflict_recovery_r1/tests`。不正な loose ref の発見、確認専用モード、バックアップ退避、正常参照の維持、候補超過の拒否、検出なしの成功誤判定防止を検査する。全体 pytest は Phase 169 最終時にのみ実施する。

完了条件は `GIT_REF_R1_STATUS=PASS` と後続の `git fetch origin develop` 成功。復旧が完了するまでは R10EK の共通 Projection 設計監査や文書更新には進まない。Proof Tree と Renderer の変更は対象外とする。
