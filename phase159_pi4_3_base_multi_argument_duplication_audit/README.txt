Phase 159 pi4_3 base multi-argument duplication audit

目的:
stage audit により、pi4_3 root conclusion の重複が
00_base_multi_argument の時点ですでに存在することが判明した。

この監査では argument ごとに次を確認する。

- conclusion block
- conclusion step が root step か
- local_body_blocks
- root block の local occurrence 数
- argument body 内の root conclusion 出現数
- transition connector

判定:
- 1つの argument body だけで root_count=2 なら body renderer 内重複。
- 異なる2 argument で root_count=1ずつなら argument ownership / local body 境界重複。
- actual base output だけ2なら multi renderer 結合段階の問題。

production code は変更しない。
pytest / 全体テストは実行しない。
