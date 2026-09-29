Phase 146-2 Structural Capability Diagnosis

Purpose
-------
Compare the six representative group proofs without using target identity in
the proposed capability decision.

Targets
-------
pi_6^3, pi_8^5, pi_10^4, pi_12^5, pi_15^8, pi_16^9

Production changes
------------------
None.

Existing test changes
---------------------
None.

Why this diagnosis is required
------------------------------
A predicate such as "NarrativeArgument can be built" may be too broad and
could silently route pi_8^5 or another group into the pi_6^3 generic
multi-argument renderer. Phase 146 must first identify a structural capability
boundary from the current semantic/block/argument data.

Next boundary
-------------
After this matrix is reviewed, the next Phase 146 step may add the smallest
target-independent capability predicate and its focused tests.
