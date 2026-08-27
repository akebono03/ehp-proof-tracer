from dataclasses import dataclass


@dataclass(frozen=True)
class SuspensionMapStatement:
  sphere_dimension: int
  stem: int


def is_freudenthal_stable_range(
  statement,
):
  return (
    statement.stem
    <= statement.sphere_dimension - 2
  )


def is_freudenthal_boundary_range(
  statement,
):
  return (
    statement.stem
    == statement.sphere_dimension - 1
  )







