def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if (not isinstance(field_names, tuple)
                    or len(field_names) < 2
                    or not is_dataclass(content)
                    or isinstance(content, type)
                    or tuple(field.name for field in fields(content)) != field_names):
                raise ValueError("registered composite field scope is inconsistent")
            statements = tuple(getattr(content, field_name) for field_name in field_names)

        for statement in statements:
            sentence = None
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
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
