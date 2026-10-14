# Phase 165 R57-R5 targeted test runner repair

This package replaces only `phase165_r57_r5_backup_reference_cleanup/run.ps1`.

The previous test runner combined all Phase test files into one pytest process and prepended the R57-R5 directory to `PYTHONPATH`. Tests importing the generic module name `install` therefore resolved the wrong Phase installer.

The repaired runner retains the installation and five required test modules, but executes each module in a separate Python process, setting `PYTHONPATH` to its own test directory followed by the repository root. It restores the original environment afterward and stops on test failure. No production Python source, renderer, or proof logic is modified. Full pytest is not run.
