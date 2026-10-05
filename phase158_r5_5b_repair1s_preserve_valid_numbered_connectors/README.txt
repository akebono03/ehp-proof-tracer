Phase 158-R5-5b repair1s — preserve valid numbered connectors

原因
====
repair1r で equation-number normalization helper の仕様を確認した。

この helper は:
- connector が参照している tag だけを保持する
- connector から参照されない tag は削除する

現在は helper より前に
suppress_toda_group_proof_narrative_dangling_connectors()
が `(1) と (2) より,` を削除しているため、
referenced_numbers が空になり tag(1), tag(2) まで消えている。

Phase 157 の dangling cleanup は番号付き connector を
paragraph 末尾にあるだけで dangling と判定していた。

しかし equation derivation では:

eq1 paragraph
eq2 paragraph
connector paragraph
derived equation paragraph

という構造が正しい。

修正
====
番号付き connector は次の場合に保持:
1. connector が参照する全 tag が前方に存在
2. 後方に導出結果となる math paragraph が存在

それ以外は dangling として削除。

standalone connector:
- 以上より,
- したがって,
- これより,
- これらより,

については従来どおり dangling cleanup を維持。

変更対象
========
Production:
- toda_group_proof_narrative_contribution_renderer.py
  - suppress_toda_group_proof_narrative_dangling_connectors()

Production import changes:
なし。

Tests:
- tests/test_phase157_r20_repair43_dangling_connector_cleanup.py
  - stale numbered-connector blanket prohibition を削除
  - valid numbered connector preservation test を追加
  - unreferenced numbered connector suppression test を追加

Phase boundary
==============
repair1s は connector validity のみ修正する。

eq3 の tag(3) が未復元なら、
それは次の独立した equation-numbering issue として扱う。

repository-wide pytest:
実行しない。
