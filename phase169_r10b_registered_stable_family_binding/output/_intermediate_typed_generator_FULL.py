def _intermediate_typed_generator(source: object, target: object, step: int,
                                  exponent: int) -> object | None:
    """Build DB-identified typed candidates, never a proven image equality.

    The HyoujiGen kinds=0 row is identity metadata. The downstream R7 rule
    continues to demand independently proved GeneratorImage obligations.
    """
    if type(step) is not int or type(exponent) is not int or not 0 <= step <= exponent:
        return None
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        from phase169_r10b_registered_stable_family_binding.family_registry import (
            registered_stable_family_pair,
        )
        family = registered_stable_family_pair(source, target)
        s, t = source.generator, target.generator
        if (family is None
                or not isinstance(s, GeneratorSymbol)
                or not isinstance(t, GeneratorSymbol)
                or type(s.index) is not int
                or type(t.index) is not int
                or t.index - s.index != exponent
                or target.dimension - source.dimension != exponent
                or target.source - source.source != exponent
                or target.target - source.target != exponent):
            return None
        if step == 0:
            return source
        if step == exponent:
            return target
        middle_index = s.index + step
        return replace(
            source,
            name=family.name_at(middle_index),
            dimension=source.dimension + step,
            source=source.source + step,
            target=source.target + step,
            generator=replace(s, index=middle_index),
        )
    if isinstance(source, Composition) and isinstance(target, Composition):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Composition(left, right) if left is not None and right is not None else None
    if isinstance(source, Sum) and isinstance(target, Sum):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Sum(left, right) if left is not None and right is not None else None
    if (isinstance(source, Multiple) and isinstance(target, Multiple)
            and source.coefficient == target.coefficient):
        inner = _intermediate_typed_generator(source.expression, target.expression,
                                              step, exponent)
        return Multiple(source.coefficient, inner) if inner is not None else None
    if step == 0:
        return source
    if step == exponent:
        return target
    if (isinstance(target, IteratedSuspension)
            and target.expression == source
            and type(target.exponent) is int
            and target.exponent == exponent):
        return IteratedSuspension(source, step)
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent - source.exponent == exponent):
        return IteratedSuspension(source.expression, source.exponent + step)
    return None
