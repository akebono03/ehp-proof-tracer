Phase157-R20 repair16

Purpose
-------
Fix the next visible generic proof-order defects after R1-R5 Reference recovery.

Production changes
------------------
1. Preserve the eta suspension bridge literally:
     eta_(n+1) = E eta_n
   Do not canonicalize the RHS suspension into eta_(n+1), which created a
   useless reflexive equation.

2. Suppress proof-graph-backed reflexive equality paragraphs generically when
   Relation(lhs=rhs) is an equality.

3. For visible surjective H map properties, move a kernel/image exactness
   reason involving the same target group to after the surjectivity conclusion
   and after the following exactness paragraph.

Test maintenance
----------------
- Phase157-R19 expected `(5.3)` definition wording is updated from the old
  `とする.` to the current definition connector `とすると,`.
- Phase156's old premise that Proposition 5.1 is internal-only is obsolete:
  Phase157 now uses pi_6^5=Z/2{eta_5} publicly in the final short exact
  sequence. The historical regression is updated to require the current five
  proof-required public References.

Phase boundary
--------------
This repair does NOT yet add:
- the explicit E(eta_2^3)=eta_3^3 != 0 order reason;
- the fully expanded Proposition 2.2 / Equation (5.7) calculation chain;
- broad prose de-duplication.

Those remain Phase157 work after this focused result is inspected.

Repository-wide pytest is not run.
