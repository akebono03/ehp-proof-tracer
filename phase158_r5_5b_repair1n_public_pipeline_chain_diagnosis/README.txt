Phase 158-R5-5b repair1n — public pipeline chain diagnosis

背景
----
repair1m で確認:

- equation (1) source: transition_source=True, relocatable=False
- equation (2) source: transition_source=True, relocatable=False
- equation (3) target: incoming_sources=(eq1, eq2), relocatable=False
- relocation 対象として残るのは:
  - pi_5^2 group result
  - E injectivity

したがって repair1l の transition-source relocation guard 自体は働いている。

一方、Phase 148 の public numbered-chain tests では tag(1) が消えている。

目的
----
chain がどの public rendering stage で変化するかを特定する。

Surface:
1. base multi-Argument renderer
2. contribution renderer final output
3. public Narrative markdown
4. Web depth=2 text

Contribution transforms:
主要な string transform を wrapper で記録し、
eq1/eq2/connector/eq3 の tagged/plain count が変わる stage を出力する。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。
