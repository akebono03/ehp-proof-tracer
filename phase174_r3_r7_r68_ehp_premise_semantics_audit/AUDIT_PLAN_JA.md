# Phase 174 R68 — 実装前監査・境界

## 現行 GitHub の確認

`akebono03/ehp-proof-tracer` の `develop` を確認。Phase 174 R67 の TeX 修正後の `phase168_r3_27_typed_statement_projection.py` が blob `9ce32b5db34a3981649b9b9f2c5ff897eb8de831` であることを確認した。

関連実装とテスト：

- `phase174_r3_r7_r5_zero_image_hopf_injective/rule.py`、`tests/test_rule.py`：$\operatorname{Im}E=0$ と E–H 完全性から $H$ の単射性（独立した2前提）
- `phase174_r3_r7_r3_ehp_zero_rule/rule.py`、`tests/test_rule.py`：$\Delta$ の全射性、2つの完全性、末端群の零から中央群の零（独立した4前提）
- `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py`：$\Delta$ 全射性は先行群の生成元から1前提で推論
- `phase174_r3_r7_r57_narrative_source_cleanup/audit.py`：二つの公開完成証明と Reference 件数
- `phase168_r3_3_proof_narrative_model.py`、`phase168_r3_5_model_renderer.py`：証明木と共通表示
- `phase174_r3_r7_r67_zero_map_tex_arrow_fix/install.py`：正しい $\to$ の表示の公開検査

## 今回のスコープ

変更する既存ファイル・既存クラス・既存関数・既存テストはない。新規 `phase174_r3_r7_r68_ehp_premise_semantics_audit/` のみ追加。

監査では、型付き命題、ProofStep の直接の前提、GIVEN/INFERENCE の役割、証明根の祖先範囲を照合する。原文の再証明、出典追加、Narrative の変更、全20段落の意味検証は実施しない。

## 完了条件

Source Guard 11件、DryRun、2群の公開検査、R68/R3/R5/R67 の限定 pytest が PASS。全体 pytest は Phase 174 終了時のみ。

## 次の境界

R68 は2つの推論接続だけを実証する。今後の文章単位の出典適切性確認と、未監査の証明段落は別に扱う。
