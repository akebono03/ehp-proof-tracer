Phase 161-R4-R5 repair9a
Final public Reference-body relink

Repair9 package failure
=======================
Repair9 failed before any production file was written.

The package generator embedded TEST_SOURCE using a repr-form string inside a
raw string. As a result, literal "\n" sequences were passed to ast.parse()
instead of real line breaks, causing SyntaxError.

Repair9a package fix
====================
Do not embed the test source in the apply script.

The test is bundled as a separate template file and copied to tests/ by the
apply script. Both the package test template and changed production code are
AST-validated before and after application.

Production design
=================
The intended repair9 production design is unchanged:

After final:
- body-usage filtering
- fixed-reference restoration
- reference renumbering
- final reference pruning
- final ordering

apply the existing graph-backed:

  link_toda_group_proof_narrative_reference_body_consumers()

one last time to the final public reference entries and final public body.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

New:
- tests/test_phase161_r4_r5_repair9a_final_public_reference_relink.py

Imports
=======
No production import changes.

Full pytest is not run.
