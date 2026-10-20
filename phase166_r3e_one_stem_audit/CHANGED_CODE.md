# Phase 166 R3-E — 変更内容

## 変更対象

本番ファイル・クラス・関数は変更しない。

新規ファイルは以下のとおり。

- `phase166_r3e_one_stem_audit/audit.py`：`inspect_case`、`main`。新規ファイルの先頭に import と関数全体を配置。
- `phase166_r3e_one_stem_audit/test_r3e.py`：6件のテスト関数を追加。新規ファイルの import 全文とテスト関数全文を収録。
- `phase166_r3e_one_stem_audit/run.ps1`：監査と対象限定 pytest を実行。
- `phase166_r3e_one_stem_audit/README.md`：実行方法。

## 監査範囲

$\pi_4^3$（最初）および $\pi_5^4$（次）の共通探索と Web Narrative を再実行する。証明未完成を自動修復・隠蔽しない。既存の文献順、規則、Renderer には変更を加えない。

## 完了条件

6件 PASS かつ `audit_result.json` の両群 `complete: true`。$\pi_5^4$ が未完成の場合は6件目で失敗し、未解決 Goal を監査結果へ記録する。全体 pytest は Phase 166 の終了時のみ実行する。
