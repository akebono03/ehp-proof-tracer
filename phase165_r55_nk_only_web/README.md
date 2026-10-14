# Phase 165 R55 — n,k-only Web proof selection

Removes the visible R54 generator-entry form. Group query and Group proof now
select a unique typed goal from the shared Unified Statement Registry, including
nested components of fixed literature propositions, and submit the proposed goal
to the same screened shared backward search used by R53. A proposed goal is never
promoted to a proof premise. If none or multiple goals are registered, the page
reports that it cannot select a goal rather than guessing a group structure.

## Installation

Unzip this package in the project root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r55_nk_only_web\run.ps1"
```

Restart Flask and enter only n=2, k=1 in Group query. Existing R54 explicit POST
API remains temporarily available for compatibility but is not shown in the UI.
No complete proof trees or legacy group results are used as premises. Targeted
pytest only; full pytest is reserved for phase closure.

`CHANGED_CODE.md` is written after installation and includes complete modified
Python imports and function body. Source files and tests are included unabridged.
