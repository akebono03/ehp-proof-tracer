# EHP Proof Tracer

A computational tool for tracing calculations in EHP exact sequences
for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that explains how
homotopy groups of spheres are determined from:

- EHP exact sequences
- composition relations
- Toda brackets
- Steenrod operations
- literature references

The project currently focuses on finite abelian groups and EHP exact
sequences.

## Current status

Phase 3 completed.

The program can now derive possible group structures from exactness
and extension data in EHP exact sequences.

Example:

```text
0 → Z/2 → π_8(S^5) → Z/4 → 0
```

gives the candidates

```text
Z/8
Z/2 ⊕ Z/4
```

The known value

```text
π_8(S^5) = Z/8
```

is one of these candidates.

Current test status:

```text
62 passed
```

## Current features

### Homotopy group data

- Load homotopy groups and generators from `data/sphere.csv`
- Represent finite abelian groups as direct sums of cyclic groups
- Access generators and their orders

### Group calculations

- Represent elements of finite abelian groups
- Apply homomorphisms represented by matrices
- Compute kernels and images
- Represent subgroups as structured objects
- Compute subgroup generators
- Compute subgroup orders
- Determine abstract structures of finite abelian subgroups

Examples:

```text
()       -> 0
(2,)     -> Z/2
(4,)     -> Z/4
(2, 2)   -> Z/2 ⊕ Z/2
(2, 4)   -> Z/2 ⊕ Z/4
```

### Quotient groups

- Construct quotient groups
- Enumerate cosets
- Compute quotient-group order
- Compute quotient-group structure
- Verify induced quotient maps

### Exact sequences

For

```text
A --f--> B --g--> C
```

the program can:

- compute `Im(f)`
- compute `Ker(g)`
- verify `Im(f) = Ker(g)`
- construct `B / Im(f)`
- compute `Im(g)`
- verify

```text
B / Im(f) ≅ Im(g)
```

### First isomorphism theorem

For a homomorphism

```text
f : G → H
```

the program can construct and verify the induced isomorphism

```text
G / Ker(f) ≅ Im(f)
```

### Extension candidates

For a short exact sequence

```text
0 → A → B → C → 0
```

the middle group `B` is not necessarily uniquely determined.

For example,

```text
0 → Z/2 → B → Z/2 → 0
```

allows both

```text
Z/4
Z/2 ⊕ Z/2
```

as possible middle groups.

The program can:

- enumerate finite abelian group structures of the required order
- construct abstract candidate groups
- test whether a candidate contains a subgroup isomorphic to `A`
- test whether the corresponding quotient is isomorphic to `C`
- return the valid middle-group candidates

### EHP calculations

For an EHP segment

```text
π_{n+k-1}(S^{n-1})
        --E-->
π_{n+k}(S^n)
        --H-->
π_{n+k}(S^{2n-1})
        --P-->
π_{n+k-2}(S^{n-1})
```

the program can:

- construct the E, H, and P homomorphisms
- compute `Im(E)`, `Ker(H)`, `Im(H)`, and `Ker(P)`
- check exactness
- determine subgroup structures
- construct exact-sequence steps
- derive quotient/image isomorphisms
- infer possible structures of middle groups

## Verified examples

### n = 3, k = 5

For

```text
π_7(S^2)
  --E-->
π_8(S^3)
  --H-->
π_8(S^5)
  --P-->
π_6(S^2)
```

the program verifies

```text
Im(E) = Ker(H)
Im(H) = Ker(P)
```

and derives:

```text
π_8(S^3):
  candidate = Z/2
```

For the Hopf target it derives:

```text
π_8(S^5):
  candidates =
    Z/8
    Z/2 ⊕ Z/4
```

The known value is:

```text
π_8(S^5) = Z/8
```

### n = 11, k = 18

The program also verifies exactness and quotient/image structure for
larger noncyclic finite abelian groups.

For example,

```text
π_29(S^11)
≅ Z/8 ⊕ Z/4 ⊕ Z/2
```

and the relevant quotient has structure

```text
Z/2 ⊕ Z/2
```

## Development status

- Phase 1: finite abelian group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: free parts such as `Z` — next

## Current limitations

The inference layer currently focuses on finite abelian groups.

Some algorithms enumerate all elements or all subgroups, so they are
intended for relatively small finite groups at this stage.

Free abelian components such as

```text
Z
```

are not yet fully supported by the quotient and extension machinery.

## Project documentation

More detailed development and design notes are kept separately:

- `docs/development_log.md` — implementation history and Phase progress
- `docs/design.md` — design decisions and mathematical/computational rationale

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

Current result:

```text
62 passed
```

## Next step

Phase 4:

Extend the algebra layer to groups containing free parts such as `Z`.

