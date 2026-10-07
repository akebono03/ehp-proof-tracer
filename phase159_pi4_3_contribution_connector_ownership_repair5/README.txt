Phase 159 pi4_3 contribution-connector ownership repair5

変更対象
========

変更:
- toda_group_proof_narrative_contribution_renderer.py
  - _contribution_insertion_indices()
  - suppress_toda_group_proof_narrative_dangling_connectors()
    - repair4 を撤回し、repair4 前の実装へ戻す

新規:
- tests/test_phase159_pi4_3_contribution_connector_ownership.py

削除:
- tests/test_phase159_pi4_3_final_connector_repair.py
  - repair4 専用テスト

import の変更
=============
なし。

根本原因
========

stage audit:

00_base_multi_argument
  P2: 以上より,
  P3: pi4_3 = Z/2{eta_3}

01_contribution_insertion
  P2: 以上より,
  ...
  P13: pi4_3 = Z/2{eta_3}

contribution insertion は conclusion の文字位置を anchor として
BEFORE_ARGUMENT_CONCLUSION contribution を挿入していた。

しかし conclusion の直前に standalone connector がある場合、
connector は conclusion の discourse ownership に属する。

従来は

  connector | conclusion

の間へ contribution を挿入してしまい、

  connector
  contributions...
  conclusion

となっていた。

その後 normalize connector が connector を最初の contribution に接続し、

  以上より, [R1]より, ...

という誤配置を作り、dangling cleanup がこれを削除していた。

修正
====

_contribution_insertion_indices() で conclusion line を見つけた後、
その直前の paragraph が

- 以上より,
- したがって,
- これより,
- これらより,

のいずれかだけからなる場合は、
conclusion anchor を connector paragraph の先頭まで後退させる。

これにより BEFORE_ARGUMENT_CONCLUSION contributions は

  contributions...
  connector
  conclusion

の順に入り、connector と conclusion の隣接関係を壊さない。

repair4 撤回
===========

repair4 は dangling cleanup 側で connector を次段落へ移す方式だったが、
pi6_3 の reason prose に

  したがって, 以上より, 完全性より, ...

のような副作用を生んだ。

根本原因が contribution insertion の ownership にあると判明したため、
repair4 は撤回する。

repair2 / repair3 は維持
========================

- generator bridge を介した group-structure semantic redundancy 判定
- redundant direct premise を provenance preservation で復活させない規則

は今回の重複解消に必要なので維持する。

テスト
======

新規:
1. BEFORE_ARGUMENT_CONCLUSION の insertion anchor が
   standalone connector の先頭になる。
2. contribution renderer 完了後も
   「以上より, pi4_3 = ...」が保持される。
3. public proof で final group conclusion が1回だけ出る。
4. proof が □ で終わる。

既存 focused regression:
- Phase 159 provenance priority
- Phase 159 generator bridge duplicate suppression
- Phase 144 contribution placement
- Phase 157 dangling connector cleanup
- Phase 50 pi4_3 inference / exactness

完了条件
========

pi4_3 public proof body の末尾が

  以上より, pi4_3 = Z/2{eta_3}.
  □

となり、pi4_3 group conclusion は本文に1回だけ現れる。

pi6_3 の既存 dangling connector / reason prose tests が再び PASS する。

次 Phase との境界
=================

今回は contribution insertion が connector ownership を壊す問題のみを修正する。

global connector prose、他 statement kind の semantic deduplication、
equation numbering の追加修正は行わない。

全体テストは Phase 159 終了時まで実行しない。
