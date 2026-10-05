Phase157 R11-R9 — Hopf surjectivity dependency audit

R11-R8 で確認:
- (5.3) entry 自体には nu_prime_hopf_relation が入る。
- しかし statement line selection で H(nu') = eta_5 が表示されない。
- final public Reference は R1 Proposition 5.6, R2 (5.3), R3 Proposition 5.3。
- H(nu') と nu' membership は R2 由来であるべき。

今回の目的:
H: pi_6^3 -> pi_6^5 surjective step が、
H(nu') = eta_5 および pi_6^5 = Z/2{eta_5}
を proof dependency として本当に持っているか確認する。

出力:
- exact rule name
- rendered statement
- literature boundary / component
- presentation graph inclusion
- direct premises
- direct consumers
- source file occurrences
- identity-based direct premise checks

production/test code は変更しない。
pytest は実行しない。
