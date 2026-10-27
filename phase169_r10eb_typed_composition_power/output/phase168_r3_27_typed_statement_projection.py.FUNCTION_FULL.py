def element_tex(value):
    """Render only supported generators; normalize typed consecutive eta composites."""
    from expression import Composition

    if isinstance(value, Composition):
        from phase169_r10eb_typed_composition_power.display import (
            typed_stable_composition_power_latex,
        )
        power = typed_stable_composition_power_latex(value)
        if power is not None:
            return power

    if isinstance(value, Multiple) and type(value.coefficient) is int:
        inner = element_tex(value.expression)
        return f"{value.coefficient}{inner}" if inner is not None else None
    if isinstance(value, Composition):
        left, right = value.left, value.right
        if not (isinstance(left, HomotopyElement)
                and isinstance(right, HomotopyElement)):
            return None
        left_symbol = getattr(left, "generator", None)
        right_symbol = getattr(right, "generator", None)
        left_index = (getattr(left_symbol, "index", None) if left_symbol is not None
                      else (left.dimension if left.name == "η" else None))
        right_index = (getattr(right_symbol, "index", None) if right_symbol is not None
                       else (right.dimension if right.name == "η" else None))
        left_eta = (left_symbol.family == "η" if left_symbol is not None
                    else left.name == "η")
        right_eta = (right_symbol.family == "η" if right_symbol is not None
                     else right.name == "η")
        if (type(left_index) is int and type(right_index) is int
                and left_eta and right_eta
                and getattr(left_symbol, "decoration", None) is None
                and getattr(right_symbol, "decoration", None) is None
                and right_index == left_index + 1
                and element_tex(left) == rf"\eta_{{{left_index}}}"
                and element_tex(right) == rf"\eta_{{{right_index}}}"):
            return rf"\eta_{{{left_index}}}^{{2}}"
        return None
    if isinstance(value, HomotopyElement):
        symbol = value.generator
        if symbol is not None and type(symbol.index) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}.get(symbol.family)
            if family is not None:
                return f"{family}_{{{symbol.index}}}"
        if value.name in ("η", "ι", "ν", "σ") and type(value.dimension) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}[value.name]
            return f"{family}_{{{value.dimension}}}"
    return None
