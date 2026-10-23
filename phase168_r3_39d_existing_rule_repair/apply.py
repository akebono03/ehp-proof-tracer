from pathlib import Path
import ast, shutil, sys

project = Path(__file__).resolve().parent.parent
package = Path(__file__).resolve().parent
changes = {}

def replace_one(path, old, new):
    value = changes.get(path, (project / path).read_text(encoding='utf-8'))
    if value.count(old) != 1:
        raise RuntimeError(f'expected one anchor in {path}: {old[:70]!r}; found {value.count(old)}')
    changes[path] = value.replace(old, new, 1)

# Existing general scalar specialization: accept equivalent concrete generator metadata,
# while keeping equality checks for every other schema.
p = 'phase165_r57_r20_general_specialization.py'
replace_one(p, '''        if not _bind(pattern.source, concrete.source, bindings):
            return False
        if not _bind(pattern.target, concrete.target, bindings):
            return False
        if not _bind(pattern.generator, concrete.generator, bindings):
            return False
        name = _substitute_name(pattern.name, bindings)
        return name == concrete.name''', '''        if pattern.source is not None and not _bind(pattern.source, concrete.source, bindings):
            return False
        if pattern.target is not None and not _bind(pattern.target, concrete.target, bindings):
            return False
        if not _bind(pattern.generator, concrete.generator, bindings):
            return False
        name = _substitute_name(pattern.name, bindings)
        if name == concrete.name:
            return True
        # The registered iota_n schema has no source/target metadata, while
        # older concrete statements use subscript characters in their names.
        if (pattern.name == "ι_n" and pattern.source is None and pattern.target is None
                and concrete.generator is not None
                and concrete.generator.family == "ι"
                and type(concrete.generator.index) is int):
            subscript = str(concrete.generator.index).translate(
                str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            return concrete.name in ("ι" + subscript, "ι_" + str(concrete.generator.index))
        return False''')
replace_one(p, '''    if instantiated != goal:
        return None
    from phase165_prop51_range_guard import allows_typed_specialization''', '''    if instantiated != goal:
        from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
        from proof import Relation, RelationType
        from expression import ScalarSymbol
        n = ScalarSymbol("n")
        is_diagonal = (
            isinstance(source, Relation)
            and source.relation_type is RelationType.EQUALITY
            and source.lhs == TodaPrimaryGroup(n, n)
            and isinstance(source.rhs, FreeCyclicGroup)
            and isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FreeCyclicGroup)
            and bindings.get("n") == goal.lhs.sphere_dimension == goal.lhs.group_dimension
            and _bind(source, goal, dict(bindings))
        )
        if not is_diagonal:
            return None
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    if (isinstance(source, TodaPrimaryGroupZeroStatement)
            and source.group.sphere_dimension == 1
            and isinstance(source.group.group_dimension, ScalarSymbol)
            and bindings.get(source.group.group_dimension.name, 0) <= 1):
        return None
    from phase165_prop51_range_guard import allows_typed_specialization''')
replace_one(p, '''        return _instantiate(premises[0].conclusion, dict(binding))''', '''        # The guard has already checked this exact goal against the registered
        # source, including the iota generator's legacy metadata representation.
        return goal''')

# Add a symbolic circle zero assertion to the EXISTING (5.1) source registry.
p = 'phase165_r12_r15_toda51.py'
replace_one(p, '''    if EXPECTED_CLAUSE not in text or r"\\begin{equation}\\label{5.1}" not in text:''', '''    if (EXPECTED_CLAUSE not in text
            or r"\\pi^{1}_{i}=0\\ (i>1)" not in text
            or r"\\begin{equation}\\label{5.1}" not in text):''')
replace_one(p, '''    return RegistryBridgeResult(registry, (), (ProofStepLink(GENERAL_ASSERTION_ID, step=step),))''', '''    # Reuse the existing scalar-specialization rule for the circle clause.
    # Its i > 1 domain is checked in specialize_typed_statement().
    from expression import ScalarSymbol
    i = ScalarSymbol("i")
    circle_source = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, 1))
    circle_id = "adopted:assertion:toda51:circle_higher_zero"
    registry.add_assertion(AssertionEntry(
        assertion_id=circle_id,
        reference_id=GENERAL_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=circle_source,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("i>1",),
    ))
    circle_step = ProofStep(
        conclusion=circle_source, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.1) general circle higher vanishing",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    return RegistryBridgeResult(registry, (), (
        ProofStepLink(GENERAL_ASSERTION_ID, step=step),
        ProofStepLink(circle_id, step=circle_step),
    ))''')

# Do not let legacy concrete leaves bypass available general sources.
p = 'phase165_r52_r9_shared_math.py'
replace_one(p, '''    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs''', '''    default_sources = sources is None
    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs''')
replace_one(p, '''    # Preserve registered mathematical statements/IDs, but keep one direct
    # GIVEN for the Hopf-image fact; relation views are derived by a rule.''', '''    # Leave archived assertion identities untouched. In the default context,
    # these four old concrete (5.1) GIVENs must be derived by the already
    # registered universal source instead of short-circuiting the Proof Tree.
    if default_sources:
        legacy_ids = {
            "shared:1:adopted:assertion:1",
            "shared:1:adopted:assertion:2",
            "shared:1:adopted:assertion:4",
            "shared:1:adopted:assertion:6",
        }
        joined = RegistryBridgeResult(
            joined.registry, joined.records,
            tuple(link for link in joined.proof_links
                  if link.assertion_id not in legacy_ids),
        )
    # Preserve registered mathematical statements/IDs, but keep one direct
    # GIVEN for the Hopf-image fact; relation views are derived by a rule.''')

# Existing Reference Projection can now show the actual circle source (not a concrete leaf).
p = 'phase168_r3_37c_reference_projection.py'
replace_one(p, '''    from homotopy_groups import TodaIteratedSuspensionMap''', '''    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement''')
replace_one(p, '''        elif isinstance(statement, Toda51BelowDiagonalZeroStatement):''', '''        elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
              and isinstance(statement.group.group_dimension, ScalarSymbol)
              and statement.group.sphere_dimension == 1):
            sentence = r"$\\pi_i^1=0\\quad(i>1)$."
        elif isinstance(statement, Toda51BelowDiagonalZeroStatement):''')

for path, value in changes.items():
    ast.parse(value, filename=path)
for path, value in changes.items():
    target = project / path
    backup = package / 'backup' / path
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(value, encoding='utf-8')
    output = package / 'full_files' / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(value, encoding='utf-8')
    print('PATCHED', path)
print('FULL_FILES', package / 'full_files')
