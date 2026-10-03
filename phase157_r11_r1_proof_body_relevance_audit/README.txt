Phase157 R11-R1 — Proof body relevance audit

目的
====
R10 完了後の実際のローカルコードを使い、pi_6^3 の証明本文で次を監査する。

1. 不要候補:
   E: pi_4^2 -> pi_5^3
2. 必要候補:
   pi_6^5 = Z/2{eta_5}
3. 各 statement がどの argument / ordered contribution に属しているか。

この R11-R1 は audit-only。
production code と test code は変更しない。
pytest も実行しない。

出力
====
- コンソール:
  - proof body の番号付き全文
  - fragment match
  - arguments
  - ordered contributions
- output/pi6_3_rendered.md
- output/pi6_3_body.md

次
==
監査結果から generic relevance / placement rule を1つに絞って R11-R2 を実装する。
