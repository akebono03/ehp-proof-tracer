<!-- PHASE150_CLOSURE -->
## Phase 150 closure — generic provenance / reason prose

Phase 150 completed RC4, generic provenance / reason prose, without adding new
Toda theorem facts or changing the stored proof graph.

The phase introduced typed Narrative reason information derived from existing proof
provenance and connected that information to generic Narrative prose. The work also
confirmed an architectural limitation in the current transition strategy: multiple
renderer routes still coexist, and route-by-route migration itself can create
group-dependent presentation differences.

Phase 150 therefore closes without continuing group-by-group renderer migration.
The next phase starts from a whole-population generic baseline instead.

The six representative groups used throughout the RC4 audit were

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

The final visible-reason contract is instance-based. If several typed reasons render
to the same generic sentence, the Narrative may contain that sentence several times;
the number of occurrences must match the number of typed reason instances producing
that sentence.

Phase 150 final repository-wide regression:

```text
10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

This run is the Phase 150 closure baseline. Future development does not treat the
complete historical suite as a mandatory end-of-every-phase operation. Focused tests
and a maintained canonical regression set are the normal development checks; the
complete historical suite is reserved for major integration or release milestones.

Phase 151 begins with an all-group generic baseline. It will force the audited group
population through the same generic Narrative route for observation and
classification while leaving the public renderer selection unchanged.
