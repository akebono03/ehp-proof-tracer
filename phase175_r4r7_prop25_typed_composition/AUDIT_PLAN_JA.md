# Phase 175 R4R7R1 — R4R6 コミット履歴境界の修正監査

## 背景

R4R7 初版の限定 pytest は135件 PASS したが、DryRun は `R4R7_UNREVIEWED_HEAD: 11968d23724cee147520b5fa3fd5a6e89989003e` で失敗した。GitHub 上で HEAD `11968d2...` は基準 `c48fdc3...` の直系子孫であり、変更は R4R6 パッケージ8ファイルだけと確認した。

## 対象ファイル・関数

- `audit.py`: `REVIEWED_R4R6_HEAD`, `REVIEWED_R4R6_PATHS` を追加。`reviewed_head_lineage()` を `git()` と `preflight()` の間に追加。`preflight()` 全体を置換。
- `tests/test_audit.py`: `hashlib`, `subprocess` を import し、合成 Git 履歴ヘルパー3件・テスト6件を末尾へ追加。
- `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`: 全文更新。

## 検証計画

1. branch `develop`、root、レビュー済みの2 HEAD のいずれかを検証する。子孫 HEAD は Git の祖先関係に加え、8ファイルの厳密な変更集合一致を要求する。
2. ワーキングツリーの既存差分制限、固定 Git blob、R4R6 監査本体 SHA256、先行成功レポートの全検証を維持する。
3. 不正な追加ファイル・未知の後続 HEAD・ソース改変・監査コード改変・祖先不一致を拒否する。
4. 限定 pytest のみ実行。全体 pytest は Phase 175 終了時に限定する。

## 禁止事項

- 既存本番コードや共有検索 Provider の変更
- `Δ(η_9)` または `π_9^5` の直接 GIVEN 登録
- 数学規則・Narrative・結論の先取り
- 符号 ± の根拠なき消去

## 成功条件

DryRun Gate `PASS_R4R7_PROP25_TYPED_INFERENCE_DRYRUN`、本実行 Gate `PASS_R4R7_PROP25_TYPED_INFERENCE_ISOLATED_NOT_PUBLIC`。ただし `π_9^5` は未完成を維持する。
