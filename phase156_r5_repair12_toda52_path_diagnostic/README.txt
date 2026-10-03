Phase 156-R5 repair12 — Toda (5.2) path diagnostic

Production changes: none.

背景
====
repair12 で Proposition 5.1 は public Reference から除外できたが、
Toda (5.2) まで同時に除外された。

これは Reference frontier の規則が強すぎる可能性を示す。

目的
====
pi_6^3 の depth 2 / 3 で、(5.2) の各 Reference step について:

- direct consumer
- frontier 判定
- internal 判定
- root までの全 path（最大20）
- path 上の Reference / rule / rendered statement

を表示する。

Proposition 5.1 との構造差を確認し、
「内部 Reference dependency」と「parent proof に必要な Reference」を
一般規則で区別するための診断。

pytest は実行しない。
repository-wide pytest も実行しない。
