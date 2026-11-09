# R32 テスト証跡と未実行条件

- GitHub `develop` の対象 HEAD と依存ファイルの blob SHA は、GitHub 接続を用いて確認した。
- Toda Proposition 5.8、式 (5.10)、Proposition 5.9 の順序と、指定文字列が各原文区間内に一度現れることを照合した。
- R32 の Python ファイルは `compileall` で構文検査した。
- R32 `kernel_contract.py` の新規テストを、データクラスと EHP 添字検査の独立スタブで実行して **25 PASS**。
- R32 `inspect_toda_citations` の最小入力に対する正常・改変拒否・Git blob LF/CRLF 同一性のローカル smoke test は PASS。

**重要：** 上記の独立スタブ検査はプロジェクト本体の実モジュールを用いたテストではない。GitHub の Python ソースはこの実行環境のファイルツリーに無いため、統合した Source Guard、通常監査、限定 pytest は実施していない。ユーザー環境で `run.ps1 -DryRun` と `run.ps1` を実行して初めて R32 の本番 Gate を確認できる。

R32 は全体 pytest を行わず、下側 Δ の核と根の完成を証明したとは主張しない。
