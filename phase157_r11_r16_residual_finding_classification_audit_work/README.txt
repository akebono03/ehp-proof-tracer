Phase157 R11-R16 — Residual Finding Classification Audit

R11-R15:
- 112 groups scanned
- exceptions 0
- 15 findings
- 6 affected groups

目的:
15 findings をそのまま修正せず、実 defect / presentation candidate /
Reference ancestry candidate に分類する。

対象群:
- pi_6^3
- pi_10^4
- pi_8^5
- pi_12^5
- pi_15^8
- pi_16^9

分類内容:
- standalone connector の前後 paragraph context
- repeated numeric equality
- public Reference without body marker の各 statement と direct consumer
- hidden zero-map statement の consumer
- E injectivity 後の four-term EHP sequence context

Reference classification:
- needed_but_marker_missing
- needed_for_root_but_marker_missing
- ancestry_only_candidate
- no_visible_direct_consumer_candidate
- entry_lookup_failed

production/test code は変更しない。
pytest は実行しない。
full repository pytest は Phase157 closure まで実行しない。
