Phase 159 R1-7c R4 exact-sequence suppression repair2 fix5

Audit3 result
-------------
The current pi_6^3 public Narrative contains this exact display-math block:

\[
\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta}
\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}.
\]

It does not contain the previously assumed five-term sequence in that block.

The public Narrative also separately contains:

\[
\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}.
\]

and the short exact sequence.

Change
------
Production code changes: none.

Update only the two Phase157 stale expectations so they verify the audited
four-term display-math block.

The tests continue to require:
- "次の完全列を考える.";
- exactly one audited four-term display block;
- that block occurs before eta_6 = E eta_5;
- no old bare inline duplicate;
- no old inline "は完全である." form.

No eta_2 wording changes.
No Reference changes.
No generator changes.
No full pytest.
