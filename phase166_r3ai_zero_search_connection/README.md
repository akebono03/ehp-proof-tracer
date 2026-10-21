# Phase 166 R3-AI: Zero Group Search Connection

変更対象:
- phase165_r55_nk_only_goal.py: search_group_from_registered_goal 全体
- phase165_r52_r2_search_adapter.py: search_registered_partial_proof 全体
- tests/test_zero_search.py: 新規テスト3件（import全文を含む）

変更後の関数全文は同梱の `*.py.txt` ファイルに収録してあります。
`apply.py` は対象関数全体を AST の行範囲を使って置換し、旧ファイルをバックアップします。
既存importの変更はありません。関数内importを使用します。

DB由来の零群Goalを共通再帰探索に渡します。
群構造DBは Goal の設定専用であり、ProofStep を作成しません。
文献の掲載順が特定できないDB Goalについては架空の citing assertion を追加せず、
既存の implicit-target citation gate を使用します。これは掲載順に基づく
「証明対象より前の全命題」検索を保証するものではありません。

Complete判定には、Goalと同一の結論を持つ実際のProofStepが必要です。
対象外の既存Relation検索経路は維持します。
`run.ps1` は限定テストのみ実行します。全体pytestはPhase末尾で実行してください。
次段階は DB Goal の文献掲載位置を別途解決する設計監査です。
