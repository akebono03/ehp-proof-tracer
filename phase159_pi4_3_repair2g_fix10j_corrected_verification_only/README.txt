Phase 159 repair2g fix10j

Purpose
-------
Verify the already-applied fix10i production repair with corrected audit
string literals.

Why fix10i audit failed
-----------------------
The rendered pi_3^2 public Narrative visibly satisfied the requested
contract, but the audit script searched for double-escaped text such as
literal "\\n" and "\\[" sequences.

That produced a false negative.

Production changes
------------------
None.

Existing test changes
---------------------
None.

Verification
------------
1. pi_3^2 public Narrative:
   - numbered injective display math (1)
   - numbered surjective display math (2)
   - terse zero-map wording
   - terse isomorphism wording in Reference and proof body
   - no inline \tag{1}/\tag{2}

2. pi_4^3 Reference:
   - [R1] (5.1)
   - pi_4^5 = 0
   - pi_5^5 = Z{iota_5}
   - [R2] Proposition 5.1
   - pi_3^2 = Z{eta_2}
   - Delta(iota_5) = +/- 2 eta_2
   - no Proposition 4.2 / EHP exactness Reference leakage

3. Focused pytest:
   - pi_3^2 Narrative contract
   - repair2g Reference policy
   - repair1 / repair1c health checks

Repository-wide pytest is not run.
