Phase157 R5-R10 repair3

目的:
- pi_6^3 generic route も他の public route と同じ
  `使用する結果 -> 区切り線 -> 証明` 構造にする。
- specialised route も Proof 見出し直前の区切り線を exact に正規化する。
- 証明末尾 QED は既存 R10 finalizer を維持する。

変更:
- toda_group_proof_narrative_renderer.py
- tests/test_phase157_r5_r10_reference_proof_boundary_qed.py

web_group_proof.py と templates/index.html は repair2 の状態をそのまま利用する。

proof graph、Reference selection、proof body relevance、argument ordering は変更しない。
全体 pytest は Phase157 closure まで実行しない。
