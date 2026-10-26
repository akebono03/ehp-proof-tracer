# Phase 169 R4 — 現状監査の設計

## 変更対象と実行単位

- **本番コード・既存テスト・既存ドキュメント：変更なし。**
- 新規 `phase169_r4_pi64_baseline_audit/audit.py`：`stable_range_allows`、`describe_search`、`run_case`、`audit_transport` などの監査関数。
- 新規 `phase169_r4_pi64_baseline_audit/tests/test_r4_audit.py`：監査契約の限定テスト4件。
- 新規 `run.ps1`：Git 状態監視、限定 pytest、監査起動。
- 出力先は新規ディレクトリ内の `output/audit.json` と `output/audit.md`。

## GitHub develop の確認事項

2026-10-26 に確認した develop HEAD：`ff08b601badf339457ff524ca21847b5d6a67ef5`。R3Z のコミット `afb6e70c3a750224e50e8cdcd10fdb71578a6d91` が履歴に存在。

読んだ主な現行コード：`phase165_r55_nk_only_goal.py`、`phase165_r52_r9_shared_math.py`、`phase165_r3_recursive_search.py`、`phase165_r57_r7_stable_expansion.py`、`phase169_r3o_stable_composite_rule.py`、`phase165_r12_r21_eta_generator_chain.py`、`phase166_r3v_generator_transport.py`、`phase168_r3_3_proof_narrative_model.py`、`web_group_proof.py`。

既存の関連テストとして `phase169_r3o_toda45_composite_transport/tests/test_r3o_toda45_composite_transport.py` と `phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py` を確認した。

## 監査前に判明した境界

R3O の `expand_cited_toda45_composite_transport` と `toda45_composite_transport_rule` は、出発群の球面次元 $n$ と stem $k$ に $n\ge k+2$ を要求する。

$\pi_5^3$ は $n=3,k=2$ でこの条件を満たさない。したがって Toda (4.5) を使った **この既存の複合輸送規則** は $\pi_6^4$ の証明には使用できない。一方、$\pi_6^4$ から $\pi_7^5$ への輸送は $n=4,k=2$ で範囲内となる。

これは $E:\pi_5^3\to\pi_6^4$ 自体の非同型性を主張するものではない。適用可能な一般規則の範囲についてのみ述べる。

## 監査結果として必要な区別

- データベースの群構造は証明目標であり、証明済み GIVEN ではない。
- Citation の存在は証明の完成を意味しない。
- 証明の再利用は現行の文献順判定・導出証拠で確認する。
- 生成元の合成懸垂の展開候補と、群同型の証明は別の義務である。
- 候補を人工的に渡す診断は実探索の根拠に採用しない。
- R4 は read-only。次工程の修正方針は実行結果を踏まえて決定する。

## 限定 pytest と完了条件

新規4件＋既存 R3O のテスト7件を実行する。全体 pytest は実行しない。監査 JSON と Markdown が生成され、Git の追跡ファイルに新たな変更がないことを確認できれば R4 監査実行完了とする。検索の `complete` 自体は監査の完了条件ではない。

次の Phase 境界：`\pi_7^5` の実装・証明探索および Toda の安定範囲の変更はこの ZIP に含めない。
