# Phase 169 — Git 競合コピー隔離 R2B

## 監査による修正理由

R2 の実行ログで、HEAD `232a92883b0cb009762b437cbb3cc550f00ab6bd`、競合コピー3件、変更なしを確認した。競合コピーの実際の相対パスは、`logs/HEAD (oomae-pc11 の競合コピー 2026-10-28)`、`logs/refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)`、`logs/refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)` である。

旧 R2 では許可対象のうち2件を誤って `.git/refs/` 配下としていた。これでは安全確認が必ず停止する。R2B は実測済みの `.git/logs/` 3件へ厳密に変更し、`.git/refs/` 配下の追加コピーなど未知の変更は拒否する。

## 変更対象と変更境界

新規フォルダ `phase169_git_environment_r2b_reflog_only_quarantine` の `recover.py` にある定数 `CONFLICT_PATHS` を訂正した。関数本体は旧 R2 と同じ。`tests/test_recovery.py` の import を新規パッケージへ更新し、監査ログとの一致を確認する `test_r2b_exact_user_observed_reflog_only_conflicts()`、未知の refs 側競合を拒否する `test_r2b_ref_conflict_not_accepted_as_observed_reflog()` を末尾に追加した。README.md と本設計文書は全文を作成した。既存リポジトリの製品コード・テスト・文書には変更を加えない。

## 保全手順

初期モードは読み取り専用。隔離は全同期 PC の Dropbox を停止し VS Code 等の Git 利用アプリを終了した後、利用者が `-Mode Quarantine -DropboxPaused` を明示した場合だけ実行する。Dropbox の実際の同期停止はスクリプトでは検知できない。

`.git` 全体と追跡対象差分・stage 済みファイル、R5D の5ファイルを Dropbox 外の `%LOCALAPPDATA%\EHPProofTracerRecovery` に複製し、Git index と競合3ファイルの SHA-256 を照合する。その後、厳密一致した `.git/logs` 内の競合コピーだけをバックアップ先へ移す。通常の HEAD・refs・index・ソースは変更せず、失敗時は隔離ファイルの復元を試みる。

## 完了条件と次の工程

`GIT_RECOVERY_QUARANTINE=PASS`、`GIT_RECOVERY_SCRIPT_EXIT=0` を確認し、`git -c core.longpaths=true status -sb` と develop 両参照の確認を行う。バックアップを保管し、Git 操作が正常になってから R10ET-R6 の AUDIT_ONLY を再開する。273文字の生成物のステージ対象除外は別課題とし、全体 pytest は Phase 169 終了時のみとする。
