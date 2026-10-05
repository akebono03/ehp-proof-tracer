Phase157 R11-R11 repair4 — Reference identity/tag linkage

repair3 result:
- 55 passed / 2 failed.
- semantic closure は発火。
- H(nu') = E^2 eta_3, E^2 eta_3 = eta_5, H(nu') = eta_5 の chain は本文へ出た。
- 残り:
  1. tagged equation が Reference reuse と認識されない。
  2. (5.3) の double relation が Reference selection から落ちる。

repair4:
1. Reference statement selection
   - ProofStep object identity に加え、同じ conclusion を持つ used premise も選択。
   - semantic closure が別 ProofStep instance を使っても logical statement を保持。

2. Reference/body standalone reuse
   - 比較時だけ `\tag{N}` と末尾 `,` / `.` を無視。
   - 表示時は equation tag を保持。
   - 例:
     `[R2]より, $H(nu') = E^2 eta_3\tag{4}$.`

3. tests
   - tagged Reference linkage を確認。
   - (5.3) に double relation と Hopf relation の両方が残ることを確認。

pi6_3 / nu_prime / rule-name hard-code は追加しない。
full repository pytest は Phase157 closure まで実行しない。
