Phase 159 repair2g fix10g audit

Purpose
-------
Determine why the fix10f replacement of
_phase158_normalize_public_equation_numbers()
does not change the final numbered map-property display.

The final public Narrative still contains:
  $H: ...\tag{1}$ は単射.
  $H: ...\tag{2}$ は全射.

If the modified fix10f function were actually executed on those lines,
the tag marker would be removed or converted.

This audit therefore checks:
1. how many definitions of
   _phase158_normalize_public_equation_numbers()
   exist in the local renderer file,
2. the exact source of the function object imported at runtime,
3. the actual proof_body lines entering that function,
4. the actual lines returned from that function,
5. the final public Narrative.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
