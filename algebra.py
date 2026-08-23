from dataclasses import dataclass
from itertools import product
from math import inf

from sympy import Matrix
from sympy.matrices.normalforms import (
  hermite_normal_form,
  smith_normal_form,
)
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import (
  smith_normal_decomp,
)

from models import (
  AbelianGroup,
  AbelianGroupStructure,
  GroupComponent,
)

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
      if order == inf:
        coefficients.append(coefficient)
      elif order == 0:
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

    if any(
      order == inf
      for order in self.ambient_group.orders
    ):
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

      if order == inf:
        pass
      elif order == 0:
        value = 0
      else:
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

  def integer_matrix(self) -> Matrix:
    if not (
      is_free_abelian_group(self.source)
      and is_free_abelian_group(self.target)
    ):
      raise NotImplementedError(
        "現在は自由アーベル群間の写像のみ対応しています"
      )

    return Matrix(
      self.matrix
    )

  def smith_normal_form(self) -> Matrix:
    return smith_normal_form(
      self.integer_matrix(),
      domain=ZZ,
    )

  def free_map_rank(self) -> int:
    return self.integer_matrix().rank()

  def kernel_structure(
    self,
  ) -> AbelianGroupStructure:
    return (
      self.presentation_kernel_structure()
    )

  def image_structure(
    self,
  ) -> AbelianGroupStructure:
    return (
      self.presentation_image_structure()
    )

  def cokernel_structure(
    self,
  ) -> AbelianGroupStructure:
    if not (
      self.is_well_defined_homomorphism()
    ):
      raise ValueError(
        "well-defined な群準同型ではありません"
      )

    target_relations = (
      relation_matrix(
        self.target
      )
    )

    map_matrix = Matrix(
      self.matrix
    )

    relations = (
      target_relations.row_join(
        map_matrix
      )
    )

    return structure_from_presentation(
      relations
    )

  def induced_quotient_map(self):
    return InducedMap(self)

  def is_well_defined_homomorphism(
    self,
  ) -> bool:
    if len(
      self.matrix
    ) != self.target.direct_sum:
      return False

    if any(
      len(row)
      != self.source.direct_sum
      for row in self.matrix
    ):
      return False

    for j, source_order in enumerate(
      self.source.orders
    ):
      if source_order == inf:
        continue

      if source_order == 0:
        relation_order = 1
      else:
        relation_order = int(
          source_order
        )

      for i, target_order in enumerate(
        self.target.orders
      ):
        value = (
          relation_order
          * self.matrix[i][j]
        )

        if target_order == inf:
          if value != 0:
            return False

        elif target_order == 0:
          continue

        elif value % int(
          target_order
        ) != 0:
          return False

    return True

  def kernel_lattice_basis(
    self,
  ) -> Matrix:
    if not (
      self.is_well_defined_homomorphism()
    ):
      raise ValueError(
        "well-defined な群準同型ではありません"
      )

    return preimage_lattice_basis(
      Matrix(self.matrix),
      relation_matrix(
        self.target
      ),
    )

  def presentation_kernel_structure(
    self,
  ) -> AbelianGroupStructure:
    kernel_basis = (
      self.kernel_lattice_basis()
    )

    source_relations = (
      relation_matrix(
        self.source
      )
    )

    kernel_relations = (
      lattice_coordinates(
        kernel_basis,
        source_relations,
      )
    )

    return structure_from_presentation(
      kernel_relations
    )

  def presentation_image_structure(
    self,
  ) -> AbelianGroupStructure:
    kernel_basis = (
      self.kernel_lattice_basis()
    )

    return structure_from_presentation(
      kernel_basis
    )

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
    left_order = finite_group_order(
      self.left_group
    )

    middle_order = finite_group_order(
      self.middle_group
    )

    right_order = finite_group_order(
      self.right_group
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

  @property
  def extension_left_group(self) -> AbelianGroup:
    if not self.is_exact():
      raise ValueError(
        "完全でないため extension を構成できません"
      )

    return abstract_abelian_group(
      self.image_of_first.structure(),
      generator_prefix="a",
    )

  @property
  def extension_right_group(self) -> AbelianGroup:
    if not self.is_exact():
      raise ValueError(
        "完全でないため extension を構成できません"
      )

    return abstract_abelian_group(
      self.image.structure(),
      generator_prefix="c",
    )

  def middle_group_candidates(
    self,
  ) -> tuple[ExtensionCandidate, ...]:
    if not self.is_exact():
      raise ValueError(
        "完全でないため中間群候補を推論できません"
      )

    return extension_candidates(
      self.extension_left_group,
      self.extension_right_group,
    )

  def middle_group_candidate_structures(
    self,
  ) -> tuple[tuple[int, ...], ...]:
    return tuple(
      candidate.middle_structure
      for candidate in self.middle_group_candidates()
    )

def group_elements(
  group: AbelianGroup,
) -> list[GroupElement]:
  if group.is_zero():
    return [
      GroupElement(
        group,
        (0,),
      )
    ]

  if any(
    order == inf
    for order in group.orders
  ):
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

    if order == inf:
      pass
    elif order == 0:
      value = 0
    else:
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

def finite_group_order(
  group: AbelianGroup,
) -> int:
  if group.is_zero():
    return 1

  if any(
    order == inf
    for order in group.orders
  ):
    raise NotImplementedError(
      "自由部分を含む群の位数は有限ではありません"
    )

  result = 1

  for order in group.orders:
    result *= order

  return result

def finite_abelian_structures(
  order: int,
) -> tuple[tuple[int, ...], ...]:
  if order < 1:
    raise ValueError(
      "群の位数は1以上である必要があります"
    )

  if order == 1:
    return ((),)

  result = set()

  def search(
    remaining: int,
    prefix: tuple[int, ...],
  ):
    if remaining == 1:
      result.add(prefix)
      return

    previous = (
      prefix[-1]
      if prefix
      else 1
    )

    for divisor in range(
      2,
      remaining + 1,
    ):
      if remaining % divisor != 0:
        continue

      if divisor % previous != 0:
        continue

      search(
        remaining // divisor,
        prefix + (divisor,),
      )

  search(
    order,
    (),
  )

  return tuple(
    sorted(
      result,
      key=lambda structure: (
        len(structure),
        structure,
      ),
    )
  )

def abstract_abelian_group(
  structure: tuple[int, ...],
  generator_prefix: str = "x",
) -> AbelianGroup:
  if not structure:
    return AbelianGroup(
      n=0,
      k=0,
      components=[
        GroupComponent(
          id=0,
          order=0,
          generator="",
          element=[],
          gen_coe=[],
        )
      ],
    )

  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=i,
        order=order,
        generator=f"{generator_prefix}{i + 1}",
        element=[],
        gen_coe=[],
      )
      for i, order in enumerate(
        structure
      )
    ],
  )

def extension_candidates(
  left_group: AbelianGroup,
  right_group: AbelianGroup,
) -> tuple[ExtensionCandidate, ...]:
  left_order = finite_group_order(
    left_group
  )

  right_order = finite_group_order(
    right_group
  )

  middle_order = (
    left_order
    * right_order
  )

  structures = finite_abelian_structures(
    middle_order
  )

  middle_groups = [
    abstract_abelian_group(
      structure,
      generator_prefix=f"b{i + 1}_",
    )
    for i, structure in enumerate(
      structures
    )
  ]

  return valid_extension_candidates(
    left_group,
    right_group,
    middle_groups,
  )

def abelian_group_structure(
  group: AbelianGroup,
) -> AbelianGroupStructure:
  if group.is_zero():
    return AbelianGroupStructure(
      free_rank=0,
      torsion_orders=(),
    )

  free_rank = sum(
    order == inf
    for order in group.orders
  )

  torsion_orders = tuple(
    int(order)
    for order in group.orders
    if (
      order != inf
      and order != 0
    )
  )

  return AbelianGroupStructure(
    free_rank=free_rank,
    torsion_orders=torsion_orders,
  )

def relation_matrix(
  group: AbelianGroup,
) -> Matrix:
  if group.is_zero():
    return Matrix([
      [1],
    ])

  columns = []

  for i, order in enumerate(
    group.orders
  ):
    if order == inf:
      continue

    if order == 0:
      continue

    column = [
      0
      for _ in range(
        group.direct_sum
      )
    ]

    column[i] = int(order)

    columns.append(column)

  if not columns:
    return Matrix.zeros(
      group.direct_sum,
      0,
    )

  return Matrix(
    group.direct_sum,
    len(columns),
    lambda i, j: columns[j][i],
  )

def integer_kernel_basis(
  matrix: Matrix,
) -> Matrix:
  if matrix.cols == 0:
    return Matrix.zeros(
      0,
      0,
    )

  domain_matrix = (
    DomainMatrix
    .from_Matrix(matrix)
    .convert_to(ZZ)
  )

  smith, _, right = (
    smith_normal_decomp(
      domain_matrix
    )
  )

  rank = matrix.rank()

  right_matrix = (
    right.to_Matrix()
  )

  return right_matrix[
    :,
    rank:
  ]

def preimage_lattice_basis(
  map_matrix: Matrix,
  target_relations: Matrix,
) -> Matrix:
  equation_matrix = (
    map_matrix.row_join(
      -target_relations
    )
  )

  solution_basis = (
    integer_kernel_basis(
      equation_matrix
    )
  )

  source_rank = (
    map_matrix.cols
  )

  projected = solution_basis[
    :source_rank,
    :
  ]

  return hermite_normal_form(
    projected
  )

def lattice_coordinates(
  basis: Matrix,
  vectors: Matrix,
) -> Matrix:
  if vectors.cols == 0:
    return Matrix.zeros(
      basis.cols,
      0,
    )

  if basis.cols == 0:
    if vectors == Matrix.zeros(
      vectors.rows,
      vectors.cols,
    ):
      return Matrix.zeros(
        0,
        vectors.cols,
      )

    raise ValueError(
      "格子基底に含まれないベクトルです"
    )

  columns = []

  for j in range(
    vectors.cols
  ):
    vector = vectors[:,j]

    solution, parameters = (
      basis.gauss_jordan_solve(
        vector
      )
    )

    if parameters.rows != 0:
      raise ValueError(
        "格子座標が一意ではありません"
      )

    for value in solution:
      if not value.is_Integer:
        raise ValueError(
          "整数格子座標になっていません"
        )

    columns.append(
      solution
    )

  return Matrix.hstack(
    *columns
  )

def structure_from_presentation(
  relations: Matrix,
) -> AbelianGroupStructure:
  smith = smith_normal_form(
    relations,
    domain=ZZ,
  )

  rank = smith.rank()

  torsion_orders = []

  diagonal_size = min(
    smith.rows,
    smith.cols,
  )

  for i in range(
    diagonal_size
  ):
    value = abs(
      int(smith[i,i])
    )

    if value > 1:
      torsion_orders.append(
        value
      )

  free_rank = (
    relations.rows
    - rank
  )

  return AbelianGroupStructure(
    free_rank=free_rank,
    torsion_orders=tuple(
      torsion_orders
    ),
  )

def is_free_abelian_group(
  group: AbelianGroup,
) -> bool:
  if group.is_zero():
    return True

  return all(
    order == inf
    for order in group.orders
  )












