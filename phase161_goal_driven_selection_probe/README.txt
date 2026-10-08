Phase 161 Goal-Driven Selection Probe (read only)

Production Repository and Rule Catalog are built unmodified.
The goal (pi_4^2 -> pi_5^3 isomorphism) determines an n=3 rule family
and four exactness windows. Candidate Proposition 5.1 and Hopf relation
premises are looked up across the Production scope, not extracted from
the completed target proof's ancestry. A bounded temporary Catalog is
used for the experiment and no permanent safety flag is changed.

Limits: this is a target-dimension-specific profile; not general-purpose
goal-only inference, and a match failure should be recorded rather than
silently importing premises from the known proof.

Run from repo root via run_phase161_goal_driven.ps1.
Output: phase161_goal_driven_selection_probe.json.
