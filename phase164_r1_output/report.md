# Phase 164 R1 — 接続監査

既存 Production コードへの変更なし。

## モジュール

- registry: `unified_statement_registry.py` — 確認可能
- bridge: `phase163_r4_registry_bridge.py` — 確認可能
- archive: `phase163_source_archive_registry.py` — 確認可能
- goal: `phase161_r5_backward_proof_reconstruction.py` — 確認可能
- matching: `phase161_r4_literature_premise_matching.py` — 確認可能
- provenance: `phase161_r7_premise_provenance_validation.py` — 確認可能
- proof: `proof.py` — 確認可能
- inference: `repository_inference.py` — 確認可能
- renderer: `phase162_validated_proof_presentation.py` — 確認可能

## 接続設計

1. R2 で引用資格を判定する独立した境界を設ける。
2. R3 では既存 ProofStep を渡す経路を利用し、新しい探索器を作らない。
3. `SOURCE_ARCHIVE`、metadata-only、未確認の掲載順は自動承認しない。
4. `PROOF_INTERNAL` は祖先証明の検査なしに文献固定事実へ昇格しない。
5. R4 では E:π₄²→π₅³ の7規則と4つの完全性証人を維持する。

## テスト候補

- `tests/test_phase163_r2_unified_registry.py`: あり
- `tests/test_phase163_r3_registry_validation.py`: あり
- `tests/test_phase163_r4_registry_bridge.py`: あり
- `tests/test_phase161_r5_backward_proof_reconstruction.py`: あり

全体 pytest は未実行。数学的真偽や引用資格の確定は R1 の対象外。
