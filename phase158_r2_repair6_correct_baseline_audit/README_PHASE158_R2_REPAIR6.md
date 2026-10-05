# Phase 158-R2 repair6

## 目的

production code は変更しない。

repair4 で導入済みの wrapper を、R2直前 baseline と正しく比較する。

## repair5 の失敗原因

1. baseline の `## 使用する結果` と `## 証明` の間には、
   Phase 157 ですでに `---` が存在する。
   これは Reference payload ではなく public shell なので、
   baseline comparison では除外する必要がある。

2. local pre-R2 baseline の pi11_4 は
   `[R3]より, $\nu_4$ の分解写像は同型写像である.`
   である。
   GitHub 上の古い `[R2]` expectation を Phase 158 で復活させない。

## 比較規則

baseline と normalized の双方から以下だけを除外して比較する。

- Reference/Proof separator `---`
- terminal QED marker (`$\square$`, `□` など)
- Phase 158 が追加した section shell

Reference 本文と Proof 本文は完全一致を要求する。

## 完了条件

- public contract valid: 112
- Reference payload preserved: 112
- Proof payload preserved: 112
- fully valid: 112
- exceptions: 0

全体 pytest は Phase 158 最後のみ。
