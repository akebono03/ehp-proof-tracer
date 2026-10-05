Phase157-R20 repair43

Purpose
-------
Remove connector prose that becomes dangling after late Reference-restatement
suppression.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

New function
------------
- suppress_toda_group_proof_narrative_dangling_connectors()

Insertion point
---------------
Immediately after:
- suppress_toda_group_proof_narrative_repeated_reference_restatements()

Import changes
--------------
None.

Generic rules
-------------
At the late public-body stage:
- remove paragraphs consisting only of:
  - 以上より,
  - したがって,
  - これより,
  - これらより,
- remove the same connector when it is the final line of a multiline paragraph;
- remove dangling equation-reference connectors such as `(6) と (7) より,`
  when they are a final line with no conclusion;
- remove a redundant generic connector immediately before a Reference marker,
  e.g. `以上より, [R1]より, ...` -> `[R1]より, ...`.

This repair does not suppress repeated semantic conclusions such as Delta=0.

New test
--------
- tests/test_phase157_r20_repair43_dangling_connector_cleanup.py

No documentation changes.
No repository-wide pytest.
