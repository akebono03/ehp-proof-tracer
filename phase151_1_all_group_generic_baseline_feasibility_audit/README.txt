Phase 151-1 — All-Group Generic Baseline Feasibility Audit
===========================================================

目的
----
112群すべてを、public renderer の route を変更せずに、
同一 generic renderer 経路で評価できるか確認する。

今回の変更
----------
production code: 変更なし
existing tests: 変更なし

追加する監査ファイル:
- phase151_1_all_group_generic_baseline_feasibility_audit/audit_phase151_1.py
- phase151_1_all_group_generic_baseline_feasibility_audit/run_phase151_1.ps1
- phase151_1_all_group_generic_baseline_feasibility_audit/README.txt

監査対象
--------
n = 2..15
k = 0..7
合計 112 群

各群について次の同一経路を使用する。

build_standard_toda_report
-> build_toda_group_result_proof_replay(max_depth=2)
-> build_toda_group_proof_presentation
-> build_toda_group_proof_narrative_semantic_closure_presentation
-> build_toda_group_proof_narrative_semantic_sidecar
-> build_toda_group_proof_narrative_blocks
-> build_toda_group_proof_narrative_arguments
-> render_toda_group_proof_narrative_multi_argument_with_contributions_markdown

public route は比較のため呼び出すだけで、切替・変更しない。

確認する内容
------------
- 112群すべてを列挙できること
- generic renderer が例外なく呼べること
- generic output が空でないこと
- blocks / arguments / OTHER block の総数を取得できること
- public renderer の失敗数を参考値として取得できること

Phase 151-1 では、typed reasons、raw/rule-name/type fallback の詳細分類は
まだ行わない。これらは Phase 151-2 の baseline 項目として取得する。

focused tests
-------------
- tests/test_phase144_6_public_route_cutover.py
- tests/test_phase144_6_r5_43_1.py
- tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py

full historical regression
--------------------------
実行しない。
Phase 151 の test 運用方針に従い、focused test と監査を実行する。

完了条件
--------
次のすべてを満たせば Phase 151-1 PASS とする。

1. scanned groups = 112
2. generic non-empty successes = 112
3. generic failures = 0
4. generic empty outputs = 0
5. public route を変更していない
6. production code を変更していない
7. existing tests を変更していない

Phase 151-2 との境界
--------------------
Phase 151-1 は「同一 generic route で全112群を評価可能か」だけを確認する。

Phase 151-2 で初めて、各群について次を baseline として保存・一覧化する。

- success / failure
- blocks
- arguments
- typed reasons
- OTHER
- raw fallback
- rule-name fallback
- type fallback
- exception

Phase 151-1 では renderer の文章品質を修正しない。
public renderer の全面切替、専用 renderer 削除、個別群 special case も行わない。
