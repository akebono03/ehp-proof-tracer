Phase 144-6-R5-42-R1 occurrence-downstream repair

Cause of the 175/190 failure:
R5-40 classifies an owner as a bridge when it reaches any visibility occurrence
in the same Argument. The first R5-42 production implementation incorrectly
checked only deduplicated owner steps. Fifteen owners therefore lost their
downstream evidence after the downstream occurrence was owned by another
Argument.

Repair:
1. classify selected owners using all same-Argument visibility occurrences;
2. after selection, compute placement among selected owner contributions;
3. preserve before_argument_conclusion for selected bridges without a selected
   successor;
4. keep the Phase-41 diagnostic stable key out of production ordering.

No renderer/public output change.
No full test suite in this subphase.
