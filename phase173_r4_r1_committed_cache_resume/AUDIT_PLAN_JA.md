# Phase 173 R4-R1 — Git 履歴のキャッシュ例外と監査再開

## 前提

GitHub develop の `f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941` を確認した。`a7763513` との差分は R3・R4-R1 の監査用ファイルの追加と `.pytest_cache/v/cache/nodeids` のコミット済み更新のみである。過去の R4-R1 監査コードは R3 の追加だけを許し、コミット済みキャッシュ変更を拒否していた。

## 変更対象（新規のみ）

- `phase173_r4_r1_committed_cache_resume/audit.py`：既存 R4-R1 監査コードの独立した読み取り専用コピー。`REVIEWED_HEADS`、`APPROVED_ADDED_PATHS`、`COMMITTED_CACHE`、`APPROVED_WORKTREE_AUDIT_SHA256` の定数、新しい `verify_audit_only_changes()`、`verify_tracked_worktree()`、`preflight()` および `main()` を含む。
- `phase173_r4_r1_committed_cache_resume/tests/test_audit.py`：コミット差分と作業ツリーの許可／拒否を検査する限定テスト。
- `phase173_r4_r1_committed_cache_resume/run.ps1`：限定 pytest と監査の実行。
- `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` は新規。

既存の全ファイルを変更しない。既存の import やクラス・関数、正式5文書を変更しない。

## 監査条件

- HEAD は実際に監査した2コミットのどちらかに固定。
- BASELINE からの追跡差分は、認可済みの追加ファイルおよび nodeids のコミット済み `M` のみ許可。
- 作業ツリーの例外は未ステージの nodeids と、SHA-256 完全一致の既存 R4-R1 監査修正3ファイルのみ。
- 11個の証明関連ソースのコミット時 blob SHA が一致すること。
- Toda の (5.6)、Prop 4.4、Lem 5.4 が原文どおりであること。
- 公開 Root の引用付き前提・先行結果の資格・未解決 Subgoal を観測する。DB Goal を GIVEN にしない。

## 完了条件／次 Phase

限定 pytest が PASS、DryRun が PASS、実監査が `PHASE173_R4_R1_RESUME_AUDIT=PASS` を出力して `audit.json` を生成すること。これは証明完成を意味しない。$\pi_8^5$ の位数8、Web 表示、全体 pytest、Closeout は対象外。
