"""Common typed reference sentence projection. No source lookup."""
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex


def project_reference_bodies(registry, assertion_ids):
    if registry is None:
        return ()
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement

    result = []
    for assertion_id in assertion_ids:
        statement = registry.assertion(assertion_id).content
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
                r"Proposition 4.2 により, EHP の列 "
                r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                r"\xrightarrow{E}\pi_i^{n+1}$ は完全である."
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
