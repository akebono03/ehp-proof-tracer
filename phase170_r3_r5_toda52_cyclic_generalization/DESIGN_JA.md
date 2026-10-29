# Phase 170 R3-R5 — Toda (5.2) 有限巡回群輸送の一般化

## 目的と根拠

R3-R4 で、`pi_5^2`〜`pi_12^2` の8群すべてが `GOAL_AVAILABLE_PROOF_UNFINISHED` となり、全件で `proven_step_count=0` と確認された。Goal の生成自体はできている。検索結果が `COMPLETE` でないため Web も `generic-partial-proof` を表示している。

`phase165_r52_r27_r5_literature.Toda52UniversalStatement` は、$i\ge3$ における $\eta_2\circ-:\pi_i^3\to\pi_i^2$ の同型を、採用済み文献 (5.2) に基づく一般命題として登録している。しかし既存の `phase168_r2_toda52_transport.py` の展開は $i=4$ に固定されている。この差を最小変更で埋める。

## 変更対象

- `phase168_r2_toda52_transport.py`：ファイル全文を `replacement/phase168_r2_toda52_transport.py` として収録。import 部分も全文収録。
  - 変更：`expand_toda52_finite_cyclic_goal()` 全体
  - 維持：`_eta2_composition_parts()`、`_toda52_rule()` の動作
  - 新規関数：`_toda52_theorem_is_exact()`、`_typed_source_and_target()`、`_eta2_right_generator()`、`_toda52_general_rule()` を `_toda52_rule()` の直後に追加
- 追加：`phase170_r3_r5_toda52_cyclic_generalization/runner.py`、`verify.py`、`run.ps1`、`tests/test_phase170_r3_r5_toda52_cyclic.py`、`tests/test_offline_contract.py`、`README.md`、`DESIGN_JA.md`
- 他の本体・既存テスト・データ・Git index は変更しない。

## 数学的安全性

輸送元の群等式 $\pi_m^3=\mathbb Z/r\{x\}$ と Toda (5.2) が、出典審査済みの `available` に実在する場合に限って、輸送先 $\pi_m^2=\mathbb Z/r\{\eta_2\circ x\}$ を候補にする。生成元の一致は型付き合成および `HyoujiGen.csv` に基づく既存の同一性判定により確認する。`available` に存在しない DB 群構造を GIVEN に格上げしない。`InferenceRule.match_guard` は実際の2前提と結論の型・位数・生成元対応を再検証する。

今回の範囲は有限巡回群である。零群・直和群の群構造輸送、および各 $\pi_m^3$ の未完成証明を解決する機能は含めない。完成済みであることが確認されている $\pi_5^3$ から $\pi_5^2$ を輸送し、Proof Tree と Web Narrative がともに完成することを主要な成功条件とする。

## 実行と完了条件

`run.ps1 -DryRun` は本体を変更せずに HEAD・blob・差分を検査する。通常実行では、原ファイルをリポジトリ外へバックアップし、修正を適用し、限定 pytest と実際の $\pi_5^2$ の検索・Web Trust Boundary を検査する。失敗時は原ファイルをバイト単位で復元する。

- 成功：限定 pytest がすべて PASS、$\pi_5^2$ が `COMPLETE`、Web が `generic-complete-proof` で `partial_result=False`、Trust Boundary に受理されること。
- 失敗：ロールバックし、バックアップと診断を `%LOCALAPPDATA%\EHPProofTracerRecovery` に保管すること。
- 全体 pytest は Phase 170 完了時まで実行しない。

## 次段階との境界

次段階では $\pi_6^2$ 以降の輸送元 $\pi_m^3$ に証明があるかを調べ、零群・直和群を別に扱う。新たな数学的主張を自動的に採用せず、証明できた結論だけを表示する。
