Phase 159 pi_4^3 repair2g fix5 audit

Purpose
-------
Audit the already-existing Toda (5.1) fixed components instead of adding
the incorrect aggregate component basic_sphere_group_relations.

Known active (5.1) components
-----------------------------
The current local repository reports these six fixed components:

- circle_higher_homotopy_zero
- sphere_connectivity_zero
- stable_negative_zero
- diagonal_identity_group
- stable_zero_stem
- diagonal_suspension_isomorphism

For pi_4^3, the expected relevant components are:

- diagonal_identity_group, for pi_5^5 = Z{iota_5}
- sphere_connectivity_zero, for pi_4^5 = 0

EHP exactness remains proof-internal and must not become a public Reference.

This audit prints, for pi_3^2 and pi_4^3:

- recursive provenance (5.1) steps,
- raw depth-2 (5.1) steps,
- semantic-closure depth-2 (5.1) steps,
- raw Reference entries,
- closure Reference entries,
- final public Narrative.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
