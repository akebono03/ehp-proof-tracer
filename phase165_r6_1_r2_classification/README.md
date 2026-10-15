# Phase 165 R6-1：群専用探索候補の追加監査（速度修正版）

この ZIP は以前の `phase165_r6_1_r2_classification` を置き換える読み取り専用監査です。production ファイルは変更しません。

## 原因と修正

旧 `audit.py` は条件分岐ごとに `ast.get_source_segment(source, condition)` を呼び、Python 3.10 ではソース全文の走査が繰り返されました。修正版ではファイルごとに `splitlines()` を一度行い、条件の `lineno` と `end_lineno` で該当行だけを参照します。1000条件分岐の検出を確認する限定テストを追加しました。

## 使用方法

リポジトリのルートで ZIP を展開してから：

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_1_r2_classification\run.ps1"
```

限定テスト4件の後に `classification.json` と `classification.md` を同じフォルダに出力します。全体 pytest は実行しません。

## 範囲と制約

トップレベルの Python ファイルにある検索関連関数と静的 import 経路を対象にします。450候補との件数比較はできません。動的 import、クラス内の関数および実際の実行可能性までは断定できません。群専用分岐の数学的分類は引き続き人手による確認が必要です。

production コードの変更・群専用 Adapter の削除は R6-2 の責務です。
