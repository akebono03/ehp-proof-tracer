Phase156-R5 repair5 — final public Reference ownership diagnostic

Production changes
==================
なし。

repair4 Fixed2 で分かったこと
==============================
4群の graph data は取得できたが、
diagnostic は filtering / renumbering 前の Reference entry number を
最終 public `[R#]` と同じ番号として扱っていた。

例:
pi_12^5 の最終 public [R1] は Lemma 5.13 だが、
filtering 前 entry 1 は Proposition 5.15。

したがって番号だけでは ownership を判定できない。

repair5
=======
最終 rendered markdown の Reference header

  **[R#] locator.**

を文書全体から取得し、
locator / label title によって filtering 前 graph entry へ逆対応する。

そのうえで各 final public Reference statement について:

- public number
- title
- original entry number
- mathematical block role
- argument conclusion か
- entry-external consumer 数
- different-reference consumer 数
- proof body occurrence と前後文脈

を取得する。

raw generic route
=================
final public Reference mapping から Reference prefix の末尾を求め、
その後だけを proof body として扱う。

wrapper route
=============
`## 証明` がある場合はその直後だけを proof body とする。

完了条件
========
- target groups = 4
- exceptions = 0
- unmatched public headers = 0
- 4群すべてで final public header -> graph entry mapping 完了

次
==
取得した final public ownership data から、
各 statement を

- Reference-owned
- proof-body-owned
- mixed / aggregate

に分類する。

この診断段階では production code を変更しない。
