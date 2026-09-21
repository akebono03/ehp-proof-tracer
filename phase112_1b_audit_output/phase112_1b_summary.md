# Phase 112-1B nu_5 end-to-end mathematical workflow audit

This report is observational. It does not change repository code.

## Results

| # | Category | Case | Return code | Classification | Command |
|---:|---|---|---:|---|---|
| 1 | baseline | `01_known_group_pi8_5` | 0 | `PASS` | `python main.py 5 3` |
| 2 | baseline | `02_show_proof_nu5_depth3` | 0 | `PASS` | `python main.py show-proof nu_5 --depth 3` |
| 3 | baseline | `03_query_Delta_nu5` | 0 | `PASS` | `python main.py query Delta(nu_5)` |
| 4 | baseline | `04_query_proof_Delta_nu5` | 0 | `PASS` | `python main.py query-proof Delta(nu_5) --depth 3` |
| 5 | baseline | `05_query_nu5_eta8` | 0 | `PASS` | `python main.py query "nu_5 o eta_8"` |
| 6 | baseline | `06_query_nu5_eta8_eta9` | 0 | `PASS` | `python main.py query "nu_5 o eta_8 o eta_9"` |
| 7 | baseline | `07_query_nu5_nu8` | 0 | `PASS` | `python main.py query "nu_5 o nu_8"` |
| 8 | baseline | `08_explore_applicable_nu5` | 0 | `PASS` | `python main.py explore-applicable nu_5` |
| 9 | observation | `09_execute_nu5` | 0 | `PASS` | `python main.py execute nu_5` |
| 10 | pressure | `10_pressure_query_E_nu5` | 1 | `LOOKUP_MISS` | `python main.py query E(nu_5)` |
| 11 | pressure | `11_pressure_query_H_nu5` | 1 | `LOOKUP_MISS` | `python main.py query H(nu_5)` |
| 12 | pressure | `12_pressure_E_nu5_eta8` | 1 | `LOOKUP_MISS` | `python main.py query "E(nu_5 o eta_8)"` |
| 13 | pressure | `13_pressure_E_three_term_nu5_eta8_eta9` | 2 | `PARSER_OR_ARGUMENT_BOUNDARY` | `python main.py query "E(nu_5 o eta_8 o eta_9)"` |
| 14 | pressure | `14_pressure_four_term_continuation` | 2 | `PARSER_OR_ARGUMENT_BOUNDARY` | `python main.py query "nu_5 o eta_8 o eta_9 o eta_10"` |

## Interpretation guide

- `PASS`: current CLI completed the requested step.
- `LOOKUP_MISS`: syntax was accepted, but no existing repository fact was found.
- `PRESENTATION_GAP`: lookup found something but the user-facing presentation could not render it directly.
- `NO_EXECUTABLE_TARGET`: generator workflow found no currently executable qualified target.
- `PARSER_OR_ARGUMENT_BOUNDARY`: current CLI syntax or argument boundary rejected the request.
- `EXPECTED_NONZERO`: a nonzero result explicitly allowed for an observational/pressure probe.
- `UNEXPECTED_FAILURE`: behavior outside the audit expectation.

## Mathematical path under audit

The intended path is:

pi_8^5 = Z/8{nu_5}
-> proof replay
-> Delta(nu_5)
-> nu_5 eta_8
-> nu_5 eta_8^2
-> nu_5^2
-> applicable theorem discovery
-> execution availability
-> nearby operation pressure probes.

## Phase 112-1B boundary

Do not implement parser, evaluator, lookup, or inference changes from a single miss.
Use this report together with Phase 112-1A and the later sigma_11 audit to identify repeated pressure.
