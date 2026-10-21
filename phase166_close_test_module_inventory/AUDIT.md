# Phase 166 終了時のテスト収集監査

変更対象：新規 `close.py`（`identify_test_modules()`、`main()`）、`run.ps1`、説明文書。既存の本番コード・テストは変更しない。

`install_and_test.py` や `apply_and_test.py` は pytest の収集対象になり、import 時に既存コードを書き換えようとして停止した。ファイル名だけの除外を繰り返さず、AST で直接 `test_` 関数・`Test` クラスがある通常テストモジュールを列挙して明示的に実行する。未解析ファイルがあればテストを開始せず停止する。

注意：テストを別モジュールからインポートするだけの特殊なモジュール、pytest の動的生成などはこの方式では拾えない可能性があるため、除外一覧を確認して終了判定する。実行で PASS しただけでは Phase 166 完了を無条件には宣言しない。

成果物：`results/<timestamp>/test_inventory.json`、`pytest_command.json`、`pytest.log`、`summary.json`、Git 状態。

Phase 167 では証明本文の修正を行い、ここでは変更しない。
