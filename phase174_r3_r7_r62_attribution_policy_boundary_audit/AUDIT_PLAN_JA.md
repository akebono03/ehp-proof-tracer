# Phase 174 R62 — Reference 出典選択ポリシー境界監査

## 実装前の確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` を確認。R61 に対応するコードを含む現行 HEAD はローカルの報告と整合。
- `phase168_r3_5_model_renderer.py`、`phase168_r3_3_proof_narrative_model.py`、`phase168_r3_12_body_binding.py`、Reference 投影コードと R57/R61 監査・関連テストを確認。
- R61 の実行報告：Source Guard 6件、3経路7呼出、2群の Reference 7件・3件、限定 pytest 18 PASS。ただし `SENTENCE_LEVEL_RELEVANCE_FULLY_PROVED=False`。

## 変更対象（すべて新規ファイル）

1. `phase174_r3_r7_r62_attribution_policy_boundary_audit/audit.py`：`git_blob_sha`、`source_guard`、`renderer_policy_contract`、`validate_number_set`、`hypothetical_route_choices`、`counterexample_contract`、`local_git_head`、`inspect_public_models`、`main` をファイル冒頭から新規追加。
2. `phase174_r3_r7_r62_attribution_policy_boundary_audit/tests/test_audit.py`：全11テスト関数（パラメータ化を含む）を追加。
3. `phase174_r3_r7_r62_attribution_policy_boundary_audit/run.ps1`：DryRun・公開監査・限定 pytest。
4. 同ディレクトリの `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`、`__init__.py`。

既存の `README.md`、`design.md`、`development_log.md`、`roadmap.md`、`proof_records.md` を含む既存ファイルには触れない。import、既存クラス、既存関数は変更しない。

## 監査方針

- `cited_general_ancestor_numbers`：引用可能な一般命題の `GIVEN` 祖先を型で選別。
- `direct_given_premise_citation_numbers`：直接の単一 `GIVEN` 前提で、対応する命題型が適格な場合だけ引用。
- `single_source_ancestor_numbers`：引用のある `GIVEN` 祖先が1種類のときだけ引用。
- 2件以上の祖先がある場合、無条件に全出典を文章へ付けると過剰になる。一方で一般命題の特定出典は意図的に抽出される場合がある。
- 新規 `hypothetical_route_choices` は**監査用の例示**であり、公開 Renderer を置き換える新しい規則ではない。
- 証明木所有を確認する R61 と、R57 の完成証明監査を実際に再実行する。

## 完了条件

Source Guard 7ファイル PASS、3経路7呼出の意味的ガード PASS、反例契約 PASS、両群の完成・Reference・既存証明木の検証 PASS、限定 pytest PASS、既存コード変更0、新規 GIVEN0、新規数学規則0。全体 pytest は Phase 終了まで実施しない。

## 次の Phase との境界

**無条件の共通化は行わない。** 3経路の意味が違うため、抽象的な共通祖先探索ヘルパーを作るなら、まず文章と出典付き ProofStep の1対1の対応を明示する必要がある。R62 では引用の適切さが完全に証明されたとは主張しない。
