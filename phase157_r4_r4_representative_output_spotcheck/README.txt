Phase157-R4-R4 representative output spot-check

目的:
- Phase157-R4-R3 の実際の public Narrative 出力を、
  representative 5 groups で一度だけ確認する。
- Reference section が fixed statement のみになっているか確認する。
- proof-internal fact が Reference に漏れていないか確認する。
- body が残っていることを確認する。

対象:
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

実行方針:
- 各群 depth 3 を1回だけ render。
- pytest には追加しない。
- production code は変更しない。
- existing tests は変更しない。
- repository-wide pytest は Phase157 closure まで実行しない。

出力:
phase157_r4_r4_spotcheck_output/
  phase157_r4_r4_spotcheck.md
  phase157_r4_r4_spotcheck.json
  pi_8_5.md
  pi_10_4.md
  pi_12_5.md
  pi_15_8.md
  pi_16_9.md
