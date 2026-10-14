# Phase 165 R27-R27

Removes two orphaned legacy Prop. 5.15 bootstrap modules, with an AST import guard limited to root-level production Python modules. The installer preserves backups, writes an audit JSON file, aborts on any active import, and runs six targeted tests only. It does not remove lower Prop. 5.6/5.8/5.11 modules, shared inference rules, or the unified statement registry. Historic tests directly importing removed files are outside the guard and may require migration. No full pytest is run.
