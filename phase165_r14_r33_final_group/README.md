# Phase 165 R14-R33

## 変更対象
新規 `phase165_r14_r33_final_group.py` に `_valid_reverse`, `_build_reverse`, `reverse_free_cyclic_transport_rule`, `pi33_cyclic_step`, `hopf_eta2_image_step`, `derive_final_group_from_steps`, `derive_adopted_tex_final_group`, `audit_r33` を全文追加。関連テスト7件全文と `run.ps1`, `audit.py`, 採用 (5.1) TeX を同梱。既存コードや規則は変更しない。

## 背景
既存 R6 の free cyclic transport は定義域→値域方向なので、その逆を使うための最小限の一般規則を追加する。R32 同型 ProofStep、Toda (5.1) の `pi3^3=Z{iota3}`、既存 `hopf_facts.ETA_2_HOPF_INVARIANT_FACT` (Proposition 5.1) を使い、`pi3^2=Z{eta2}` の最終 ProofStep を生成する。

## 完了条件
対象7テスト合格。必要な3前提からのみ推論し、対象群や対応生成元が間違っている場合は拒否する。

## 次工程との境界
採用 TeX と既存事実に基づく証明導出を確認した後、厳密な命題台帳引用資格と共通 Backward Search での証明再構築を行う。全体 pytest は Phase165 の終了時のみ。
