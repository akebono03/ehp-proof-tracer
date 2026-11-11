# Phase 174 R63 — 特定文章の出典証人監査

## GitHub 現行コードと関連テストの事前確認

- `akebono03/ehp-proof-tracer`、`develop`、現行コードの Git Blob SHA を確認。
- 共通 `phase168_r3_3_proof_narrative_model.py`（引用番号の所有）と
  `phase168_r3_5_model_renderer.py`（3種類の文章レベル出典選択）を確認。
- `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py`（生成元から Δ 全射性を導く1前提規則）を確認。
- R57 公開証明監査、R60 所有関係監査、R61 経路監査、R62 各経路の意味の相違と限定テストを確認。
- HEAD を固定すると監査ファイル追加だけで再失敗するため、7ファイルの Blob SHA を固定する。

## 変更対象

既存ファイル・既存 API・既存テスト・主要5文書の変更は0。
新規 `phase174_r3_r7_r63_sentence_witness_audit/` のみ。

- `audit.py`：7ファイル Source Guard、Verified ProofStep 祖先走査、表示文章と出典番号の対応、二群の対象文章を検査。
- `tests/test_audit.py`：独立した負例・祖先一意性・本文探索・Source Guard 回帰テスト。
- `run.ps1`：DryRun / 本実行 / 限定 pytest。pytest キャッシュを更新しない。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## 対象と限界

1. 両群：Proposition 4.2 の一般 GIVEN に基づく EHP 完全列の表示。
2. `π_11^6`：Toda (5.10) の引用と検証済み GIVEN。
3. `π_11^6`：Proposition 2.7 の型付き具体化、引用と検証済み GIVEN 祖先。
4. `π_12^7`：先行データベース GIVEN 1前提からの Delta 全射性。

表示の出典番号が Verified Proof Tree に由来することと、**文章の数学的適切性全体**とは異なる。
今回の監査で確認するのは対象文章の限定的な依存関係まで。
それ以外の文章、一般的な多重前提の寄与の十分性、他の群については完全監査と宣言しない。

## 完了条件

- Source Guard 7件と DryRun PASS。
- 上記4種類の引用経路が、実際に型付き GIVEN 祖先と表示行を持つ。
- `π_11^6` は Reference 7件、`π_12^7` は3件を維持。
- 限定 pytest PASS。全体 pytest は Phase 末尾のみ。
- 新規 GIVEN・数学規則・Production 変更とも0。

## R64 との境界

この監査で未確認と判明した文章のうち、どの表示だけに個別の出典根拠が不足するかを特定してから、必要な共通構造を設計する。
全引用を無条件に統合する実装、Narrative 専用規則、結論 GIVEN は加えない。
