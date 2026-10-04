Phase157-R20 repair46 runtime audit

Purpose
-------
Inspect the existing semantic/reason structure for:

  ord(eta_3^3) = 2

after repair45.

Known static structure
----------------------
The repository's Phase150 semantic sufficiency audit confirms that the order
step has exactly two direct premises:

1. pi_5^2 = Z/2{eta_2^3}
2. E: pi_5^2 -> pi_6^3 is injective

The missing public explanation is therefore a rendering/reason issue, not a
missing mathematical dependency.

This runtime audit prints:
- the exact order step;
- its direct premises;
- its aggregate semantic kind;
- every reason attached to that conclusion step;
- rendered reason sentence, if any;
- current visible body window around R1, E-injectivity, and ord(eta_3^3)=2.

Production code changes: none.
pytest: not run.
