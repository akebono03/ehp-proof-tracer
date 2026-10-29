# Phase 170 R3-R1 — 未完成証明の原因切り分け監査

## 目的

R1 で `SEARCH_FAILED`、R2 で `SOURCE_ORDER_OR_CITATION_DIAGNOSTIC` と記録された次の5群について、保存済みの実測記録を読み取り、現在の本番 Goal 選択・出典審査経路と照合する。

$$\pi_6^3,\quad\pi_7^4,\quad\pi_8^5,\quad\pi_8^4,\quad\pi_9^5$$

## 監査対象のコードと関数

本体には変更を加えない。読み取り対象は `phase165_r55_nk_only_goal.py` の `registered_group_goal_candidates`、`phase166_r3t_goal_source_binding/goal_source.py` の `resolve_specialized_goal_citing_id`、`phase165_r52_r16_web_citation_gate.py` の `screen_shared_proof_context`、`phase169_r10e2_unpositioned_citation/source_first.py` の `screen_independent_sources_for_derived_goal` など。

新規パッケージに `audit.py` の `preflight`、`load_reports`、`load_trace`、`infer_frontier`、`inspect_source_screen`、`report_case`、`markdown`、`run`、`main` と補助関数を追加。新規 `tests/test_audit.py` に限定テストを追加する。

## 判定基準

型付き Goal 未登録、複数候補、固定命題の掲載位置を持つ引用 ID の有無、独立した出典審査経路、出典審査済み候補、実測された ProofStep、未解決 Goal を区別する。

出典審査済み候補が存在しても、その候補を使用した証明が完成したとは評価しない。引用 ID が無い場合も、独立した導出経路が存在する可能性を維持する。

不足している Toda 命題・新規推論規則・Renderer の欠陥は、この監査だけでは確定しない。実際の Backward Search の再実行や規則の追加は今回の範囲外。

## 安全境界

`AUDIT_ONLY`。GitHub で確認した本体コードの blob ID、R1・R2 の HEAD と監査資料の整合、`develop` の祖先関係、監査専用コミット以外の変更の不在を確認する。データベース CSV の未コミット変更も拒否する。

既存の Git tracked ファイル、index、既存テスト、出典台帳、Proof Tree には変更を加えない。`reset`、`restore`、`clean`、`git add` は呼ばない。全体 pytest は Phase 170 終了時まで実行しない。

## 完了条件と次工程

保存された R1・R2 の12群と、未完成5群の実測トレースが整合し、現行の出典審査結果が記録され、Git tracked/index が維持されたとき、R3-R1 の診断実行を完了とする。

次の R3-R2 で、実際に不足する型付き展開候補・数学的前提をさらに精査するか判断する。証明の完成化や新規規則実装は先取りしない。
