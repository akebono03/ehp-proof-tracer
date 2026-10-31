# Phase 171 R20R8 — 変更コード全文

## 変更ファイルと対象

1. `phase171_r2j_r4_r7_nonzero_nu_order/source.py`：最終行の後に `expand_public_nonzero_double_from_cited_source` を追加。既存の import・クラス・関数は変更しない。追加関数内の import は次の関数全文に含めた。
2. `phase165_r52_r9_shared_math.py`：`shared_expansion_provider` 関数内で、R20R7 の非零性候補追加行の直後に以下の局所 import と候補追加を行う。ファイル先頭の import は変更しない。
3. `phase171_r20r8_public_double_nonzero/install.py`、`audit.py`、`tests/test_install.py`、`tests/test_source.py`、`run.ps1` は本 ZIP に全文収録。

本番ファイルの変更後の **`shared_expansion_provider()` 全文**は、実行後 `phase171_r20r8_public_double_nonzero/output/SHARED_PROVIDER_FUNCTION_FULL_AFTER.py` に出力する。変更後の **`source.py` 全文**は同じ出力先の `SOURCE_FULL_AFTER.py` に出力する。既存関数・クラスの定義を切り詰めず、置換可能な単位で保存する。

## 新規関数全文（`source.py` 末尾）

```python
def expand_public_nonzero_double_from_cited_source(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer a double-nonzero proof from screened equations and typed prior goals.

    A structured database generator supplies only a *candidate* image goal.
    The earlier cyclic group relation and the cited double relation must be
    present in screened source claims; both inferred premises are reconstructed
    in the public recursive search. No database goal is accepted as a proof.
    """
    from phase165_r3_recursive_search import GoalExpansion
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    from phase171_r2j_r4_r3_double_image_bridge.source import (
        typed_double_image_conclusion,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must contain screened fixed statements")
    if (
        not isinstance(goal, NonZeroGroupElement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.element, Multiple)
        or type(goal.element.coefficient) is not int
        or goal.element.coefficient != 2
    ):
        return ()
    group = goal.group
    q, n = group.group_dimension, group.sphere_dimension
    if (
        type(q) is not int
        or type(n) is not int
        or n < 3
        or q <= n
        or _endpoints(goal.element.expression) != (q, n)
    ):
        return ()
    earlier_group = TodaPrimaryGroup(q - 1, n - 1)
    injection = MapInjective(TodaSuspensionMap(earlier_group, group))
    prior_sources = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == earlier_group
        and isinstance(claim.rhs, FiniteCyclicGroup)
        and type(claim.rhs.order) is int
        and claim.rhs.order > 1
    )
    # The structured database is used to type a goal, NEVER to establish the
    # earlier group as a premise or produce a GIVEN.
    typed_candidates = database_structured_group_goal_candidates(
        n=n - 1, k=q - n,
    )
    double_sources = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == goal.element
    )
    proposals: list[GoalExpansion] = []
    for prior in prior_sources:
        for typed in typed_candidates:
            if (
                not isinstance(typed, Relation)
                or typed.relation_type is not RelationType.EQUALITY
                or typed.lhs != earlier_group
                or not isinstance(typed.rhs, FiniteCyclicGroup)
                or typed.rhs.order != prior.rhs.order
                or not same_registered_group_presentation(prior.rhs, typed.rhs)
            ):
                continue
            for cited_double in double_sources:
                image = GeneratorImage(
                    map=TodaSuspensionMap(earlier_group, group),
                    source_generator=typed.rhs.generator,
                    target_generator=cited_double.rhs,
                )
                typed_equality = typed_double_image_conclusion(
                    cited_double, image,
                )
                if typed_equality is None:
                    continue
                nonzero_image = NonZeroGroupElement(group, typed_equality.rhs)
                if (
                    nonzero_cyclic_generator_image(
                        prior, injection, typed_equality.rhs,
                    ) != nonzero_image
                    or nonzero_double_from_equality(
                        typed_equality, nonzero_image,
                    ) != goal
                ):
                    continue
                option = GoalExpansion(
                    inferred_nonzero_double_rule(
                        goal, typed_equality, nonzero_image,
                    ),
                    (typed_equality, nonzero_image),
                )
                if not any(
                    existing.subgoals == option.subgoals
                    and existing.rule.name == option.rule.name
                    for existing in proposals
                ):
                    proposals.append(option)
    # Alternative source-grounded proofs may coexist; recursive search takes
    # the first completed certified derivation, not a uniquely chosen route.
    # Direct-reference ambiguity is still checked by the search itself.
    return tuple(proposals)
```

## `shared_expansion_provider` 内の追加箇所（局所 import 全文）

既存の次の1行の直後に追加する。

```python
        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_nonzero_double_from_cited_source,
        )
        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))
```

`run.ps1` は限定 pytest の後に独立した R4-R7 証明木との一致監査を実行する。完了条件は `PHASE171_R20R8_DOUBLE_NONZERO=CERTIFIED_PUBLIC_PROPOSAL_PRESENT`。この段階では等式サブゴールの公開証明は未接続。
