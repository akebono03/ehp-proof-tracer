Phase157-R20 repair48

Purpose
-------
Repair the final placement of INJECTIVE_IMAGE_ORDER reason prose.

repair47 result
---------------
The generic reason was generated correctly, but late body reordering moved its
visible premises after the reason paragraph. Final output therefore showed the
reason before:
- the finite-cyclic group premise;
- the injective suspension-map premise.

Changed production files
------------------------
1. toda_group_proof_narrative_reason_renderer.py
   - new order_toda_group_proof_narrative_injective_image_order_reason()

2. toda_group_proof_narrative_contribution_renderer.py
   - import the new ordering helper
   - call it after repair45 unique-step deduplication

Import change
-------------
See full_import_change.txt.

Generic ordering contract
-------------------------
For INJECTIVE_IMAGE_ORDER only:
- identify its visible reason paragraph;
- identify every visible direct premise by normalized public statement key;
- require all premises to occur before the conclusion;
- relocate the reason paragraph to immediately before the conclusion;
- do not change other reason kinds.

Expected pi_6^3 window
----------------------
[R1] pi_5^2 = Z/2{eta_2^3}
...
E: pi_5^2 -> pi_6^3 is injective
reason: E(eta_2^3)=eta_3^3 != 0 and injectivity preserves exact order
ord(eta_3^3)=2

New focused test
----------------
- tests/test_phase157_r20_repair48_injective_image_reason_ordering.py

No documentation changes.
No repository-wide pytest.
