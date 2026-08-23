from dataclasses import dataclass
from algebra import ExactSequenceStep

@dataclass
class ExactnessResult:
  left_map: object
  right_map: object

  @property
  def middle_group(self):
    return self.left_map.target

  @property
  def exact_step(self):
    return ExactSequenceStep(
      first_map=self.left_map,
      second_map=self.right_map,
    )

  def image(self):
    return self.left_map.image_subgroup()

  def kernel(self):
    return self.right_map.kernel_subgroup()

  @property
  def image_structure(self):
    return self.image().structure()

  @property
  def kernel_structure(self):
    return self.kernel().structure()

  @property
  def image_abelian_structure(self):
    return (
      self.exact_step
      .image_of_first_structure
    )

  @property
  def kernel_abelian_structure(self):
    return (
      self.exact_step
      .kernel_of_second_structure
    )

  @property
  def quotient_abelian_structure(self):
    return (
      self.exact_step
      .quotient_structure
    )

  @property
  def right_image_abelian_structure(self):
    return (
      self.exact_step
      .image_structure
    )

  def is_exact(self):
    return (
      self.exact_step
      .is_exact()
    )

  def verifies_quotient_image_structure_isomorphism(
    self,
  ):
    return (
      self.exact_step
      .verifies_quotient_image_structure_isomorphism()
    )

class EHPSegment:
  def __init__(self, repository, n, k):
    self.repository = repository
    self.n = n
    self.k = k

    # π_{n+k-1}(S^{n-1}) --E-->
    # π_{n+k}(S^n) --H-->
    # π_{n+k}(S^{2n-1}) --P-->
    # π_{n+k-2}(S^{n-1})

    self.E = repository.get_group_map(
      "E",
      source_n=n - 1,
      source_k=k,
    )

    self.H = repository.get_group_map(
      "H",
      source_n=n,
      source_k=k,
    )

    self.P = repository.get_group_map(
      "P",
      source_n=2 * n - 1,
      source_k=k - n + 1,
    )

  def exactness_at_sphere(self):
    return ExactnessResult(
      self.E,
      self.H,
    )

  def exactness_at_hopf_target(self):
    return ExactnessResult(
      self.H,
      self.P,
    )

  def exact_step_at_sphere(self):
    return ExactSequenceStep(
      first_map=self.E,
      second_map=self.H,
    )

  def exact_step_at_hopf_target(self):
    return ExactSequenceStep(
      first_map=self.H,
      second_map=self.P,
    )

  def check(self):
    return [
      self.exactness_at_sphere(),
      self.exactness_at_hopf_target(),
    ]

  def sphere_group_candidates(self):
    return (
      self.exact_step_at_sphere()
      .middle_group_candidates()
    )

  def sphere_group_candidate_structures(self):
    return (
      self.exact_step_at_sphere()
      .middle_group_candidate_structures()
    )

  def hopf_target_group_candidates(self):
    return (
      self.exact_step_at_hopf_target()
      .middle_group_candidates()
    )

  def hopf_target_group_candidate_structures(self):
    return (
      self.exact_step_at_hopf_target()
      .middle_group_candidate_structures()
    )




