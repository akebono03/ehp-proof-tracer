# Phase 165 R14-R32

## 変更対象（各ファイル全文）
- `phase165_r14_r32_hopf_isomorphism.py` 新規：`derive_hopf_isomorphism_from_steps`、`derive_adopted_tex_hopf_isomorphism`、`audit_r32`
- `test_phase165_r14_r32_hopf_isomorphism.py` 新規：対象テスト7件
- `audit.py`、`run.ps1`、`toda_51_complete.tex` 新規

## 目的
R30 で導出した Hopf 写像の全射性と R31 で導出した単射性を、既存 `map_isomorphism_rule()` と `derive_inference_proof_step()` で結合する。対象は同一の `TodaHopfInvariantMap(pi3^2,pi3^3)` に限定する。新しい一般規則、従来証明の replay、Registry の書換えは行わない。

## テスト・完了条件
対象 pytest 7件。正しい2枝なら `MapIsomorphism(H)` の `INFERENCE` ProofStep が得られ、順序逆転、写像不一致、適用方針不一致は拒否する。監査は JSON を出力する。

## 次工程
型付きの生成元対応と群構造を利用して `pi3^2=Z{eta2}` へ到達する。採用 TeX に基づく一時的な導出と厳密な Registry 引用資格は区別したままとする。全体 pytest は Phase165 最終工程のみ。
