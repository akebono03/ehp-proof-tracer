Phase 159 - pi_4^3 repair3c fix5
Four-fact selection-stage diagnosis

目的
----
fix4 で pi_4^3 の必要4事実の状態が以下と判明した。

current selected:
- TodaDeltaImageUpToSignStatement: True
- TodaDeltaImageFreeCyclicStatement: True
- TodaSuspensionKernelFreeCyclicStatement: False
- TodaSuspensionSurjectiveStatement: False

fix5 では各 fact がどの段階で失われるかを確認する。

確認段階
--------
- local body に存在するか
- hidden candidate か
- repair3c chain に含まれるか
- necessity が非空か
- provider key を持つか
- base public markdown に既出か
- fallback rendering か
- visibility occurrence に入るか
- dedup owner になるか
- final selected contribution に入るか
- 最寄りの already-public downstream descendant は何か

狙い
----
ker E / E surjective が、

1. occurrence 前で落ちる
2. grouping / owner で落ちる
3. selected-owner relevance で落ちる

のどこかを確定する。

また、already-public downstream descendant が存在する場合、
「hidden prerequisite -> already-public dependent fact」という一般的 linkage を
selection boundary として利用できる可能性を評価する。

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
実行しない。
repository-wide pytest も実行しない。

完了条件
--------
pi_4^3 の4事実すべてについて selection pipeline の状態が確定すること。
その結果を見るまで production selection は変更しない。
