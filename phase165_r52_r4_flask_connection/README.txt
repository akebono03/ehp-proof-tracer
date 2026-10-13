R52-R4: Flask group-proof-progress route, generic WebGroupProofView presentation.

Changes: web_app.py:create_app.index, templates/index.html, new phase165_r52_r4_flask_bridge.py, new targeted tests.
Existing standard group proof route and Goal-only fail-closed path unchanged.
No mathematical goal is inferred from n,k. A request without a typed goal is explicitly NOT_SEARCHED. To search, pass verified goal/bridge/provider through the generic bridge from an authorized caller.
The existing complete-proof rendering remains separate and unchanged; full Flask integration for typed goal provisioning is beyond this R4 step.
Full pytest is deliberately not run.
