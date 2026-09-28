from pathlib import Path
import re

project = Path(r"C:\Users\user\Dropbox\Python\fitz\ehp_proof")

phase114 = (
    project
    / "tests"
    / "test_phase114_3_nu5_operation_query_handoff.py"
)

phase115 = (
    project
    / "tests"
    / "test_phase115_sigma11_operation_query_handoff.py"
)


def add_resolver_import(text):
    import_block = """from generator_input import (
  resolve_generator_input,
)
"""

    if "from generator_input import (" in text:
        return text

    anchor = "from proof import (\n"

    if anchor not in text:
        raise RuntimeError(
            "proof import anchor not found"
        )

    return text.replace(
        anchor,
        import_block + anchor,
        1,
    )


def replace_function(
    text,
    function_name,
    replacement,
):
    pattern = (
        r"(?ms)^def "
        + re.escape(function_name)
        + r"\(\):.*?(?=^def |\Z)"
    )

    text, count = re.subn(
        pattern,
        lambda match: replacement,
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    return text


# --------------------------------------------------
# Phase 114
# --------------------------------------------------

text = phase114.read_text(
    encoding="utf-8",
)

text = add_resolver_import(
    text
)

text = replace_function(
    text,
    "test_phase114_3_facade_handoff_derives_e_nu5_equals_nu6",
    """def test_phase114_3_facade_handoff_derives_e_nu5_equals_nu6():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  assert result.found

  assert all(
    isinstance(
      match.statement,
      Relation,
    )
    for match in result.matches
  )

  assert all(
    match.statement.relation_type
    is RelationType.EQUALITY
    for match in result.matches
  )

  assert all(
    isinstance(
      match.statement.lhs,
      Suspension,
    )
    for match in result.matches
  )

  assert all(
    match.statement.lhs.expression.generator
    == resolve_generator_input(
      "nu_5"
    )
    for match in result.matches
  )

  assert all(
    match.statement.rhs.generator
    == resolve_generator_input(
      "nu_6"
    )
    for match in result.matches
  )

  assert all(
    match.match_kind
    is RepositoryOperationQueryMatchKind.SUSPENSION_RELATION
    for match in result.matches
  )


""",
)

text = replace_function(
    text,
    "test_phase114_3_handoff_preserves_symbolic_bridge_as_provenance",
    """def test_phase114_3_handoff_preserves_symbolic_bridge_as_provenance():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  root_step = (
    result.matches[
      0
    ].scope_node.proof_step
  )

  assert root_step.rule is ProofRule.INFERENCE
  assert len(root_step.premises) == 1

  symbolic_step = root_step.premises[
    0
  ]

  assert isinstance(
    symbolic_step.conclusion,
    Relation,
  )

  assert isinstance(
    symbolic_step.conclusion.lhs,
    IteratedSuspension,
  )

  assert (
    symbolic_step.conclusion.lhs
    .expression
    .generator
    == resolve_generator_input(
      "nu_5"
    )
  )


""",
)

phase114.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)

print(
    "Repaired Phase 114 tests."
)


# --------------------------------------------------
# Phase 115
# --------------------------------------------------

text = phase115.read_text(
    encoding="utf-8",
)

text = add_resolver_import(
    text
)

text = replace_function(
    text,
    "test_phase115_4_existing_nu5_handoff_remains_available",
    """def test_phase115_4_existing_nu5_handoff_remains_available():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  assert result.found

  assert any(
    (
      isinstance(
        match.statement,
        Relation,
      )
      and isinstance(
        match.statement.lhs,
        Suspension,
      )
      and match.statement.lhs
      .expression
      .generator
      == resolve_generator_input(
        "nu_5"
      )
      and match.statement.rhs.generator
      == resolve_generator_input(
        "nu_6"
      )
    )
    for match in result.matches
  )


""",
)

phase115.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)

print(
    "Repaired Phase 115 tests."
)
