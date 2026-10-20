# Phase 166 R3-Q：Hopf 事実の一元化に向けた監査

## 変更対象

本番ファイル・既存関数は変更しない。追加するのは `phase166_r3q_hopf_single_source_audit/audit.py` の `main()`（import と関数全文を同ファイルに収録）、`run.ps1`、`README.md`、本ファイルのみ。

## 監査範囲

Proposition 5.1 の Hopf 等式について、独立登録・複合主張の子登録・`GeneratorImage` 登録の3形式を調べる。数学的データのうち、入出力生成元・写像の表示・掲載位置・既存 GIVEN の有無を比較する。自動的に登録を削除せず、新しい推論規則も追加しない。

## テストと完了条件

実行コマンドは `python -m phase166_r3q_hopf_single_source_audit.audit`。`audit.json` が作成されること。pytest は本段階で実行しない。結果を確認してから次の Phase 166 R3-Q に必要な最小の変換規則と重複削除を判断する。全体 pytest は Phase 終了時のみ。
