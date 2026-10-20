# Phase 166 R3-Q: Missing module repair

This repair installs only `phase166_r3q_hopf_image_relation.py` into the repository root. The previous ZIP contained this module within its installation directory, but did not copy it to the root where Python imports it. The runner refuses to overwrite a differing existing module, checks the import explicitly, and runs 10 focused tests. It does not edit other production files or run the full test suite.
