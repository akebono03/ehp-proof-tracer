---

# Phase 144 — generic Narrative / ownership-boundary audit closure

Phase 144 は、Phase 143 の semantic Narrative を「statement 単体」ではなく
「証明全体」として一般化できるかを監査した。

## renderer route comparison

代表群

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9
$$

について legacy / generic route を比較した。

初期比較では、$\pi_6^3$ は専用 Narrative の情報量が多い一方、他群では generic
renderer が semantic statement を多く表示するケースがあり、単純な文字数比較では
一般化の完成度を判定できないことを確認した。

## semantic / argument generalization

Phase 144-6 では次を段階的に監査した。

```text
definition relevance
argument ownership
direct-premise frontier
semantic closure
complete replay
contribution ordering
topological determinism
Narrative participation
detached argument boundary
entry classification
```

complete replay API により、explicit positive depth の Narrative で bounded replay 外の
semantic dependency を参照できる基盤を確認した。

一方、depth 0 まで complete replay に切り替わる regression が最終確認で見つかり、
`main.py` の complete-replay 条件を `max_depth > 0` に限定して depth 0 semantics を復元した。

## R25-30-R3 cutoff

R25-30-R3 を Phase 144-6 の技術調査 endpoint とした。

current six-group inventory:

```text
pi_6^3:  selected=6 participating=6/6 detached=0/0 transport=1 missing=0
pi_8^5:  selected=10 participating=7/7 detached=3/3 transport=1 missing=0
pi_10^4: selected=22 participating=0/0 detached=22/0 transport=2 missing=0
pi_12^5: selected=46 participating=2/2 detached=44/0 transport=4 missing=0
pi_15^8: selected=54 participating=10/10 detached=44/0 transport=4 missing=0
pi_16^9: selected=54 participating=10/10 detached=44/0 transport=4 missing=0

TOTAL selected=192
TOTAL participating=35
TOTAL detached=157
TOTAL detached_insertable=3
TOTAL missing=0
```

R25-30-R3 focused:

```text
10 passed
```

production-route controls:

```text
13 passed
```

boundary classification と existing child Argument pair は対象3ケースですべて一致した。

ここで、$\pi_{15}^8$ / $\pi_{16}^9$ の巨大な group-structure / definition Narrative は
ownership-boundary leak ではなく、owned entry の proof subtree を再展開する
result-reuse problem と分類した。この問題は Phase 144 では解かず、Phase 146 以降の
具体的課題へ送った。

## final regression repair

有効な canonical whole-suite runner は

```powershell
python -m pytest tests -q
```

を `PYTHONPATH=<repo>;<repo>/tests` と package import を成立させた環境で実行した。

final repository-wide result:

```text
10298 collected
10273 passed
25 failed
2321.20s (0:38:41)
```

25 failures は R5-39〜R5-43 の historical completion / fixed-count snapshot に集中した。
代表的な drift は

```text
190 → 192 selected
33 → 35 participating
pi_6^3 contribution count 5 → 6
detached_insertable 0 → 3
```

だった。

これらを current gate として production を旧状態へ戻すことはせず、historical snapshot
tests を structural invariant へ maintenance した。新しい `192` 等を固定 snapshot として
埋め込むこともしなかった。

R3 focused regression:

```text
66 passed in 1308.82s (0:21:48)
```

production renderer changes:

```text
none
```

R3 後は whole repository suite を再実行していない。Phase の全体テストは Phase 最後に
一度だけという運用を維持し、closure evidence は上記 final suite と R3 focused regression
の組として記録する。

## Phase 144 completion boundary

完了条件:

```text
generic Narrative route の現状を監査済み
complete replay API の必要境界を確認済み
depth 0 semantics を維持
argument ownership / boundary classification を確認済み
R25-30-R3 を調査 endpoint として確定
historical R5 snapshot を current semantic gate から分離
result-reuse problem を次 Phase 群へ明示的に分離
final whole-suite failures を focused maintenance で解消
```

Phase 144 完了。

次の Phase 145 は Narrative + depth 2 の default 化だけを扱う。
