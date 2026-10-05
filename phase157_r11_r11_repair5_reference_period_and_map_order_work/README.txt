Phase157 R11-R11 repair5 — Reference periods / map ordering

R11-R12 audit confirmed:

- (5.3) の membership / double relation / bracket definition / Hopf relation は
  4件すべて identity_used=True。
- double relation が「落ちた」のではなく、Hopf relation が最後に追加されたため
  double relation が `,` 終止になり、period を期待する test と不一致だった。
- body order は:
  pi_6^5 group -> H-surjective -> tag(4) -> tag(5) -> tag(6)
  で、proof graph の premise order と逆だった。
- graph では tag(6) が H-surjective の direct equality premise、
  tag(4), tag(5) が tag(6) の direct equality premises。

repair5:

1. Reference fixed-definition formatter
   - definition line だけ `とすると,`
   - それ以外の独立 statement はすべて `.` 終止。

2. map-property support ordering
   - presentation graph を使う。
   - MAP_PROPERTY step の direct equality premise と、
     その1段の equality premises を contiguous support block として
     map-property statement の直前へ移動。
   - 既存 pi_6^5 group-before-H-surjective ordering は維持。

3. tests
   - Reference の non-definition lines が period 終止であることを追加確認。

pi6_3 / nu_prime / rule-name hard-code は追加しない。
full repository pytest は Phase157 closure まで実行しない。
