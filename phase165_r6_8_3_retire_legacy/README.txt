Phase 165 R6-8(3) cautious retirement.
This script will DELETE only the enumerated legacy files if and only if no imports from outside this set remain in active root/probes/tests Python files.
It writes phase165_r6_8_3_retirement_report.json. A blocked run deletes nothing.
Before any deletion, a ZIP backup named phase165_r6_8_3_retired_<UTC>.zip is created in the repository root.
No changes to the current backward search, statement registry, mathematical rules or renderer.
Only limited guard tests are run. Full pytest is NOT run.
