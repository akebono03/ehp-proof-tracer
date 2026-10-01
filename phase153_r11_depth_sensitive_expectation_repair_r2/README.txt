Phase 153-R11 Depth-sensitive Expectation Repair R2
================================================

Observed failure
----------------
The new R11 test used max_depth=2 but assumed that Proposition 4.4 and
Proposition 5.1 must remain because an older Phase 144 test keeps them at
max_depth=3.

That assumption is too strong.

At depth 2, R11 may correctly remove References whose ProofSteps are outside
the displayed generic argument scope. At depth 3, the older structured
Reference behavior remains valid and its existing test continues to cover it.

Repair
------
Production changes: none.

Changed:
tests/test_phase153_r11_generic_reference_attribution_filtering.py

The R11 test now derives expected depth-2 References from:
- used ProofStep identities;
- current NarrativeArgument scope;
- selected ordered contributions;
- root self-reference exclusion.

Audit
-----
The audit verifies:
- root theorem self-reference is absent;
- Reference numbering is contiguous;
- pi_6^3 keeps core depth-2 external References;
- deeper-scope References are not required at depth 2.

Boundary
--------
Punctuation normalization remains deferred.
The requested final style is "," and "." instead of "、" and "。".

Full pytest remains deferred until the end of Phase 153.

R2 packaging repair
-------------------
R1 incorrectly passed the literal string \\n to pathlib.Path.write_text(newline=...).
R2 uses newline="\n" correctly. Production logic is unchanged.
