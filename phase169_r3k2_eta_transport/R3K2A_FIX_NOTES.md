# Phase 169 R3K2A — インストーラーの位置判定修正

## 前回の停止原因

`apply.py` の `patch_renderer()` は、4つの空白から始まる
`from homotopy_groups import TodaPrimaryGroupZeroStatement` という文字列が
1回だけ登場すると仮定していました。しかし現行 R3K の関数には4空白と8空白で
始まる2つの import 文があり、部分文字列検索によって2件と数えられました。

`patch_renderer()` はファイル書き込みより前に例外を発生させたため、
前回の停止時点では本番ファイルへの部分適用はありません。

## 変更するファイルと関数

- `phase169_r3k2_eta_transport/apply.py`：`patch_renderer()` 全文。
  本文ループ `    for index in order:` の完全一致行を一意な位置として使用。
  R3K が設置した補助関数と重複抑止用集合の存在も検査。
- `phase169_r3k2_eta_transport/run.ps1`：全文更新。インストール前の
  専用回帰 pytest を追加。
- `phase169_r3k2_eta_transport/tests/test_r3k2a_anchor_guard.py`：新規。
  2個の import 文字列が存在する場合も置換に成功し、本文ループが
  ない場合は何も書き換えず拒否することを検査。

`phase168_r3_5_model_renderer.py` や
`phase168_r3_27_typed_statement_projection.py` に適用する**数学的な変更内容は前回 R3K2 と同じ**です。
証明探索、台帳、既存テスト、ドキュメントは変更しません。

## 実行方法

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3k2a_anchor_fix.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3k2_eta_transport\run.ps1"
```

ZIP は前回と同じディレクトリ名で展開され、修正版 `apply.py` と `run.ps1`
を上書きします。

## 限定検証

最初に新規のインストーラー回帰2件を実行し、それが通ってから本番の
2関数の置換に進みます。続けて R3K2 の5件、R3J の4件、既存1-stemの
限定回帰を別プロセスで実行し、最後に Web Narrative を監査します。
全体 pytest は Phase 169 の最後にだけ実行します。

## 完了条件

- `R3K2A_INSTALLER_PYTEST_EXIT_CODE=0`
- `R3K2_PATCH_COMPLETE=True`
- `R3K2_FOCUSED_PYTEST_EXIT_CODE=0`
- `R3K2_ONE_STEM_PYTEST_EXIT_CODE=0`
- `R3K2_AUDIT_PASS=True`
- `R3K2_COMPLETE`

実行結果が得られるまで完了したとは判定しません。
