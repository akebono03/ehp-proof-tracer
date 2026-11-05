@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """Toda Proposition 4.4: a conditional isomorphism, not existence of alpha.

    The hypothesis H(alpha)=+/-iota is proved independently before use.
    The preceding Hopf-fibration paragraph is NOT part of the proposition.
    """
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True
