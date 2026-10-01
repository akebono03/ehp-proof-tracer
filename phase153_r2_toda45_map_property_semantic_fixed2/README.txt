Phase 153-R2 Fixed2
====================

Reason for Fixed2
-----------------
The first R2 focused run proved that classification succeeded but generic
rendering returned None for the real pi_10^6 Toda45IsomorphismStatement.

Root cause
----------
The real Toda45IsomorphismStatement uses TodaIteratedSuspensionMap with a
symbolic scalar exponent. The existing generic map-name helper accepted only
positive integer exponents.

Existing project behavior
-------------------------
The established Narrative renderer already renders symbolic suspension
exponents with toda_human_readable_renderer._render_scalar_latex.
The existing Phase143-74A regression also requires symbolic iterated-suspension
map rendering.

Minimal correction
------------------
- Keep Toda45IsomorphismStatement classified as MAP_PROPERTY.
- Keep it registered in the generic isomorphism statement types.
- Extend only _generic_group_map_name so TodaIteratedSuspensionMap symbolic
  exponents reuse the existing scalar LaTeX renderer.
- No Toda45-specific renderer is introduced.
- No other Phase152 defect type is addressed.

Focused real case
-----------------
pi_10^6 from the Phase152 inventory.

Whole-suite boundary
--------------------
Only focused and directly related regression tests are run.
The full repository suite remains deferred until the end of Phase153.
