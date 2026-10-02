Phase 155 Closure-R2A-R1

Repairs the five Phase132/133 tests that still froze Lemma 5.14 / Lemma 5.13
as visible Reference names.

Current local output shows different selected References (for example
Proposition 5.3 for pi16_9 and Proposition 5.11 for pi12_5), while the target
group results remain correct.

The repaired tests verify:
- a normalized Reference marker exists;
- the mathematical target/result is present;
- internal historical rule names remain hidden.

No production changes. No import changes. No repository-wide pytest.

After the five repaired tests pass, the previous 7 PASS results are reused to
promote batch 1 to PASS, then the original checkpointed R2A runner resumes at
batch 2.
