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

  def __hash__(self):
    return hash((
      tuple(self.group.orders),
      self.coefficients,
    ))

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


@dataclass(frozen=True)
class Subgroup:
  ambient_group: AbelianGroup
  elements: frozenset[GroupElement]
  generators: tuple[GroupElement, ...]

  def __contains__(self, x: GroupElement) -> bool:
    return x in self.elements

  def __len__(self) -> int:
    return len(self.elements)

  @property
  def order(self) -> int:
    return len(self.elements)

  def structure(self) -> tuple[int, ...]:
    return subgroup_structure(self)
  
  def __eq__(self, other) -> bool:
    if not isinstance(other, Subgroup):
      return NotImplemented

    return (
      self.ambient_group == other.ambient_group
      and self.elements == other.elements
    )

@dataclass(frozen=True)
class QuotientGroup:
  ambient_group: AbelianGroup
  subgroup: Subgroup

  def __post_init__(self):
    if self.subgroup.ambient_group != self.ambient_group:
      raise ValueError(
        "部分群の ambient_group が一致しません"
      )

    if any(order == 0 for order in self.ambient_group.orders):
      raise NotImplementedError(
        "自由部分を含む群の商群はまだ実装されていません"
      )

  def coset(
    self,
    element: GroupElement,
  ) -> frozenset[GroupElement]:
    if element.group != self.ambient_group:
      raise ValueError(
        "商群の ambient_group と元の群が一致しません"
      )

    x = element.normalized()

    return frozenset(
      add_elements(x, h).normalized()
      for h in self.subgroup.elements
    )

  @property
  def cosets(
    self,
  ) -> tuple[frozenset[GroupElement], ...]:
    remaining = set(
      group_elements(self.ambient_group)
    )
    result = []

    while remaining:
      representative = min(
        remaining,
        key=lambda x: x.coefficients,
      )

      coset = self.coset(representative)

      result.append(coset)
      remaining -= coset

    return tuple(result)

  @property
  def order(self) -> int:
    return len(self.cosets)

  def add_cosets(
    self,
    left: frozenset[GroupElement],
    right: frozenset[GroupElement],
  ) -> frozenset[GroupElement]:
    if left not in self.cosets:
      raise ValueError(
        "left はこの商群の剰余類ではありません"
      )

    if right not in self.cosets:
      raise ValueError(
        "right はこの商群の剰余類ではありません"
      )

    x = min(
      left,
      key=lambda element: element.coefficients,
    )
    y = min(
      right,
      key=lambda element: element.coefficients,
    )

    return self.coset(
      add_elements(x, y)
    )

def group_elements(
  group: AbelianGroup,
) -> list[GroupElement]:
  if any(order == 0 for order in group.orders):
    raise NotImplementedError(
      "自由部分を含む群の全元列挙はまだ実装されていません"
    )

  ranges = [
    range(order)
    for order in group.orders
  ]

  return [
    GroupElement(group, tuple(x))
    for x in product(*ranges)
  ]

def add_elements(x: GroupElement, y: GroupElement) -> GroupElement:
  if x.group != y.group:
    raise ValueError("異なる群の元は加算できません")

  coefficients = []

  for a, b, order in zip(
    x.coefficients,
    y.coefficients,
    x.group.orders,
  ):
    value = a + b

    if order != 0:
      value %= order

    coefficients.append(value)

  return GroupElement(
    x.group,
    tuple(coefficients),
  )

def multiply_element(
  n: int,
  x: GroupElement,
) -> GroupElement:
  coefficients = []

  for coefficient, order in zip(
    x.coefficients,
    x.group.orders,
  ):
    value = n * coefficient

    if order != 0:
      value %= order

    coefficients.append(value)

  return GroupElement(
    x.group,
    tuple(coefficients),
  )


def prime_factors(n: int) -> list[int]:
  factors = []
  p = 2

  while p * p <= n:
    if n % p == 0:
      factors.append(p)

      while n % p == 0:
        n //= p

    p += 1

  if n > 1:
    factors.append(n)

  return factors


def subgroup_structure(
  subgroup: Subgroup,
) -> tuple[int, ...]:
  if subgroup.order == 1:
    return ()

  prime_parts = []

  for p in prime_factors(subgroup.order):
    powers = []
    pk = p
    previous_rank = 0

    while pk <= subgroup.order:
      killed = sum(
        multiply_element(pk, x).is_zero()
        for x in subgroup.elements
      )

      rank = 0
      value = killed

      while value > 1:
        value //= p
        rank += 1

      count_at_least_k = rank - previous_rank
      powers.append(count_at_least_k)
      previous_rank = rank

      if killed == subgroup.order:
        break

      pk *= p

    elementary = []

    for k in range(len(powers)):
      current = powers[k]
      following = (
        powers[k + 1]
        if k + 1 < len(powers)
        else 0
      )

      count_exact = current - following

      elementary.extend(
        [p ** (k + 1)] * count_exact
      )

    elementary.sort()
    prime_parts.append(elementary)

  rank = max(
    len(part)
    for part in prime_parts
  )

  invariant_factors = [1] * rank

  for part in prime_parts:
    offset = rank - len(part)

    for i, value in enumerate(part):
      invariant_factors[offset + i] *= value

  return tuple(invariant_factors)

def generated_subgroup_elements(
  ambient_group: AbelianGroup,
  generators: tuple[GroupElement, ...],
) -> frozenset[GroupElement]:
  zero = GroupElement(
    ambient_group,
    tuple(0 for _ in ambient_group.orders),
  )

  generated = {zero}
  frontier = [zero]

  while frontier:
    x = frontier.pop()

    for generator in generators:
      y = add_elements(x, generator).normalized()

      if y not in generated:
        generated.add(y)
        frontier.append(y)

  return frozenset(generated)


def find_generators(
  ambient_group: AbelianGroup,
  elements: frozenset[GroupElement],
) -> tuple[GroupElement, ...]:
  generators = ()
  generated = generated_subgroup_elements(
    ambient_group,
    generators,
  )

  for x in sorted(
    elements,
    key=lambda element: element.coefficients,
  ):
    if x in generated:
      continue

    generators += (x,)
    generated = generated_subgroup_elements(
      ambient_group,
      generators,
    )

    if generated == elements:
      break

  return generators


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
    return group_elements(self.source)

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

  def kernel_subgroup(self) -> Subgroup:
    elements = frozenset(self.kernel())

    return Subgroup(
      ambient_group=self.source,
      elements=elements,
      generators=find_generators(
        self.source,
        elements,
      ),
    )

  def image_subgroup(self) -> Subgroup:
    elements = frozenset(self.image())

    return Subgroup(
      ambient_group=self.target,
      elements=elements,
      generators=find_generators(
        self.target,
        elements,
      ),
    )
