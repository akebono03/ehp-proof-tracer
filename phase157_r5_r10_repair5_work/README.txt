Phase157 R5-R10 repair5

原因:
1. テストの `## 証明` 検索が `## 証明対象` を誤って先に拾っていた。
2. pi_6^3 の Reference section は
   `toda_group_proof_narrative_contribution_renderer.py`
   で実際に public body へ連結されており、後段 wrapper で再構成する方式では一致しなかった。

修正:
- generic contribution renderer 自身が
  `# Group proof narrative`
  `## 使用する結果`
  `---`
  `## 証明`
  を出力する。
- テストは exact proof heading `\n## 証明\n` を検索する。

変更対象:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r5_r10_reference_proof_boundary_qed.py

proof graph、Reference selection、statement relevance、argument ordering は変更しない。
全体 pytest は Phase157 closure の最後だけ実行する。
