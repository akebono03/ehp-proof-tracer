Phase 148 RC2-4 Repair R4.2-R2
Web TeX assertion backslash repair

Failure classification
----------------------
The preceding R4.2-R1 run produced:
58 passed, 1 failed.

The only failure was the Flask HTML assertion for the numbered TeX tag.

GitHub develop inspection confirmed that templates/index.html renders
segment.value directly in both data-latex and element text.

A TeX tag in rendered HTML contains one literal backslash:
\tag{1}

In a Python bytes literal, source text b"\\tag{1}" represents that one
literal backslash. The stale test source b"\\\\tag{1}" represents two.

Repair
------
Test-only. The Flask response assertion is changed to the correct
one-backslash runtime value.

Production changes
------------------
None.

R4.2 semantic-closure production code is not modified.

Phase boundary
--------------
No recursive calculation closure.
No exactness-policy change.
No Narrative ordering change.
No repository-wide pytest.
