---

<!-- PHASE150_CLOSURE -->
# 34. Phase 150 完了境界 — generic provenance / reason prose

Phase 150 は Phase 146 で RC4 と分類した `Generic provenance / reason prose`
を対象とした。

数学的 ground truth は引き続き次である。

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

Phase 150 の reason layer は、これらの既存 provenance から Narrative に必要な
「なぜこの結論を述べられるか」を型付きで表す presentation-side structure である。

```text
typed Narrative reason
!= new theorem fact
!= new proof edge
!= new proof search
!= theorem ranking
```

reason prose は typed reason から生成する。複数の異なる typed reason instance が
同一の汎用 sentence を生成する場合がある。その場合、文字列を一意化して1回だけ表示することを
正しさの条件にはしない。

正しい表示契約は sentence $s$ ごとに

$$
\#\{\text{typed reason instances rendering to }s\}
=
\#\{\text{occurrences of }s\text{ in Narrative}\}
$$

である。

6代表群の multiplicity audit では、問題となった共通 sentence について次を確認した。

```text
pi_6^3:  typed=3, rendered=3
pi_8^5:  typed=3, rendered=3
pi_10^4: typed=2, rendered=2
pi_12^5: typed=2, rendered=2
pi_15^8: typed=1, rendered=1
pi_16^9: typed=3, rendered=3
```

したがって Phase 150 final repair は production renderer を変更せず、historical test contract
を instance multiplicity に合わせた。

## renderer-route 境界

Phase 150 では段階的 generic route 移行を進めた結果、複数 renderer の共存そのものが
群間の表示差を生み、代表群ごとの修正では一般化の評価が難しいことを確認した。

したがって Phase 150 では group-by-group migration を継続しない。

```text
Phase 150
→ RC4 reason semantics / prose の確立
→ route coexistence を architectural pressure として確認
→ incremental migration をここで停止

Phase 151
→ whole-population generic baseline
```

Phase 151 では対象群を同じ generic renderer へ強制的に通して観測するが、
public renderer selection は変更しない。

```text
generic baseline audit
!= public route switch
!= dedicated renderer deletion
!= legacy fallback deletion
```

## test strategy

Phase 150 final full regression は closure baseline として全 `tests` を1回実行した。

```text
10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

この約42分の historical full suite を、今後すべての Phase 終了時に必須とはしない。

通常の開発サイクルは次とする。

```text
RC / repair
→ focused tests

Phase closure
→ focused tests
→ maintained canonical regression

major integration / release milestone
→ complete historical regression
```

test suite 自体についても、後続 Phase で現在の保証を重複して検証する historical test、
audit-only test、旧 renderer contract を整理し、canonical regression を明示する。

ただし test 数の削減そのものを目的とせず、現在の仕様・数学的 provenance・public API の
保証を維持することを優先する。

## Phase 151 境界

Phase 151 は `All-Group Generic Baseline` とする。

目的:

```text
同一 population
→ 同一 generic route
→ 同一 depth / observation conditions
→ success / failure / fallback / semantic inventory を一括取得
```

Phase 151 では generic renderer の欠陥をその場で群別修正しない。
まず全体像を取得し、欠陥分類を次 Phase の入力とする。

---

# 35. 現行 regression 方針

旧方針の「Phase 終了時に必ず repository-wide full regression」は Phase 150 closure をもって
運用上の標準から外す。

現行方針:

```text
focused regression
→ 日常の実装・repair

canonical regression
→ Phase closure の標準

complete historical regression
→ renderer 統一、public API 大変更、release 等の大きな節目
```

完全な historical suite は削除せず、必要な節目で再実行できる状態を維持する。
