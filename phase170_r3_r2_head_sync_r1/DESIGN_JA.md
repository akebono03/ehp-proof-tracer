# Phase 170 R3-R2 HEAD 同期修正 — 設計・監査記録

## 目的

旧 `phase170_r3_r2_root_expansion_audit` では R3-R1 の `preflight` をそのまま再利用したため、R2 後に追加された R3-R1 の監査専用6ファイルを未確認変更として拒否した。R3-R1 のコードや既存本体は変更せず、R3-R2 の新規パッケージに厳密な履歴検証を追加する。

## 確認済み Git 履歴

- R2 実測・R3-R1 が使用する基準 HEAD: `f9e9a9d59970943d967e2cbcb0a98f13b2471407`
- R3-R1 の実測時 HEAD: `56347c34c36dd458d23af2851b7a1af531d00a6d`
- R3-R2 再実行用に監査済みの現行 HEAD: `d63e644ea4c5353cffcdd31cf183111e43e5de17`

GitHub `develop` のコミット比較により、基準 HEAD から現行 HEAD まで2コミットの差があり、R2 監査パッケージ13ファイルと R3-R1 監査パッケージ6ファイルが追加されただけと確認した。既存の本体・CSV・テスト・文書のコミット済み変更はない。

## 変更対象と置換単位

新規パッケージ `phase170_r3_r2_head_sync_r1/` 内だけに変更を限定する。

- `audit.py`：import 部分は元の新規監査ファイルを完全維持。定数 `REVIEWED_R3_REPORT_HEAD`、`REVIEWED_HEAD`、`REVIEWED_ADDED_AUDIT_FILES` を定義し、新規 `preflight_after_reviewed_audit_commits` を `load_reviewed_r3_code` と `check_reports` の間に追加。既存 `check_reports` 内の保存済み R3-R1 HEAD 判定と `run` 内の preflight 呼び出しを修正。両関数全文をファイルに収録。
- `run.ps1`：出力フォルダ名を修正版専用に変更。全文収録。
- `tests/test_head_sync.py`：新規テスト関数をファイル全文で追加。
- `tests/test_audit_contract.py`：旧 R3-R2 の限定テストを変更せず同梱。
- `README.md`：英語、全文更新。
- `DESIGN_JA.md`：日本語、全文更新。
- `__init__.py`：新規パッケージの定義。既存本体には触れない。

## 安全性の検証

`preflight_after_reviewed_audit_commits` は Git ブランチを `develop` に、HEAD を上記現行コミットに限定する。R2 基準 HEAD からの差分を NUL 区切りで取得し、追加19ファイルのステータスと名前を完全一致で判定する。新規追加、削除、改名、変更、欠落はすべて拒否する。さらに Git index・ワークツリーの未コミット変更、R3-R1 が確認済みの本体 Git blob、4種類のデータベースがコミット済み内容と同一であることを確認する。元の R3-R1 監査コードの SHA-256 検証も維持する。

HEAD の検証は二つを区別する。保存済み R3-R1 `audit.json` は R3 実行時の `56347c...`、今回監査する実際の HEAD は `d63e...` でなければならない。保存済み観測を新しいコミットで実行したものと誤認しない。

## 完了条件・次工程との境界

新規・既存限定テストの PASS、5件の根元 Goal の推論候補採録、監査出力のリポジトリ外への新規保存、`tracked_unchanged=True`、`AUDIT_EXIT=0` をもって今回の監査実行完了とする。全体 pytest は Phase 170 末尾まで行わない。

この監査は証明探索や新しい ProofStep の構築を行わない。推論候補の存在は数学的証明を意味しない。R3-R3 以降の判断は実測出力に基づき行う。
