Phase157 R11-R11 — map-property equality semantic closure

R11-R10 監査結果:
- H-surjectivity step は raw presentation に存在。
- 直接前提 H(nu') = eta_5 も raw presentation に存在。
- しかしその導出に必要な
  H(nu') = E^2 eta_3
  E^2 eta_3 = eta_5
  は semantic closure に入っていなかった。

今回の一般修正:
- 選択済み MAP_PROPERTY step の direct premise が equality の場合、
  その equality step の direct equality premises を1段だけ closure に含める。
- pi6_3 / nu_prime / Proposition 5.3 / equality-transitivity rule name の hard-code はしない。
- renderer-side の Reference H-value 文字列挿入 call は外す。
- 既存 graph と Reference linkage に表示を任せる。

focused tests のみ実行。
full repository pytest は Phase157 closure まで実行しない。
