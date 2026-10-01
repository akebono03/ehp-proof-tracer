Phase 154 Closure Audit Repair3 — Exact Heading Order

Repair2 後の closure audit:
- Phase 154 focused regression: 44 passed
- ordering / reason regression boundary: 57 passed
- 112-group audit:
  - exceptions: 0
  - violations: 2
  - pi_8^5 ordering
  - pi_15^8 ordering
  - both "Reference section appears after proof section"

原因
----
production defect ではなく audit false positive。

Repair2 で heading count は exact line match に修正済みだったが、
heading order 判定はまだ:

`rendered.index("## 証明")`

を使っていた。

そのため:
`## 証明対象`
の先頭 substring を
`## 証明`
の位置として拾っていた。

修正
----
closure audit 内だけ変更。

`rendered_lines = rendered.splitlines()` を使い、
exact line match で:

- `## 使用する結果`
- `## 証明`

の index を求める。

production 変更
---------------
なし。

既存 test 変更
--------------
なし。

追加 verification
-----------------
pi_8^5 / pi_15^8 について:

`## 証明対象`
<
`## 使用する結果`
<
`## 証明`

を exact line index で確認する。

その後、Phase 154 closure audit を最初から再実行する。

完了条件
--------
- dedicated-route heading order verification PASS
- Phase 154 focused regression PASS
- ordering / reason regression boundary PASS
- scanned groups = 112
- rendered groups = 112
- exceptions = 0
- violations = 0

full test suite
---------------
まだ実行しない。
Phase 154 最後にのみ実行する。
