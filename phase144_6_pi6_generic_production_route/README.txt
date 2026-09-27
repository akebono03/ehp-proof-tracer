Phase 144-6
===========

目的
----
π_6^3 の user-visible production Narrative を legacy 専用 renderer から外し、
Phase 143/144-5 の generic Semantic -> Block -> Argument -> Renderer 経路へ接続する。

変更対象
--------
1. toda_group_proof_narrative_renderer.py
   - imports
   - render_toda_group_proof_narrative_markdown()

2. tests/test_phase144_6_pi6_generic_production_route.py
   - 新規

変更しない
----------
- main.py
- web_group_proof.py
- π_8^5 / π_15^8 / π_16^9 の経路
- legacy helper/function の削除
- docs

理由:
CLI/Web は既に render_toda_group_proof_narrative_markdown() を共有している。
Phase 144-6 では public renderer 内の π_6^3 route だけを generic に切り替える。

完了条件
--------
- public Narrative(π_6^3) == generic multi-argument Narrative
- legacy π_6^3 renderer を monkeypatch で失敗させても public Narrative が成功
- CLI group-proof 3 3 --mode narrative が generic prose を表示
- legacy [R1] ベースの専用出力を production route が返さない
- focused regression が成功

Phase 144-7 との境界
--------------------
他の代表群を同じ generic renderer へ横断接続するのは Phase 144-7。
legacy 関数そのものの削除は Phase 144-9。
全体 pytest は Phase 144 最後まで実行しない。
