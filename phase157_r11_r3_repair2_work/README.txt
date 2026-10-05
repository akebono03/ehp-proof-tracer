Phase157 R11-R3 repair2

repair1 output was too verbose because full reason objects were printed.
The terminal paste was dominated by huge nested ProofStep repr output.

repair2 prints only:
- target statement presence per stage;
- line numbers;
- compact reason conclusion type;
- owner_argument_index;
- reference_application;
- inference rule name.

Stages:
1. base markdown
2. contributions
3. reason prose
4. final narrative

Targets:
- E: pi_4^2 -> pi_5^3 isomorphism
- pi_6^5 = Z/2{eta_5}

Production code changes: none
Test code changes: none
pytest: not run
