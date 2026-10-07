Phase 159 pi4_3 connector position stage audit

目的:
repair3 後、pi4_3 の「以上より,」は stage 21 時点で
最終結論ではなく [R1] paragraph に付着していることが判明した。

この監査では stage 00〜21 について:
- connector を含む paragraph index
- root conclusion を含む paragraph index
- それぞれの前後 paragraph

を出力する。

判定:
connector と root が最初に離れる stage が、
今回の connector misplacement の原因層である。

production code は変更しない。
pytest / 全体テストは実行しない。
