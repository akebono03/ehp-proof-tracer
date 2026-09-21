# Phase 112-1A nu_prime end-to-end mathematical workflow audit

This report is observational. It does not change repository code.

## Results

| # | Category | Case | Return code | Classification | Command |
|---:|---|---|---:|---|---|
| 1 | baseline | `01_known_group_pi6_3` | 0 | `PASS` | `python main.py 3 3` |
| 2 | baseline | `02_show_proof_nu_prime_depth3` | 0 | `PASS` | `python main.py show-proof nu_prime --depth 3` |
| 3 | baseline | `03_query_H_nu_prime` | 0 | `PASS` | `python main.py query H(nu_prime)` |
| 4 | baseline | `04_query_proof_H_nu_prime_fact1` | 0 | `PASS` | `python main.py query-proof H(nu_prime) --fact 1 --depth 3` |
| 5 | baseline | `05_query_proof_H_nu_prime_fact2` | 0 | `PASS` | `python main.py query-proof H(nu_prime) --fact 2 --depth 3` |
| 6 | baseline | `06_query_E_eta2_nu_prime` | 0 | `PASS` | `python main.py query "E(eta_2 o nu_prime)"` |
| 7 | baseline | `07_query_proof_E_eta2_nu_prime` | 0 | `PASS` | `python main.py query-proof "E(eta_2 o nu_prime)" --depth 3` |
| 8 | baseline | `08_query_eta2_nu_prime` | 0 | `PASS` | `python main.py query "eta_2 o nu_prime"` |
| 9 | baseline | `09_query_eta2_nu_prime_eta6` | 0 | `PASS` | `python main.py query "eta_2 o nu_prime o eta_6"` |
| 10 | baseline | `10_explore_applicable_nu_prime` | 0 | `PASS` | `python main.py explore-applicable nu_prime` |
| 11 | baseline | `11_execute_nu_prime_candidates` | 0 | `PASS` | `python main.py execute nu_prime` |
| 12 | baseline | `12_execute_nu_prime_candidate1` | 0 | `PASS` | `python main.py execute nu_prime --candidate 1` |
| 13 | baseline | `13_execute_nu_prime_candidate2` | 0 | `PASS` | `python main.py execute nu_prime --candidate 2` |
| 14 | pressure | `14_pressure_query_E_nu_prime` | 1 | `LOOKUP_MISS` | `python main.py query E(nu_prime)` |
| 15 | pressure | `15_pressure_query_Delta_nu_prime` | 1 | `LOOKUP_MISS` | `python main.py query Delta(nu_prime)` |
| 16 | pressure | `16_pressure_E_three_term_composition` | 2 | `PARSER_OR_ARGUMENT_BOUNDARY` | `python main.py query "E(eta_2 o nu_prime o eta_6)"` |

## Interpretation guide

- `PASS`: current CLI completed the requested step.
- `LOOKUP_MISS`: syntax was accepted, but no existing repository fact was found.
- `PRESENTATION_GAP`: lookup found something but the user-facing presentation could not render it directly.
- `PARSER_OR_ARGUMENT_BOUNDARY`: the current CLI syntax or argument boundary rejected the request.
- `EXPECTED_NONZERO`: a nonzero result explicitly allowed for a pressure probe.
- `UNEXPECTED_FAILURE`: behavior outside the audit expectation.

## Phase 112-1A boundary

Baseline cases test the already-supported nu_prime workflow.
Pressure cases intentionally ask the next nearby mathematical questions.
Do not implement a fix from this report alone; classify the observed pressure in Phase 112-2 before choosing lookup, orchestration, inference, evaluator, or parser work.
