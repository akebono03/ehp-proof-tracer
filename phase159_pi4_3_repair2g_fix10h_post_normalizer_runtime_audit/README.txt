Phase 159 repair2g fix10h audit

Purpose
-------
Find the exact runtime stage that introduces public \tag{1}/\tag{2}
map-property numbering after
_phase158_normalize_public_equation_numbers().

Confirmed before this audit
---------------------------
- Only one runtime definition of
  _phase158_normalize_public_equation_numbers() exists.
- Its input contains no \tag markers for the pi_3^2 injective/surjective
  map-property lines.
- Its output also contains no \tag markers.
- The final public Narrative nevertheless contains \tag{1}/\tag{2}.

This audit:
1. prints the runtime source of
   _phase158_normalize_public_narrative_contract(),
2. prints all local renderer functions whose source contains tag or
   map-property wording tokens,
3. replaces the injective/surjective output of the equation normalizer
   with unique sentinel lines,
4. renders pi_3^2 and checks whether those sentinels survive.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
