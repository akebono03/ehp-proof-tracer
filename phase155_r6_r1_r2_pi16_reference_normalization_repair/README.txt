Phase 155-R6-R1-R2 — pi16 Reference normalization stale expectation repair

Why R2 is needed
----------------
The R6-R1 repair correctly fixed the Phase144 heavy audit test, which then
passed.

The remaining pi16_9 test failed earlier than the Reference-name assertions:
the current renderer does not emit the old `## 使用する結果` section heading
for this route. It emits:

    使用する結果を先にまとめる.

followed by normalized `[R#]` Reference entries.

The local current output also differs from older Phase154 snapshots in which
specific Reference names were fixed. Therefore R2 stops freezing exact
Reference names in this old Phase150 normalization test.

Changed file/function
---------------------
tests/test_phase150_rc4_7a_cross_group_reference_normalization.py

test_phase150_rc4_7a_pi16_9_numbers_normalized_references

The function now checks only:
- the current Reference-introduction sentence,
- presence of normalized `**[R1] ...` / `[R1]` markup.

It does not require:
- `## 使用する結果`,
- Proposition 5.15,
- Lemma 5.14,
- Theorem 3.6,
- Lemma 5.13.

This keeps the old test focused on Reference numbering/normalization and does
not implement Phase156 Reference relevance/minimal-display behavior.

Execution behavior
------------------
- only this one focused test is run before resume;
- the 26-second Phase144 test is not repeated;
- all 21 collection batches remain checkpointed;
- after focused PASS, only the two saved FAIL runtime checkpoints are removed;
- R6 then resumes and re-runs runtime probes 9 and 10 only.

No production code changes.
No import changes.
No canonical regression.
No repository-wide pytest.
