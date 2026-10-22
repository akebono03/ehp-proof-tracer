# Phase 168 R3-12 test expectation fix

This repair package changes only the R3-12 test expectation, not the production implementation or the public Web route.

The function checks the citation-to-step direction first. A malformed map containing `((2,),)` therefore raises `ValueError("citation and step map disagree")` before the later forward-direction validation. The corrected test checks the actual exception.

Run `run.ps1` from the repository root after extracting the ZIP. This runs four targeted tests and the original four-group probe. It does not run the full suite or modify repository files.
