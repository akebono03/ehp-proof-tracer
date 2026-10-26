# Phase 169 R3H — (5.3) の Hopf 等式の出典接続

## 現行コード・関連テストの確認

GitHub `akebono03/ehp-proof-tracer`、監査対象 HEAD `a95940646b5554181a5ef3f70f4a8b2123badaa2`（169-3f3）。既存テスト `phase165_r52_r27_r5_typed_references/test_r5_typed_references.py` は従来の文献ブリッジが3件であることを確認するため、そのブリッジには追加しない。`phase166_r3g_toda45_registry_connection/test_r3g.py`、`phase165_r14_r5_ehp_connection/test_phase165_r14_r5_ehp_connection.py`、`tests/test_phase161_r3_backward_goal_schema.py` も確認済み。

## 変更対象

- `phase165_r52_r9_shared_math.py` の **`build_shared_typed_bridge()` 全文**を置換する。既存の8個の `sources` は元の位置に維持し、9個目の (5.3) 出典ブリッジだけを追加する。import 節の変更はない。局所 import は関数全文に含む。
- リポジトリ直下に **新規ファイル** `phase169_r3h_source_registry.py` を追加。新規関数 `build_adopted_toda53_hopf_reference()` を定数宣言の直後に配置し、ファイル全文を提示する。
- `phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py` を新規追加。6テスト関数の全文と import はファイルに収録。
- このパッケージの `apply.py`、`audit.py`、`run.ps1` を新規追加。既存の文書や既存テストは変更しない。

## 出典・証明境界

Toda 転記元 `sources/toda/Toda_05_2.tex` の (5.3) に $H(\nu')=\eta_5$ が明記される。ソース・アーカイブ `toda:tex:ch5:0005` の SHA-256 `f949b19909fdd4f60f562b1daa4b121a621a4e7a32b5461f770e1e80ada6d3f2` を厳格検査する。manifest の既知 Reference ID `toda:(5.3)` を使い、原文書順の `publication_position=8100` を既存の共通接続から引き継ぐ。Proposition 5.3 の出典に先行することを実探索で監査する。

追加する証拠は **引用された GIVEN**。命題を証明した INFERENCE へ偽装せず、未証明の終端推論規則は変更しない。Proposition 5.1 の複合命題も GIVEN のままである。従って $\pi_5^3$ の完了は主張しない。

## 限定 pytest と完了条件

`run.ps1` が実行するのは新規6テストおよび現行の文献・EHP 既存テストに限定する。全体 pytest は Phase 169 終了時のみ。

- `R3H_FOCUSED_PYTEST_EXIT_CODE=0`
- `R3H_AUDIT_EXIT_CODE=0`
- $\pi_4^2$ が `complete`、$\pi_5^3$ が `partial`
- (5.3) が文献順で `prior=True`、適切な `GIVEN` ProofStep によって検索可能
- EHP 終端規則の `INFERENCE` 条件は不変

未知のローカル変更、異なる Git blob、文献原文や型付き式の不一致は拒否する。失敗時には新規ファイルを削除し、既存の変更ファイルをバックアップから復元する。復元後の再試行は可能。

## 次の R3I との境界

R3H は引用の供給に限定する。R3I では Proposition 5.1 の複合命題と (5.3) の `GIVEN` を前提に取り得る正当な終端推論契約を、既存 API と文献順を守って検討する。この段階では先取り実装しない。
