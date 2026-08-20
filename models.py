from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class GroupComponent:
  id: int
  order: int | float
  generator: str
  element: list[int]
  gen_coe: list[int]

  def is_infinite(self):
    return self.order == inf


@dataclass(frozen=True)
class AbelianGroup:
  n: int
  k: int
  components: list[GroupComponent]

  @property
  def degree(self):
    return self.n + self.k

  @property
  def direct_sum(self):
    return len(self.components)

  @property
  def orders(self):
    return [component.order for component in self.components]

  @property
  def generators(self):
    return [component.generator for component in self.components]

  def is_zero(self):
    return (
      len(self.components) == 1
      and self.components[0].order == 0
    )

  def __str__(self):
    if self.is_zero():
      return f"π_{self.degree}(S^{self.n}) = 0"

    parts = []

    for component in self.components:
      if component.order == inf:
        group = "Z"
      else:
        group = f"Z/{component.order}"

      if component.generator:
        group += f"<{component.generator}>"

      parts.append(group)

    return (
      f"π_{self.degree}(S^{self.n}) = "
      + " ⊕ ".join(parts)
    )


@dataclass(frozen=True)
class MapImage:
  map_name: str
  source_id: int
  coefficients: list[int]
  reference: str | None
  