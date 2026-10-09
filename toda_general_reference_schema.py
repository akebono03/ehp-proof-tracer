"""Phase 162 R5-2: fixed literature statements, independent of ProofStep instances.

Each catalog entry represents a source statement, not its applied conclusion.
Component identities remain aligned with toda_literature_statement_boundary.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneralReferenceComponent:
    component_key: str
    statement_latex: str

    def __post_init__(self) -> None:
        if not self.component_key or not isinstance(self.component_key, str):
            raise ValueError("component_key must be a nonempty str")
        if not self.statement_latex or not isinstance(self.statement_latex, str):
            raise ValueError("statement_latex must be a nonempty str")


@dataclass(frozen=True)
class GeneralReferenceStatement:
    locator: str
    components: tuple[GeneralReferenceComponent, ...]
    conditions_latex: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.locator, str) or not self.locator:
            raise ValueError("locator must be a nonempty str")
        if not isinstance(self.components, tuple) or not self.components:
            raise ValueError("components must be a nonempty tuple")
        if not all(isinstance(item, GeneralReferenceComponent) for item in self.components):
            raise TypeError("components must contain GeneralReferenceComponent")
        keys = tuple(item.component_key for item in self.components)
        if len(set(keys)) != len(keys):
            raise ValueError("component keys must be unique")
        if not isinstance(self.conditions_latex, tuple) or not all(
            isinstance(condition, str) and condition for condition in self.conditions_latex
        ):
            raise TypeError("conditions_latex must contain nonempty strings")


_GENERAL_REFERENCE_CATALOG = (
    GeneralReferenceStatement(
        locator="(4.5)",
        conditions_latex=(r"n\ge k+2", r"m\ge n"),
        components=(
            GeneralReferenceComponent(
                "stable_range_suspension_isomorphism",
                r"E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}",
            ),
        ),
    ),
    GeneralReferenceStatement(
        locator="(5.3)",
        components=(
            GeneralReferenceComponent(
                "nu_prime_bracket_definition",
                r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}",
            ),
            GeneralReferenceComponent(
                "nu_prime_membership", r"\nu'\in\pi_{6}^{3}",
            ),
            GeneralReferenceComponent(
                "nu_prime_double_relation",
                r"2\nu'=\eta_{3}\eta_{4}\eta_{5}",
            ),
            GeneralReferenceComponent(
                "nu_prime_hopf_relation", r"H(\nu')=\eta_{5}",
            ),
        ),
    ),
    GeneralReferenceStatement(
        locator="Proposition 5.1",
        components=(
            GeneralReferenceComponent(
                "pi3_2_group_relation", r"\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}",
            ),
            GeneralReferenceComponent(
                "eta2_hopf_relation", r"H(\eta_{2})=\iota_{3}",
            ),
            GeneralReferenceComponent(
                "delta_iota5_relation", r"\Delta(\iota_{5})=\pm2\eta_{2}",
            ),
            GeneralReferenceComponent(
                "higher_eta_group_relation", r"\pi_{n+1}^{n}=\mathbb{Z}/2\{\eta_{n}\}\quad(n\ge3)",
            ),
        ),
    ),
)


def get_general_reference_statement(locator: str) -> GeneralReferenceStatement | None:
    if not isinstance(locator, str):
        raise TypeError("locator must be a str")
    return next((item for item in _GENERAL_REFERENCE_CATALOG if item.locator == locator), None)


def render_general_reference_statement_lines(locator: str) -> tuple[str, ...] | None:
    """Return the source's fixed formula, never an applied ProofStep conclusion."""
    statement = get_general_reference_statement(locator)
    if statement is None:
        return None
    if statement.conditions_latex:
        conditions = r",\quad ".join(statement.conditions_latex)
        return ("$" + conditions + r"\quad \Longrightarrow\quad " + statement.components[0].statement_latex + "$.",)
    return tuple("$" + component.statement_latex + "$." for component in statement.components)
