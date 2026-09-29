Phase 144-5-R1
==============

目的
----
Phase 144-5 の focused test 4件の失敗を修正する。

原因
----
production implementation の失敗ではなく、新規テストの Python 文字列・正規表現の
エスケープが過剰だった。

実際の Phase 144-5 出力にはすでに以下が確認できた。

- `まず、$\nu'$ を定める.`
- 数式への `\tag{1}` ... `\tag{35}`

修正
----
tests/test_phase144_5_generic_definition_order_equations.py のみ置換する。

1. テスト入力の `\\n` を実際の改行 `\n` に修正。
2. `\\nu'` の期待値を実際の LaTeX `\nu'` に修正。
3. `\\tag` の期待値・regex を実際の LaTeX `\tag` に修正。

production source は変更しない。

実行
----
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase144_5_r1_test_fix.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_5_r1_test_fix\run_phase144_5_r1.ps1"

全体 pytest は Phase 途中なので実行しない。
