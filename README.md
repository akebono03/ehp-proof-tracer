# EHP Proof Tracer

A computational tool for tracing calculations in EHP exact sequences
for unstable homotopy groups of spheres.

## Current features

- Load homotopy groups and generators from `sphere.csv`
- Represent finite abelian groups
- Construct E, H, and P homomorphisms
- Compute kernels and images
- Check exactness of EHP sequence segments

## Example

For

π_7(S^2) → π_8(S^3) → π_8(S^5) → π_6(S^2)

the program computes

Im(E) = Ker(H)

and

Im(H) = Ker(P).

## Goal

The long-term goal is to build a proof tracer that explains how
homotopy groups of spheres are determined from EHP exact sequences,
composition relations, Toda brackets, and literature references.