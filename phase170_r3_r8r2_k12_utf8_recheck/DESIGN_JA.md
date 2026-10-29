# Phase 170 R3-R8R2 — k=12 UTF-8 再監査

## 原因

R3-R8 の全件監査では n=2, k=1..33 のうち32件が COMPLETE_AND_WEB_VERIFIED、k=12 が WORKER_FAILED だった。詳細ログでは `print(SENTINEL + json.dumps(data, ensure_ascii=False, sort_keys=True))` の時点で Windows 標準出力 `cp932` による `UnicodeEncodeError` が発生していた。さらに GitHub `develop` の HEAD が、R3-R8 監査をコミットした `114a67d708edba3d17da673a218034fcd804aa15` に進んだため、前版の HEAD 検査で処理が拒否された。

## 変更対象

本番の production ファイル、既存の監査ファイル、既存テスト、五つの正式文書は**一切変更しない**。新規監査パッケージ `phase170_r3_r8r2_k12_utf8_recheck/` に `runner.py`（独立実行）、`run.ps1`（Windows 起動）、`tests/test_contract.py`（独立テスト）、`README.md`、本ファイル、`FULL_CHANGED_CODE_JA.md` を置く。

## 処理

1. GitHub で確認した `develop` HEAD、`audit.py`・Toda (5.2) 輸送・R10E4 先行 DB 判定の Git blob を事前確認し、追跡済みの差分がある場合は拒否する。
2. 既存 `phase170_r3_r8_n2_exhaustive_audit/audit.py --worker --k 12` を新しい Python 子プロセスで実行する。子プロセスの `PYTHONIOENCODING` を `utf-8`、`PYTHONUTF8` を `1` に固定する。
3. Worker の既存 `search_group_from_registered_goal` と Web の Trust Boundary を変更せず、マシン可読な結果を UTF-8 で取り出す。
4. 先行する33件監査結果を見つけた場合は、k=0..33 の行がすべて存在し、前回の未完了は k=12 の WORKER_FAILED だけ、32件完成、追跡済みファイル不変、前回 HEAD が `170-3-7` であったことを検査する。今回の k=12 行だけを新規集計に差し替える。**元の audit.json は変更しない**。
5. 結果を `%LOCALAPPDATA%/EHPProofTracerRecovery/phase170_r3_r8r2_k12_*/audit.json` と `k_012.log` に保存する。Git 状態の不変性を事後確認する。

## 完了条件

`PHASE170_R3R8R2_k=12_RESULT=COMPLETE_AND_WEB_VERIFIED` が出力され、過去の監査との統合が `COMBINED_33_K`、`DOMAIN_CHECKED=33`、`DOMAIN_COMPLETE=33`、`DOMAIN_GAPS=0` となること。k=12 が未完成の場合は証明を捏造せず診断を残す。全体 pytest は Phase 170 の終盤まで実行しない。

## Phase 境界

このパッケージは R3-R8 の監査出力問題の切り分けに限定する。Toda (5.2) の共通証明経路、先行 DB 採用条件、生成元一致の数学的検証、文献採録、Renderer に変更を加えない。
