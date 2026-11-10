"""Common typed reference sentence projection. No source lookup."""
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex


def _verified_source_sentence(statement: object) -> str | None:
    """Render a fully source-screened typed statement without deducing a fact."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )
    return None


def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Render an actual cited GIVEN when an assertion-ID body was not attached.

    Preserve the established Lemma 5.4 fallback. For Toda (4.8) and (5.5),
    require a unique canonical cited GIVEN with explicit source provenance,
    plus reverified adopted source text and chronological position. This is
    display-only: neither source links nor ProofSteps are created here.
    """
    from proof import LiteratureReference, ProofRule, ProofStep

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    candidates = tuple(
        (step, _verified_source_sentence(step.conclusion))
        for step in cited_steps
        if isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
        and not step.premises
    )
    verified = tuple(
        sentence for step, sentence in candidates
        if sentence is not None and locator == "Lemma 5.4"
    )
    if verified:
        return verified if len(verified) == 1 else ()

    from phase174_r3_r6_r4_common_reference.projection import (
        project_verified_cited_toda_given_reference_body,
    )
    return project_verified_cited_toda_given_reference_body(reference, cited_steps)


def _project_certified_general_reference_body(assertion: object, registry: object,
                                         statement: object) -> str | None:
    """Show already-cited general laws when source identity and typed data agree."""
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin, ReferenceKind,
        UnifiedStatementRegistry,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
    )
    from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
        Prop27UniversalLiteratureStatement,
    )

    if not isinstance(registry, UnifiedStatementRegistry) or not isinstance(assertion, AssertionEntry):
        return None
    try:
        if registry.assertion(assertion.assertion_id) is not assertion:
            return None
        reference = registry.reference(assertion.reference_id)
    except KeyError:
        return None
    if (assertion.kind is not AssertionKind.STATEMENT
            or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.dependencies
            or assertion.content is not statement
            or not isinstance(reference.publication_position, int)
            or reference.publication_position <= 0):
        return None

    if type(statement) is CitedFamilyAnnihilator:
        if (statement != CitedFamilyAnnihilator(
                left_family_id=4, right_family_id=2,
                minimum_left_index=6, right_index_offset=3,
                citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
            )
                or not assertion.assertion_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general:statement')
                or not assertion.reference_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general')
                or assertion.scope != 'nu_n composed eta_(n+3) = 0, n>=6'
                or reference.kind is not ReferenceKind.EQUATION
                or reference.locator != '(5.9)'
                or reference.source_id != (
                    'sources/toda/Toda_05_2.tex '
                    '(adopted; printed edition unchecked)'
                )):
            return None
        return r'$n\ge6$ に対して, $\nu_n\circ\eta_{n+3}=0$.'

    if type(statement) is Prop27UniversalLiteratureStatement:
        if (statement != Prop27UniversalLiteratureStatement()
                or not assertion.assertion_id.endswith(
                    ':typed_literature:assertion:toda:prop2.7')
                or not assertion.reference_id.endswith(
                    ':typed_literature:toda:prop2.7')
                or assertion.scope != ('n >= 2', 'n even', 'sign undetermined')
                or reference.kind is not ReferenceKind.PROPOSITION
                or reference.locator != 'Proposition 2.7'
                or reference.source_id != 'toda:tex:ch2:0018'):
            return None
        return (r'$n\ge2$ を偶数とすると, '
                r'$H(\Delta(\iota_{2n+1}))=\pm2\iota_{2n-1}$.')
    return None

def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        TodaPreProp44SplittingStatement,
    )
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if not isinstance(field_names, tuple) or len(field_names) < 2:
                raise ValueError("registered composite field scope is inconsistent")
            content_fields = (
                tuple(field.name for field in fields(content))
                if is_dataclass(content) and not isinstance(content, type) else ()
            )
            if content_fields == field_names:
                statements = tuple(getattr(content, field_name) for field_name in field_names)
            else:
                # The registered component bridge retains the parent's scope
                # on an atomic child. Validate the exact parent dependency and
                # field content instead of expanding this child a second time.
                dependencies = getattr(assertion, "dependencies", ())
                if not isinstance(dependencies, tuple) or len(dependencies) != 1:
                    raise ValueError("registered composite field scope is inconsistent")
                parent = registry.assertion(dependencies[0])
                parent_content = parent.content
                parent_fields = (
                    tuple(field.name for field in fields(parent_content))
                    if is_dataclass(parent_content) and not isinstance(parent_content, type)
                    else ()
                )
                if (parent.scope != scope
                        or parent_fields != field_names
                        or not any(
                            type(content) is type(getattr(parent_content, field_name))
                            and content == getattr(parent_content, field_name)
                            for field_name in field_names
                        )):
                    raise ValueError("registered composite field scope is inconsistent")

        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()):
                sentence = (
                    r"$\alpha\in\pi_{2n-1}^{n}$ で "
                    r"$H(\alpha)=\pm\iota_{2n-1}$ とする."
                    "\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\n"
                    r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\;\cong\;}\pi_i^n,\quad"
                    r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$."
                    "\n"
                    r"特に $E:\pi_{i-1}^{n-1}\to\pi_i^{n}$ は単射である."
                )
            elif (type(statement) is TodaPreProp44SplittingStatement
                  and statement == TodaPreProp44SplittingStatement()):
                sentence = (
                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\to S^n$ "
                    r"が存在し, 任意の $i$ で "
                    r"$E+h_*:\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\cong}\pi_i^n$ が成り立つ "
                    r"(Steenrod 1951 を引用)."
                )
            elif isinstance(statement, TodaProp42GeneralExactnessStatement):
                sentence = (
                    r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                    r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                    r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                    r"\xrightarrow{E}\pi_i^{n+1}$ は完全."
                )
            elif isinstance(statement, Toda52UniversalStatement):
                if (statement.variable == "i" and statement.minimum_i == 3
                        and statement.map_formula == "alpha -> eta_2 o alpha"
                        and statement.source_group == "pi_i^3"
                        and statement.target_group == "pi_i^2"):
                    sentence = (
                        r"$i\ge 3$ に対し, "
                        r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
                    )
            elif isinstance(statement, Toda45IsomorphismStatement):
                mapping = statement.map
                n, m, k = ScalarSymbol("n"), ScalarSymbol("m"), ScalarSymbol("k")
                if (
                    isinstance(mapping, TodaIteratedSuspensionMap)
                    and mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                    and mapping.source_group.sphere_dimension == n
                    and mapping.target_group.sphere_dimension == m
                    and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                    and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
                ):
                    sentence = (
                        r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ."
                    )
            elif isinstance(statement, Relation) and _is_generic_eta_group_relation(statement):
                # The typed source schema, already guarded by the general
                # eta-group recognizer, has the documented n >= 4 range.
                variable = statement.lhs.sphere_dimension.name
                sentence = (
                    r"$\pi_{" + variable + r"+1}^{" + variable + r"}="
                    r"\mathbb{Z}/2\{\eta_{" + variable + r"}\}"
                    r"\quad(" + variable + r"\ge4)$."
                )
            if sentence is None:
                sentence = _project_certified_general_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
            if sentence is None:
                latex, fallback = _group_proof_statement_latex(statement)
                if latex is not None and fallback is None:
                    sentence = "$" + latex + "$."
            if (sentence is not None and r"\pi_{n}^{n}" in sentence
                    and r"\mathbb{Z}" in sentence and r"n\ge" not in sentence
                    and sentence.endswith("$.")):
                sentence = sentence[:-2] + r"\quad(n\ge 1)$."
            if sentence is not None and sentence not in result:
                result.append(sentence)
    return tuple(result)
