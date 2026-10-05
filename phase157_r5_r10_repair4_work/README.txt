Phase157 R5-R10 repair4

目的:
- Reference/Proof 境界を finalizer の推測ではなく wrapper 自身の責務にする。
- generic route と specialized route の両方で `---` を保証する。
- pi_6^3 の legacy intro `使用する結果を先にまとめる.` を public wrapper で正規化する。

変更:
- toda_group_proof_narrative_renderer.py
- tests/test_phase157_r5_r10_reference_proof_boundary_qed.py

既存の web_group_proof.py / templates/index.html の repair2 変更はそのまま利用する。
proof graph、Reference selection、statement relevance、argument ordering は変更しない。
全体 pytest は Phase157 closure の最後だけ実行する。
