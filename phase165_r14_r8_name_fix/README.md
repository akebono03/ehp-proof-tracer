# Phase 165 R14-R8 — Generator Name Normalization Fix

## 変更対象
- `phase165_r14_r8_source_link.py`: `dataclasses` import, `homotopy_groups` import, `find_pi33_source_candidate()` 全体。
- `test_phase165_r14_r8_source_link.py`: 回帰テスト `test_normalized_diagonal_preserves_generator_structure()` を追加。
- `audit.py`, `run.ps1` は元の R14-R8 と同一。

## 原因と対応
R14-R2 の対角群生成元は `name="ι_3"`、既存 `hopf_facts.IOTA_3` は `name="ι₃"` で、dataclass 等価比較が失敗した。次数・source・target・GeneratorSymbol を一致確認した上で、既存の canonical generator に正規化する。

## テストと完了条件
従来の5件と追加1件の targeted pytest、監査で `root_expansions=1`, `proof_steps_created=0`, `source_certified=false` を確認。全体 pytest は実行しない。

## 次段階との境界
出典認証、登録済み ProofStep 生成、EHP 完全性の導出は対象外。
