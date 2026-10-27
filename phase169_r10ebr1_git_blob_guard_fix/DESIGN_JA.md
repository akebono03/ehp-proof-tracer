# Phase 169 R10EB-R1 — Git blob と改行形式の整合性検査修正

## 現象と原因

R10EB の初回実行は `R10EB source Git blob not reviewed: phase168_r3_27_typed_statement_projection.py` で停止した。GitHub の `develop` HEAD `b80a8475051b384fb0c58b21d2b74980caccc4e0` では、対象の `phase168_r3_27_typed_statement_projection.py` と `toda_human_readable_renderer.py` はどちらも CRLF を含む Git blob として保存されている。元の `prepare_patch()` は LF に正規化した後の bytes から SHA-1 を計算するため、登録済みの Git blob の SHA-1 と一致しなかった。

## 最小の対応

変更対象は **新規** `phase169_r10ebr1_git_blob_guard_fix/patch.py` の `prepare_patch()` および `main()` と、それを起動する新規 `run.ps1`、限定テストのみ。既存 R10EB パッケージのファイルも、数学的なコードも変更しない。

`prepare_patch()` は元のファイルの bytes、LF 正規化の bytes、CRLF 再構築 bytes のうち、Git で確認済みの blob SHA と一致するものがある場合だけ許可する。実行スクリプト側では Git の祖先関係、該当ファイルの `HEAD:path` blob、未コミット差分がないことも先に確認する。混在改行・未検証の内容は許可しない。変換後は元の改行形式を保持する。

実際の Renderer の変更内容は元の R10EB の `transform()` を使用する。対象は `element_tex()` と `render_toda_expression_latex()` のみで、共通の `typed_stable_composition_power_latex()` を使用する。証明木・検索・引用・Trust Boundary（信頼境界）に変更はない。

## テストと完了条件

新規 `tests/test_r10ebr1_git_blob_guard.py` で、CRLF Git blob、LF blob、CRLF blob からの LF checkout、未検証内容の拒否、混在改行拒否、二重適用拒否、欠落ファイル拒否を確認する。作成環境では新規と既存 offline の限定テスト計12件 PASS。Windows 実リポジトリでの R10EB 既存限定 pytest・４群の Trust Boundary 監査・公開表示 `\\nu_{30}^{3}` の確認は、`run.ps1` に任せる。

実行に失敗した場合は本番２ファイルと監査出力の実行前 bytes を復元する。全体 pytest は Phase 169 の終了時のみ実施する。

## 次 Phase との境界

R10EB-R1 はチェック処理の不具合のみを直す。重複する逐次懸垂等式と長い表示を短縮する機能は R10EC 以降とし、今回追加しない。
