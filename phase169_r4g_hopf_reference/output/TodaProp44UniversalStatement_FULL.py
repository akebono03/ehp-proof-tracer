@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """Conditional proposition plus its explicitly checked preceding Hopf-fibration premise.

    The fibration statement is printed before Proposition 4.4 in the adopted
    Toda source, not in the proposition environment itself.
    """
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True
    preceding_hopf_fibration_dimensions: tuple[int, ...] = (2, 4, 8)

