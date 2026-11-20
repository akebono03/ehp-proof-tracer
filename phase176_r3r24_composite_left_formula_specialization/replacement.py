def _formula_parts(goal: object) -> tuple[object, HomotopyElement] | None:
    """Recognize the cited right-Hopf formula for explicitly typed maps.

    The left factor may be a typed composite. Neither a symbolic display
    name nor associativity alone is evidence of a valid sphere-map type.
    """
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints

    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return None
    if not isinstance(goal.lhs, MapApplication) or goal.lhs.map != EHP_H_MAP:
        return None
    product = goal.lhs.expression
    if not isinstance(product, Composition):
        return None
    alpha, right = product.left, product.right
    if not isinstance(alpha, (HomotopyElement, Composition)):
        return None
    if not isinstance(right, Suspension) or not isinstance(right.expression, HomotopyElement):
        return None
    beta = right.expression
    alpha_endpoints = expression_endpoints(alpha)
    beta_endpoints = expression_endpoints(beta)
    if alpha_endpoints is None or beta_endpoints is None:
        return None
    suspended_endpoints = (beta_endpoints[0] + 1, beta_endpoints[1] + 1)
    if alpha_endpoints[0] != suspended_endpoints[1]:
        return None
    expected = Composition(MapApplication(EHP_H_MAP, alpha), right)
    return (alpha, beta) if goal.rhs == expected else None
