Phase 159 R1-7c R4 exact-sequence suppression repair2 fix3

Finding
-------
After repair2 fix2, the required pi_6^3 exact sequence is present again.

The remaining two failures are stale Phase157 expectations.

Old expected presentation:
  $...$ は完全である.

Current public presentation:
  次の完全列を考える.
  \[
  ...
  \]

The current display-math form is the active public contract.

Change
------
Production code changes: none.

Update only:
  tests/test_phase157_r20_repair32_exactness_intro_anchor.py

The tests now verify:
- the proof introduces the displayed sequence as an exact sequence;
- the current five-term EHP sequence is present;
- it occurs before eta_6 = E eta_5;
- the old shorter bare duplicate is absent;
- the stale inline "は完全である." form is absent;
- the displayed five-term sequence occurs once.

No eta_2 wording changes.
No Reference changes.
No generator changes.
No full pytest.
