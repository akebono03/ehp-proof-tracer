Phase157-R20 repair48-r1

Purpose
-------
Repair the NameError introduced by repair48.

Failure
-------
order_toda_group_proof_narrative_injective_image_order_reason()
called:

  _phase157_r11_reference_statement_match_key()

but that helper belongs to the contribution renderer and is not imported into
the reason renderer.

Why no import is added
----------------------
Importing the contribution-renderer helper back into the reason renderer would
create an undesirable circular dependency because the contribution renderer
already imports from the reason renderer.

Minimal repair
--------------
Replace only:
- order_toda_group_proof_narrative_injective_image_order_reason()

The replacement contains a local statement_match_key() with the same minimal
normalization contract needed here:
- strip leading/trailing whitespace;
- strip trailing punctuation;
- ignore numeric \tag{N} equation tags.

No mathematical rule changes.
No pipeline changes.
No import changes.
No new test file is required; the repair48 tests reproduce the failure.

Completion conditions
---------------------
- repair48 focused ordering tests pass;
- repair47 reason tests pass;
- repair42-45 focused tests pass;
- Phase157 Narrative regression passes;
- Phase156 Reference regression passes;
- pi_6^3 renders with:
  [R1] and E-injectivity before the injective-image reason,
  and the reason immediately before ord(eta_3^3)=2.

No repository-wide pytest.
