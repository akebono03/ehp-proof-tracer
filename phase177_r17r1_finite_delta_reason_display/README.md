# Phase 177 R17R1R2R1 — Delta equality display regression fix

R17R1R2 の表示処理、既存ファイルへの接続、数学的推論規則は変更しない。実際の型付き生成元像の等式を共通 Renderer で数式化し、証明本文で単射性の表示より先に現れることを検査する。空白と括弧のサイズ指定のみを無視する。参考文献欄だけに数式が存在する場合は合格にしない。

同一ディレクトリに上書き解凍する。run.ps1 -DryRun と run.ps1 を実行する。既存 installer の Gate は R17R1R2 のまま、最終 Gate は R17R1R2R1 となる。限定 pytest は22件を期待する。全体 pytest は実行しない。変更後の既存ファイル全文は従来どおり監査ディレクトリへ出力する。
