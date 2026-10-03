Phase156-R5 repair2 duplicate (5.3) diagnostic

Purpose
=======
After Lemma 5.2 specialization attribution was separated correctly,
pi_6^3 still contains two Reference headers with locator "(5.3)".

This diagnostic prints, for both entries:
- Reference number
- label
- locator
- author/title/year
- all proof steps
- inference rule name
- rendered statement
- selected statement status
- extracted LiteratureReference
- premise count

Production changes
==================
None.

Why diagnostic first
====================
Two entries with the same locator may have different provenance.
The repair must preserve the genuine Toda (5.3) source statement and
must not suppress a mathematically distinct source by display-only deduplication.
