# R3-C 一時差し戻し

- 復旧する既存ファイル：`phase165_r3_recursive_search.py`
- 復旧元：R3-C 実行時に生成されたバックアップ `phase166_r3c_ordered_search/backups/phase165_r3_recursive_search.py.20261020T024237Z.bak`
- 今回の追加ファイル：`phase166_r3c_restore/run.ps1`, `README.md`, `CHANGED_CODE.md`
- 関数内容を推測して生成せず、バックアップの実ファイルを完全復元する。import とクラス、関数は当該バックアップの全文に戻る。
- テスト変更なし。既存の限定テスト `tests/test_phase165_r3_recursive_search.py` を実行。
- 完了条件：復元ハッシュ一致、限定テスト PASS、Web の実表示確認。
- 次工程との境界：shared prefix と文献 canonical ID の結び付きは次の R3-C 修復で別途対応し、R3-D は実際の完全証明が戻ってから検証する。
