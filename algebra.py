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
    zero = GroupElement(
      self.ambient_group,
      tuple(
        0
        for _ in self.ambient_group.orders
      ),
    )

    return finite_abelian_structure(
      elements=self.elements,
      zero=zero,
      add=add_elements,
    )
  
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

  def structure(self) -> tuple[int, ...]:
    cosets = self.cosets

    zero = self.coset(
      GroupElement(
        self.ambient_group,
        tuple(
          0
          for _ in self.ambient_group.orders
        ),
      )
    )

    return finite_abelian_structure(
      elements=cosets,
      zero=zero,
      add=self.add_cosets,
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

  def induced_quotient_map(self):
    return InducedMap(self)


@dataclass(frozen=True)
class InducedMap:
  original_map: GroupMap

  @property
  def source(self) -> QuotientGroup:
    return QuotientGroup(
      ambient_group=self.original_map.source,
      subgroup=self.original_map.kernel_subgroup(),
    )

  @property
  def target(self) -> Subgroup:
    return self.original_map.image_subgroup()

  def apply(
    self,
    coset: frozenset[GroupElement],
  ) -> GroupElement:
    if coset not in self.source.cosets:
      raise ValueError(
        "この商群の剰余類ではありません"
      )

    representative = min(
      coset,
      key=lambda x: x.coefficients,
    )

    return self.original_map.apply(
      representative
    ).normalized()

  def is_well_defined(self) -> bool:
    for coset in self.source.cosets:
      images = {
        self.original_map.apply(
          x
        ).normalized()
        for x in coset
      }

      if len(images) != 1:
        return False

    return True

  def is_injective(self) -> bool:
    images = [
      self.apply(coset)
      for coset in self.source.cosets
    ]

    return len(images) == len(set(images))

  def is_surjective(self) -> bool:
    images = {
      self.apply(coset)
      for coset in self.source.cosets
    }

    return images == set(
      self.target.elements
    )

  def is_isomorphism(self) -> bool:
    return (
      self.is_well_defined()
      and self.is_injective()
      and self.is_surjective()
    )

@dataclass(frozen=True)
class ExactSequenceStep:
  first_map: GroupMap
  second_map: GroupMap

  def __post_init__(self):
    if self.first_map.target != self.second_map.source:
      raise ValueError(
        "first_map の target と second_map の source が一致しません"
      )

  @property
  def middle_group(self) -> AbelianGroup:
    return self.first_map.target

  @property
  def image_of_first(self) -> Subgroup:
    return self.first_map.image_subgroup()

  @property
  def kernel_of_second(self) -> Subgroup:
    return self.second_map.kernel_subgroup()

  def is_exact(self) -> bool:
    return (
      self.image_of_first
      == self.kernel_of_second
    )

  @property
  def quotient(self) -> QuotientGroup:
    return QuotientGroup(
      ambient_group=self.middle_group,
      subgroup=self.image_of_first,
    )

  @property
  def image(self) -> Subgroup:
    return self.second_map.image_subgroup()

  @property
  def induced_map(self) -> InducedMap:
    if not self.is_exact():
      raise ValueError(
        "完全でないため B / Im(f) → Im(g) の同型を構成できません"
      )

    return self.second_map.induced_quotient_map()

  def verifies_quotient_image_isomorphism(
    self,
  ) -> bool:
    if not self.is_exact():
      return False

    induced = self.induced_map

    return (
      self.quotient == induced.source
      and self.image == induced.target
      and induced.is_isomorphism()
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


def scalar_multiple(
  x,
  n: int,
  zero,
  add,
):
  result = zero
  current = x

  while n > 0:
    if n % 2 == 1:
      result = add(result, current)

    current = add(current, current)
    n //= 2

  return result

def finite_abelian_structure(
  elements,
  zero,
  add,
) -> tuple[int, ...]:
  elements = tuple(elements)
  order = len(elements)

  if order == 1:
    return ()

  prime_parts = []

  for p in prime_factors(order):
    p_part_order = 1
    temp = order

    while temp % p == 0:
      p_part_order *= p
      temp //= p

    killed_sizes = [1]
    power = p

    while True:
      killed_size = sum(
        scalar_multiple(
          x,
          power,
          zero,
          add,
        ) == zero
        for x in elements
      )

      killed_sizes.append(killed_size)

      if killed_size == p_part_order:
        break

      power *= p

    dimensions = []

    for k in range(
      1,
      len(killed_sizes),
    ):
      ratio = (
        killed_sizes[k]
        // killed_sizes[k - 1]
      )

      dimension = 0

      while ratio > 1:
        ratio //= p
        dimension += 1

      dimensions.append(dimension)

    factors = []

    for k in range(
      len(dimensions),
      0,
      -1,
    ):
      current = dimensions[k - 1]

      if k < len(dimensions):
        next_value = dimensions[k]
      else:
        next_value = 0

      count = current - next_value

      factors.extend(
        [p ** k] * count
      )

    factors.sort()
    prime_parts.append(factors)

  rank = max(
    len(part)
    for part in prime_parts
  )

  result = [1] * rank

  for part in prime_parts:
    padded = (
      [1] * (rank - len(part))
      + part
    )

    for i, value in enumerate(padded):
      result[i] *= value

  return tuple(result)

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

def group_structure(
  group: AbelianGroup,
) -> tuple[int, ...]:
  elements = group_elements(group)

  zero = GroupElement(
    group,
    tuple(
      0
      for _ in group.orders
    ),
  )

  return finite_abelian_structure(
    elements=elements,
    zero=zero,
    add=add_elements,
  )

def all_subgroups(
  group: AbelianGroup,
) -> tuple[Subgroup, ...]:
  elements = group_elements(group)

  zero = GroupElement(
    group,
    tuple(
      0
      for _ in group.orders
    ),
  )

  trivial = frozenset({
    zero,
  })

  seen = {
    trivial,
  }

  frontier = [
    trivial,
  ]

  while frontier:
    subgroup_elements = frontier.pop()

    generators = find_generators(
      group,
      subgroup_elements,
    )

    for x in elements:
      if x in subgroup_elements:
        continue

      new_generators = (
        generators
        + (x,)
      )

      generated = generated_subgroup_elements(
        group,
        new_generators,
      )

      if generated in seen:
        continue

      seen.add(generated)
      frontier.append(generated)

  result = []

  for elements_set in seen:
    result.append(
      Subgroup(
        ambient_group=group,
        elements=elements_set,
        generators=find_generators(
          group,
          elements_set,
        ),
      )
    )

  return tuple(
    sorted(
      result,
      key=lambda subgroup: (
        subgroup.order,
        tuple(
          sorted(
            x.coefficients
            for x in subgroup.elements
          )
        ),
      ),
    )
  )

@dataclass(frozen=True)
class ExtensionCandidate:
  left_group: AbelianGroup
  middle_group: AbelianGroup
  right_group: AbelianGroup

  @property
  def left_structure(self) -> tuple[int, ...]:
    return group_structure(
      self.left_group
    )

  @property
  def middle_structure(self) -> tuple[int, ...]:
    return group_structure(
      self.middle_group
    )

  @property
  def right_structure(self) -> tuple[int, ...]:
    return group_structure(
      self.right_group
    )

  @property
  def matching_subgroups(
    self,
  ) -> tuple[Subgroup, ...]:
    left_order = len(
      group_elements(
        self.left_group
      )
    )

    middle_order = len(
      group_elements(
        self.middle_group
      )
    )

    right_order = len(
      group_elements(
        self.right_group
      )
    )

    if middle_order != (
      left_order * right_order
    ):
      return ()

    result = []

    for subgroup in all_subgroups(
      self.middle_group
    ):
      if (
        subgroup.structure()
        != self.left_structure
      ):
        continue

      quotient = QuotientGroup(
        ambient_group=self.middle_group,
        subgroup=subgroup,
      )

      if (
        quotient.structure()
        != self.right_structure
      ):
        continue

      result.append(subgroup)

    return tuple(result)

  def is_valid(self) -> bool:
    return bool(
      self.matching_subgroups
    )

def valid_extension_candidates(
  left_group: AbelianGroup,
  right_group: AbelianGroup,
  middle_groups,
) -> tuple[ExtensionCandidate, ...]:
  result = []

  for middle_group in middle_groups:
    candidate = ExtensionCandidate(
      left_group=left_group,
      middle_group=middle_group,
      right_group=right_group,
    )

    if candidate.is_valid():
      result.append(candidate)

  return tuple(result)







