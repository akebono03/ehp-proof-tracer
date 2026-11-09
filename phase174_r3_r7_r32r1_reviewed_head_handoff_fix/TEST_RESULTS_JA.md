# R32R1 検証証跡

- GitHub `develop` の HEAD が `02f694b27a4239052bfa9d27a116fca6bbbff6b5` であることを確認。
- `25118e281445ca17b30c60c8fd02d00acaa25ea5` からの差分は、R31 監査ディレクトリの9ファイル追加のみ。
- R32 `audit.py` の AST 比較では、変更した既存関数は **`verify_checkout()` のみ**。追加した定数は `REVIEWED_R31_MERGE_HEAD` のみ。import は不変。
- R32 `run.ps1` の変更は、R31 HEAD 固定テストのうち新しい HEAD では再実行できない2件を実行対象から外し、現行ソースでも検証可能な8件だけを列挙する部分のみ。
- `python -m compileall` でパッケージ内の Python 構文を確認。
- 修正 Source Guard のローカル HEAD 2モード、未知の HEAD 拒否、R31 改変拒否、参照元ファイル改変拒否、パッチの全文 SHA256、インストールの冪等性について、独立した限定テスト **11 PASS**。
- Windows PowerShell 上の Source Guard、R32 本監査、R32/R18/R5 の限定 pytest は、ユーザー環境で実行するまで未確認。全体 pytest 未実施。
- R32 の `LOWER_DELTA_KERNEL_PROVED=False`、`DELTA_SURJECTIVITY_PROVED=False`、`ROOT_COMPLETE=False` は維持する。
