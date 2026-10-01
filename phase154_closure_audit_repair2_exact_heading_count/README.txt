Phase 154 Closure Audit Repair2 — Exact Heading Count

Repair1 後の closure audit:
- Phase 154 focused regression: 44 passed
- ordering / reason regression boundary: 57 passed
- 112-group audit:
  - exceptions: 0
  - violations: 2
  - pi_8^5 ordering
  - pi_15^8 ordering
  - both "duplicate proof section heading"

原因
----
production defect ではなく audit false positive。

pi_8^5 / pi_15^8 の dedicated Narrative は:

- `## 証明対象`
- `## 使用する結果`
- `## 証明`

をそれぞれ1回持つ。

しかし closure audit は:

`rendered.count("## 証明")`

で数えていたため、
`## 証明対象` の先頭部分も `## 証明` として数え、
proof heading count = 2 と誤判定した。

修正
----
closure audit 内だけ変更。

substring count をやめて、
`rendered.splitlines()` 上で

`line.strip() == "## 証明"`

を exact match（完全一致）で数える。

同様に Reference heading も exact line count に統一。

production 変更
---------------
なし。

既存 test 変更
--------------
なし。

追加 verification
-----------------
pi_8^5 / pi_15^8 について:

- `## 証明対象` = 1
- `## 証明` = 1

を確認する。

その後、Phase 154 closure audit を最初から再実行する。

完了条件
--------
- dedicated-route heading verification PASS
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
