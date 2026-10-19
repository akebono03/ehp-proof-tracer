from repository_operation_query_facade import (
  query_standard_repository_operation_input,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
from repository_operation_query_proof_replay import (
  build_repository_operation_query_proof_replay,
)
from repository_operation_query_proof_replay_presentation import (
  build_repository_operation_query_proof_replay_presentation,
)
from repository_operation_query_proof_replay_renderer import (
  render_repository_operation_query_proof_replay_markdown,
)
from repository_operation_query_proof_replay_statement_presentation import (
  build_repository_operation_query_proof_replay_statement_presentation,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
  TodaDeltaSurjectiveStatement,
  TodaLemma57TwoIota5ImageMembershipStatement,
  TodaProp56FiniteDimensionalStatement,
)


def _query_presentation(
  query_input,
):
  return (
    build_repository_operation_query_presentation(
      query_standard_repository_operation_input(
        query_input
      )
    )
  )


def _replay_presentation(
  query_input,
  fact_number=None,
):
  query_presentation = (
    _query_presentation(
      query_input
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      query_presentation,
      fact_number=fact_number,
    )
  )

  return (
    build_repository_operation_query_proof_replay_presentation(
      replay
    )
  )


def _first_statement_of_type(
  presentation,
  statement_type,
):
  return next(
    replay_step.proof_step.conclusion
    for replay_step in presentation.steps
    if isinstance(
      replay_step.proof_step.conclusion,
      statement_type,
    )
  )


def test_phase110_12_nu_prime_specialization_uses_bracket_membership_latex():
  presentation = (
    _replay_presentation(
      "H(nu_prime)",
      fact_number=2,
    )
  )

  statement = (
    _first_statement_of_type(
      presentation,
      Toda53NuPrimeBracketSpecializationStatement,
    )
  )

  statement_presentation = (
    build_repository_operation_query_proof_replay_statement_presentation(
      statement
    )
  )

  assert (
    statement_presentation.latex
    == (
      r"\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    )
  )

  assert (
    statement_presentation.fallback_type_name
    is None
  )


def test_phase110_12_nu_prime_specialization_renderer_has_no_raw_repr():
  markdown = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "H(nu_prime)",
        fact_number=2,
      )
    )
  )

  assert (
    r"$\nu' \in "
    r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
    in markdown
  )

  assert (
    "Toda53NuPrimeBracketSpecializationStatement("
    not in markdown
  )

  assert (
    "HomotopyElement(name="
    not in markdown
  )


def test_phase110_12_lemma57_hypothesis_renders_image_membership():
  presentation = (
    _replay_presentation(
      "E(eta_2 o nu_prime)"
    )
  )

  statement = (
    _first_statement_of_type(
      presentation,
      TodaLemma57TwoIota5ImageMembershipStatement,
    )
  )

  statement_presentation = (
    build_repository_operation_query_proof_replay_statement_presentation(
      statement
    )
  )

  assert (
    statement_presentation.latex
    == (
      r"E^{2}\nu' "
      r"\in 2\iota_{5}\circ \pi_{8}^{5}"
    )
  )

  assert (
    statement_presentation.fallback_type_name
    is None
  )


def test_phase110_12_lemma57_renderer_has_no_raw_repr():
  markdown = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "E(eta_2 o nu_prime)"
      )
    )
  )

  assert (
    r"$E^{2}\nu' "
    r"\in 2\iota_{5}\circ \pi_{8}^{5}$"
    in markdown
  )

  assert (
    "TodaLemma57TwoIota5ImageMembershipStatement("
    not in markdown
  )


def test_phase110_12_delta_surjective_renders_map_property():
  presentation = (
    _replay_presentation(
      "eta_2 o nu_prime",
      fact_number=4,
    )
  )

  statement = (
    _first_statement_of_type(
      presentation,
      TodaDeltaSurjectiveStatement,
    )
  )

  statement_presentation = (
    build_repository_operation_query_proof_replay_statement_presentation(
      statement
    )
  )

  assert (
    statement_presentation.latex
    == (
      r"\Delta: "
      r"\pi_{8}^{5} \to \pi_{6}^{2} "
      r"\text{ is surjective}"
    )
  )

  assert (
    statement_presentation.fallback_type_name
    is None
  )


def test_phase110_12_aggregate_uses_safe_type_fallback():
  presentation = (
    _replay_presentation(
      "eta_2 o nu_prime",
      fact_number=4,
    )
  )

  statement = (
    _first_statement_of_type(
      presentation,
      TodaProp56FiniteDimensionalStatement,
    )
  )

  statement_presentation = (
    build_repository_operation_query_proof_replay_statement_presentation(
      statement
    )
  )

  assert (
    statement_presentation.latex
    is None
  )

  assert (
    statement_presentation.fallback_type_name
    == "TodaProp56FiniteDimensionalStatement"
  )


def test_phase110_12_replay_renderer_removes_python_dataclass_repr_leakage():
  markdown = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "eta_2 o nu_prime",
        fact_number=4,
      )
    )
  )

  assert (
    r"$\Delta: "
    r"\pi_{8}^{5} \to \pi_{6}^{2} "
    r"\text{ is surjective}$"
    in markdown
  )

  assert (
    "`TodaProp56FiniteDimensionalStatement`"
    in markdown
  )

  assert (
    "TodaDeltaSurjectiveStatement("
    not in markdown
  )

  assert (
    "TodaProp56FiniteDimensionalStatement("
    not in markdown
  )

  assert (
    "HomotopyElement(name="
    not in markdown
  )

  assert (
    "Relation(lhs="
    not in markdown
  )

  assert (
    "object at 0x"
    not in markdown
  )


def test_phase110_12_existing_supported_relation_rendering_is_unchanged():
  markdown = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "H(nu_prime)",
        fact_number=1,
      )
    )
  )

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$"
    in markdown
  )

  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$"
    in markdown
  )

  assert (
    r"$E^{2}\eta_{3} = \eta_{5}$"
    in markdown
  )


def test_phase110_12_statement_rendering_is_deterministic():
  first = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "eta_2 o nu_prime",
        fact_number=4,
      )
    )
  )

  second = (
    render_repository_operation_query_proof_replay_markdown(
      _replay_presentation(
        "eta_2 o nu_prime",
        fact_number=4,
      )
    )
  )

  assert first == second
