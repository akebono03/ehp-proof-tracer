from dataclasses import dataclass


@dataclass
class ExactnessResult:
  left_map: object
  right_map: object

  @property
  def middle_group(self):
    return self.left_map.target

  def image(self):
    return {
      x.coefficients
      for x in self.left_map.image()
    }

  def kernel(self):
    return {
      x.coefficients
      for x in self.right_map.kernel()
    }

  def is_exact(self):
    return self.image() == self.kernel()


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

  def check(self):
    return [
      self.exactness_at_sphere(),
      self.exactness_at_hopf_target(),
    ]
  