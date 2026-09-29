Phase 148 RC2-5 Repair R4.3

Test-only repair. Production code is unchanged.

RC2 E4 states that UNOWNED_RECURSIVE exactness evidence is not automatically
expanded into Narrative body contributions. The contribution filter returns
an empty tuple for this exposure class, covering both EXACTNESS_WINDOW and
DERIVED_SHORT_EXACT_SEQUENCE contributions.

Therefore the remaining pi8_5 Phase143_47 expectation for the recursive
short exact sequence is updated from one occurrence to zero.

Focused regression only. Repository-wide pytest is NOT run.
