# Phase 166 R3-AI — Zero group Goal discovery

This patch **adds only** `database_zero_group_goal_candidates` to
`phase166_r3af_goal_adapter.py`, and adds the import
`TodaPrimaryGroupZeroStatement` to its existing `homotopy_groups` import.

The function constructs a `TodaPrimaryGroupZeroStatement` for an explicit
single-component CSV zero row (`orders=0`, `generator=0`). It is a Goal,
never a ProofStep or GIVEN evidence. The stable fallback follows the existing
`SphereRepository` behavior.

This step does **not** route zero Goals through the public Web search.
That requires a separate, audited change to the search and rendering boundary;
currently those paths expect `Relation` with cyclic/direct-sum RHS.

## Modified import (complete)

```python
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
```

## Full new function

```python
def database_zero_group_goal_candidates(*, n: int, k: int, csv_path=None):
    """Construct zero-group Goals from explicit DB zero rows; never evidence.

    For an unlisted stable target, reuse its stable-base row, as in
    SphereRepository. A missing or mixed row is not a zero-group assertion.
    """
    if type(n) is not int or type(k) is not int or n < 2 or k < 0:
        return ()
    path = (
        Path(csv_path)
        if csv_path is not None
        else Path(__file__).resolve().parent / "data" / "sphere.csv"
    )
    if not path.is_file():
        return ()
    repo = SphereRepository(path)
    direct = repo.df[(repo.df["n"] == n) & (repo.df["k"] == k)]
    if not direct.empty:
        source_n = n
    elif n >= k + 2:
        source_n = k + 2
    else:
        return ()
    components = repo.get_group(source_n, k).components
    if (
        len(components) != 1
        or components[0].order != 0
        or components[0].generator.strip() != "0"
    ):
        return ()
    return (
        TodaPrimaryGroupZeroStatement(
            TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
        ),
    )
```

The function is inserted at the end of `phase166_r3af_goal_adapter.py`,
after `database_group_goal_candidates`. No existing function is replaced.

## Tests

Run `run.ps1` from the repository root after extracting the ZIP. It runs
five focused zero-goal checks plus the prior R3-AI regression tests; it does
not run the full pytest suite.

## Completion criteria

All 23 explicit zero groups produce typed zero Goals, while mixed and
nonzero source rows do not produce zero Goals. The Web proof route is left
unchanged for a later step.
