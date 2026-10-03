Phase157 R5-R10 repair2

目的:
- Reference 内に既存の horizontal rule があっても、Proof 直前の境界線だけを検証する。
- Web adapter が `---` を確実に separator として扱う。

変更:
- web_group_proof.py
- tests/test_phase157_r5_r10_reference_proof_boundary_qed.py

production の証明選択・Reference 選択・proof graph は変更しない。
全体 pytest は Phase157 closure まで実行しない。
