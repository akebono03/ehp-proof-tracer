Phase157-R20 repair20 runtime audit

Purpose
-------
Locate the first current generic Narrative pipeline stage where

  eta_3^3 = eta_3^3

appears.

Background
----------
repair19 fixed1 proved that eta_5 = eta_5 is a rendered-reflexive Relation:
the source statement is E^2 eta_3 = eta_5, but generic side normalization
renders both sides as eta_5.

The remaining eta_3^3 = eta_3^3 paragraph was not represented by any
rendered-reflexive Relation among the 32 semantic-closure nodes. Therefore it
must be introduced or retained through another Narrative assembly stage.

Method
------
Monkey-patch current production transforms at runtime only and print target
presence before/after each stage that sees the paragraph.

Production code changes: none.
Tests: none.
pytest: not run.
