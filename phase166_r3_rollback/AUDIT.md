# Phase 166 R3 差し戻し

対象ファイルは `phase165_r3_recursive_search.py` のみ。Phase 166 R3 の `typed_reference` 資格判定修正直前に作成されたバックアップ `phase166_r3_lookup_gate_fix/backups/phase165_r3_recursive_search_20261019T150915Z.py` を復元する。

復元前に現在のファイルを別名で保存し、SHA-256 一致で復元を検証する。バックアップ欠落時は復元を実施しない。構文検査のみで、全体 pytest は実施しない。

これにより Phase 166 R3 で追加した資格判定変更は取り消される。以前の引用取得経路の安全性問題も復活するため、その扱いは別途再検討する。証明生成や Web 表示の復旧は実行結果を確認するまで保証しない。
