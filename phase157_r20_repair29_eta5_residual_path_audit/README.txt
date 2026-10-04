Phase157-R20 repair29 runtime audit

Purpose
-------
Trace the remaining public paragraph:

  eta_5 = eta_5

after repair28.

Known state
-----------
- eta_3^3 = eta_3^3 is now gone.
- repair25 previously showed the helper returns True for eta_5 = eta_5.

This audit traces:
- the helper result for the eta_5 bridge step;
- whether the argument-body renderer still emits it;
- each contribution-renderer transform that sees or introduces it;
- the final Narrative.

Production code changes: none.
pytest: not run.
