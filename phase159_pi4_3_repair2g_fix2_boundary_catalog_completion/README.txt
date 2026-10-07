Phase 159 pi_4^3 repair2g fix2
===================================

Purpose
-------
Repair the two concrete failures observed after repair2g fix1:

1. (5.1) was classified as FIXED_STATEMENT with component key
   basic_sphere_group_relations, but the fixed-component catalog did not
   contain the corresponding (5.1) component, causing KeyError.
2. The Phase49 focused test incorrectly assumed exactly two (5.1)-tagged
   GIVEN steps. The accumulated local contract already contains three.
   The repaired test checks the two mathematically required foundational
   conclusions instead of an exact count.

Production changes
------------------
- toda_literature_statement_boundary.py
  Ensure (5.1) / basic_sphere_group_relations is registered in
  _FIXED_COMPONENTS_BY_REFERENCE.
  Keep the existing fixed-rule component/locator mappings present.

Test changes
------------
- tests/test_phase159_pi4_3_repair2g_reference_policy.py
  Replace the brittle exact-count assertion with explicit checks that
  pi_2^1 = 0 and pi_3^3 = Z{iota_3} carry (5.1) provenance while all
  Phase49 premises remain GIVEN.

Not changed
-----------
- EHP exactness remains proof-internal and is not a Reference.
- No pi_4^3 n/k renderer hard-code is added.
- No proof-body prose repair is attempted here.
- No repository-wide pytest is run.
