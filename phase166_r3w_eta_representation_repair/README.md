# Phase 166 R3-W — Evidence-bound Eta Representation Repair

This patch does not introduce a new cited mathematical fact. It uses registered earlier group generators, Toda (4.5), and the already proven eta suspension, while allowing only typed `eta_3` / `eta₃` notation variants. No renderer changes or full test suite.

Run `run.ps1` from the extracted folder. The installer keeps backups and supports repeated execution.

## Indentation hotfix
This package corrects the one-character leading indentation in the generated gate function. The earlier run stopped before writing production files. Apply this ZIP over the original folder.
