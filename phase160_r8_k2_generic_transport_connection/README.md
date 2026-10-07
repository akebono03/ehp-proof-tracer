# Phase 160-R8

Connect the existing two-stem production path to the Phase 160 generic finite-cyclic stable transport.

The canonical stable base is:

`pi_6^4 = Z/2{eta_4 eta_5}`.

The previous production helper `_build_higher_eta_transport()` used the specialized rule `toda_prop53_eta4_squared_stable_transport_inference_rule()`.

Phase 160-R8 changes only that transport step to use `toda_45_generic_finite_cyclic_transport_inference_rule()`.

The existing Proposition 5.3 eta-squared bridge remains responsible for generator normalization:

`E^(n-4)(eta_4 eta_5) = eta_n eta_(n+1)`.

The existing finite-cyclic generator bridge then replaces the transported generator with the normalized eta-squared generator.

No new normalization rule is introduced. The old specialized transport rule remains available for compatibility. Public Narrative is not changed in this substep. No full test suite is run.
