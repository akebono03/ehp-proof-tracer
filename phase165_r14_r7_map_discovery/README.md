# Phase 165 R14-R7 — Hopf Map Candidate Discovery

変更対象は新規 `phase165_r14_r7_map_discovery.py` の `CandidateMap` クラス、`discover_hopf_map_candidates()`、`_check_inverse_transport()`、`_build_inverse_transport()`、`inverse_free_cyclic_transport_rule()`、`expand_discovered_group_goal()`、`audit_hopf_discovery()` 関数と関連テスト・audit・runner。追加位置はプロジェクト直下。各ファイルには省略のない全文を含む。

群構造 Goal に対して、EHP の次数則から Hopf 写像の構造的候補を生成する。ただし候補は `STRUCTURAL_CANDIDATE_NOT_VERIFIED` であり、文献固定命題として登録・証明認証されたことを意味しない。群構造の逆輸送には同型、対象群の巡回群構造、生成元の像の3前提が必要。これらの型付き登録候補がなければ root expansion は0のままとする。

実行する pytest: `test_phase165_r14_r7_map_discovery.py` のみ。完了条件は π₃² の H 候補が1件検出され、前提なしでは ProofStep が生成されず、外部から正しく対応する前提を与えた fixture では規則の一致と導出が成立すること。全体 pytest は Phase 165 末尾のみ。

次の段階は (5.1) の対角群構造と H(η₂)=ι₃ の出典照合・型付き登録、EHP 単射・全射の根拠を正式に接続すること。今回の実装は数学的証明の完成を宣言しない。
