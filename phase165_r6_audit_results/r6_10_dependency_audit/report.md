# Phase 165 R6-10 dependency audit

Read-only. No test or Probe has been retired.

Scanned Python files: 729
Phase 49/56 named test files: 13
Other direct legacy importers: 1
AST parse errors: 0

## Candidate tests
- tests/test_phase49_concrete_pi3_2_compatibility.py
- tests/test_phase49_delta_hopf_surjectivity.py
- tests/test_phase49_hopf_injectivity.py
- tests/test_phase49_hopf_isomorphism.py
- tests/test_phase49_low_dimensional_facts.py
- tests/test_phase49_probe.py
- tests/test_phase55_prop51_phase49_dependency.py
- tests/test_phase56_pi_i_minus_1_1_zero.py
- tests/test_phase56_probe.py
- tests/test_phase56_prop44_composition_compatibility.py
- tests/test_phase56_prop44_eta2_specialization.py
- tests/test_phase56_prop44_second_summand_restriction.py
- tests/test_phase56_toda52_composition_isomorphism.py

## Other direct legacy importers
- probes/probe_phase58_capabilities.py

## Caution
Do not retire a Probe until all active imports and call sites are resolved.
