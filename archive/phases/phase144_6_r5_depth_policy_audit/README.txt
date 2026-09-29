Phase 144-6-R5 Narrative depth policy audit

本体変更なし。

対象:
- pi_6^3
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

depth 0..5 について以下を比較:
- presentation nodes / edges
- Narrative blocks
- Narrative arguments / roles
- semantic dependencies
- calculation step transitions

さらに pi_6^3 の replay node と shortest depth を表示する。

目的:
固定 depth を決めるのではなく、Narrative に必要な構造が揃う条件を
一般的に定義できるか監査する。

production code / tests / docs は変更しない。
