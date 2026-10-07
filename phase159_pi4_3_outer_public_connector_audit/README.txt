Phase 159 pi4_3 outer public connector audit

目的:
repair4 後、dangling-connector cleanup 単体では connector を
following derivation へ移せるが、actual public Narrative では
「以上より,」が消えている。

この監査では actual public route を最後まで追う。

段階:
00 base multi-argument
01 contribution renderer 完了後
02 public wrapper
03 finalizer
04 public contract normalization
05 actual public renderer

各段階で:
- pi4_3 root conclusion 数
- 「以上より,」数
- root conclusion を含む paragraph

を記録する。

注意:
repair4 は pi6_3 の既存 reason-prose test に副作用を出している。
したがって次の本修正では repair4 を撤回し、
outer pipeline の正確な消失箇所だけを修正する。

production code は変更しない。
pytest / 全体テストは実行しない。
