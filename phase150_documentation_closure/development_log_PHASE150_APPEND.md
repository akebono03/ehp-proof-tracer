---

<!-- PHASE150_CLOSURE -->
# Phase 150 — RC4 Generic provenance / reason prose 完了

Phase 150 は Phase 146 で整理した6課題のうち RC4
`Generic provenance / reason prose` を対象とした。

## 実施内容

既存 `ProofStep` provenance と semantic sidecar から、Narrative の結論を支える理由を
typed reason として扱う経路を整備した。

6代表群:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9
$$

を横断して、reason prose の存在、未型付け理由文の混入、表示位置、多重度を監査した。

## final regression 9-failure repair

Phase 150 final regression の途中で、

```text
10469 passed
9 failed
```

まで到達した。

9件の内訳は、production semantics の欠落ではなく historical display/test contract の
不一致として切り分けた。

Phase 148 関連4件は、semantic exactness evidence が proof provenance に残っている一方で、
generic Narrative が旧 literal exactness phrase を必須としなくなったことに test contract を
合わせた。

RC4-5 関連5件は visible reason multiplicity audit を行った。

共通 reason sentence の multiplicity:

```text
pi_6^3:  typed=3, rendered=3
pi_8^5:  typed=3, rendered=3
pi_10^4: typed=2, rendered=2
pi_12^5: typed=2, rendered=2
pi_15^8: typed=1, rendered=1
pi_16^9: typed=3, rendered=3
```

同一 sentence の複数出現は renderer duplication ではなく、異なる typed reason instance が
同一の汎用 prose を生成した結果だった。

Repair R2 では production code を変更せず、sentence ごとの typed reason instance 数と
rendered occurrence 数を比較する test contract へ修正した。

focused verification:

```text
RC4-5 focused regression:
9 passed in 5.65s

original nine-failure focused regression:
17 passed in 9.03s
```

## performance / full regression

Phase 150 では historical full suite が長時間化していることも確認した。
途中の performance repair は数学的 coverage を削らず、重複 setup / recomputation を対象とした。

Phase 150 最終 full regression:

```text
Python 3.10.3
pytest 9.1.1
branch: develop

10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

これにより Phase 150 の canonical closure baseline は全 test PASS で確定した。

## architectural conclusion

段階的な generic route 移行を進めた結果、複数 renderer の共存そのものが群間の表示差を生み、
代表群ごとの修正では一般化の評価が難しいことを確認した。

したがって、これ以上 group-by-group に public route を移行する方法は採らない。

次の Phase 151 では、public behavior を変えずに対象群全体を同一 generic renderer へ通し、
whole-population baseline を先に取得する。

## test operation change

Phase 150 の約42分の full regression を、今後の全 Phase で機械的に繰り返さない。

今後の標準:

```text
実装中:
focused tests

Phase closure:
focused tests + canonical regression

大きな統合点 / release:
complete historical regression
```

historical tests は直ちに削除しない。
後続で Test Suite Consolidation を行い、現在の保証を重複している test、
audit-only test、旧仕様 snapshot を分類し、canonical regression set を明示する。

## Phase 150 完了条件

```text
RC4 typed reason / prose contract established
six representative groups audited
nine final-regression failures repaired
focused repair regression PASS
10478 / 10478 full regression PASS
production proof semantics preserved
Phase 151 boundary documented
```

Phase 150 完了。

次は Phase 151 `All-Group Generic Baseline`。
