from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup


@dataclass(frozen=True)
class TodaGroupQuery:
  n: int
  k: int

  def __post_init__(
    self,
  ) -> None:
    if (
      isinstance(
        self.n,
        bool,
      )
      or not isinstance(
        self.n,
        int,
      )
    ):
      raise TypeError(
        "n must be an int"
      )

    if (
      isinstance(
        self.k,
        bool,
      )
      or not isinstance(
        self.k,
        int,
      )
    ):
      raise TypeError(
        "k must be an int"
      )

    if self.n <= 0:
      raise ValueError(
        "n must be positive"
      )

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return TodaPrimaryGroup(
      group_dimension=(
        self.n
        + self.k
      ),
      sphere_dimension=self.n,
    )
