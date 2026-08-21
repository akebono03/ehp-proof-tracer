# EHP Proof Tracer

A computational tool for tracing calculations in EHP exact sequences
for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that explains how
homotopy groups of spheres are determined from:

* EHP exact sequences
* composition relations
* Toda brackets
* Steenrod operations
* literature references

The project currently focuses on finite abelian groups and EHP exact
sequences.

## Current features

### Homotopy group data

* Load homotopy groups and generators from `data/sphere.csv`
* Represent finite abelian groups as direct sums of cyclic groups
* Access generators and their orders

### Group calculations

* Represent elements of finite abelian groups
* Apply homomorphisms represented by matrices
* Compute kernels and images
* Represent subgroups as structured objects
* Compute subgroup generators
* Compute subgroup orders
* Determine the abstract structure of finite abelian subgroups

Examples:

```text
()       -> 0
(2,)     -> Z/2
(4,)     -> Z/4
(2, 2)   -> Z/2 ⊕ Z/2
(2, 4)   -> Z/2 ⊕ Z/4
```

### EHP calculations

* Construct E, H, and P homomorphisms
* Compute `Im(E)`, `Ker(H)`, `Im(H)`, and `Ker(P)` as subgroups
* Check exactness using subgroup equality
* Determine the abstract group structure of images and kernels

## Example

For the EHP segment

```text
π_7(S^2) --E--> π_8(S^3) --H--> π_8(S^5) --P--> π_6(S^2)
```

the program verifies

```text
Im(E) = Ker(H)
Im(H) = Ker(P)
```

and can also determine the group structures of these subgroups.

## Development status

* Phase 1: finite abelian group calculations — completed
* Phase 2: structured subgroup calculations — completed
* Phase 3: inference from exact sequences — next

Current test status:

```text
18 passed
```

## Next phase

### Phase 3: infer unknown group structures from exact sequences

The next step is to move from verifying known EHP exact sequences to
using exactness to infer unknown group structures.

The first target is quotient groups.

For an exact sequence

```text
A --f--> B --g--> C
```

exactness gives

```text
B / Im(f) ≅ Im(g)
```

Phase 3 will begin by introducing a quotient-group representation and
computing the structure of `B / Im(f)`.

## Project documentation

More detailed development and design notes are kept separately:

* `docs/development_log.md` — implementation history and Phase progress
* `docs/design.md` — design decisions and mathematical/computational rationale

## Tests

Run the test suite with:

```powershell
python -m pytest -v
```
