Phase 129-4 minimal implementation bundle

Copy/extract these files into the repository root, preserving the tests/ directory:

- repository_nu_prime_suspension_membership_specialization.py  (new)
- repository_operation_query_facade.py                         (replace)
- repository_operation_query_lookup.py                         (replace)
- tests/test_phase129_nu_prime_operation_query_handoff.py       (new)
- run_phase129_4.ps1                                            (new helper)

Run from the repository root in PowerShell:

  .\run_phase129_4.ps1

Expected user-facing result:

  E\nu' \in \pi_{7}^{4}

The provenance should replay through the existing Toda Proposition 5.6 decomposition

  \pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}.

This phase does NOT add a general E evaluator, a general membership evaluator,
recursive arbitrary containment matching, or parser extensions.
