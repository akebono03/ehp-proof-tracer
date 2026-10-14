Phase 165 R27-R8 - Legacy group query and CLI caller migration

変更するファイル
- web_group_query.py: import 節、build_standard_web_group_query_view() 全体
- main.py: _run_group_proof_command() 全体、main() 全体のうち通常 Group query の末尾（それ以外のサブコマンドは厳密に維持）
- phase165_r27_r8/test_phase165_r27_r8.py: 新規テスト4件

差し替え単位
- web_group_query_IMPORTS_FULL.py.txt: 変更後の import 全文
- web_query_function.txt: 変更後の Web 関数全文
- cli_proof_function.txt: 変更後の CLI Group proof 関数全文
- main() は install.py が既存関数を読み、従来のすべてのサブコマンド処理を維持して通常計算部のみ cli_normal_query_tail.txt の実装へ置き換える。書き換え後も main() 全体を compile で検証する。

対象テスト
python -m pytest -q phase165_r27_r8/test_phase165_r27_r8.py
全体 pytest は Phase 165 最終段階に限る。

完了条件
1. Web Group query が build_standard_toda_report を使わない
2. CLI の通常 Group query と group-proof が旧 Report / replay を使わない
3. SEARCH_FAILED / PARTIAL を FOUND、証明完成、□ に昇格させない
4. その他の CLI サブコマンドを変更しない

次 Phase との境界
- main.py に残る旧関数 import や web_group_proof.py、旧 Repository 本体の削除は未実施。
- 旧 Group query の完成済みとされていた結果は、新方式の型付き証明が揃うまで NOT_FOUND になる場合がある。これは意図した fail-closed 動作。
- n=1,k>=0 等、共通探索未対応の入力は NOT_FOUND とする（境界/負次元の既存判定は維持）。
