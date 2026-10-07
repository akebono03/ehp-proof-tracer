Phase 159 pi4_3 redundant-vs-provenance audit

目的:
repair2 で quotient premise が redundant direct premise と認識されても
public Narrative に残る原因を確認する。

確認する値:
- quotient premise が redundant か
- quotient premise の block が derivation source か
- その block が preserve_provenance_block_ids に入るか
- root transition の source blocks

現在の body renderer には次の例外がある:

  block が preserve_provenance_block_ids に含まれ、
  step が redundant_direct_premise_step_ids に含まれる場合、
  その step を表示側に残す。

したがって

  redundant=True
  preserve=True

なら semantic suppression と provenance preservation の衝突が
今回の残存重複の直接原因である。

production code は変更しない。
pytest / 全体テストは実行しない。
