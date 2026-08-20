from dataclasses import dataclass
from itertools import product

from models import AbelianGroup


@dataclass(frozen=True)
class GroupElement:
  group: AbelianGroup
  coefficients: tuple[int, ...]

  def __post_init__(self):
    if len(self.coefficients) != self.group.direct_sum:
      raise ValueError("係数の数と群の直和成分数が一致しません")

  def normalized(self):
    coefficients = []

    for coefficient, order in zip(
      self.coefficients,
      self.group.orders
    ):
      if order == 0:
        coefficients.append(0)
      else:
        coefficients.append(coefficient % order)

    return GroupElement(
      self.group,
      tuple(coefficients),
    )

  def is_zero(self):
    return all(
      coefficient == 0
      for coefficient in self.normalized().coefficients
    )


@dataclass
class GroupMap:
  name: str
  source: AbelianGroup
  target: AbelianGroup
  matrix: list[list[int]]

  def apply(self, element):
    x = element.normalized().coefficients

    result = []

    for i, order in enumerate(self.target.orders):
      value = 0

      for j in range(self.source.direct_sum):
        value += self.matrix[i][j] * x[j]

      if order != 0:
        value %= order

      result.append(value)

    return GroupElement(
      self.target,
      tuple(result),
    )

  def source_elements(self):
    ranges = [
      range(order)
      for order in self.source.orders
    ]

    return [
      GroupElement(self.source, tuple(x))
      for x in product(*ranges)
    ]

  def kernel(self):
    return [
      x
      for x in self.source_elements()
      if self.apply(x).is_zero()
    ]

  def image(self):
    result = {}

    for x in self.source_elements():
      y = self.apply(x).normalized()
      result[y.coefficients] = y

    return list(result.values())
  