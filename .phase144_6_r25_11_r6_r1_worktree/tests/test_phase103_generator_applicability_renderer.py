import pytest

from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_applicability_renderer import (
  render_repository_generator_applicability_markdown,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from proof import (
  InferenceRule,
  PremisePattern,
)


def build_renderer_catalog(
  *,
  fixed_point_safe=True,
):
  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key=(
        "phase103.renderer."
        "candidate"
      ),
      rule=InferenceRule(
        name=(
          "phase103 renderer "
          "candidate rule"
        ),
        premise_patterns=(
          PremisePattern(),
        ),
      ),
      conclusion_type=object,
      fixed_point_safe=(
        fixed_point_safe
      ),
    )
  )

  return catalog


def test_phase103_5_renderer_renders_candidate_metadata():
  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      build_renderer_catalog(),
    )
  )

  markdown = (
    render_repository_generator_applicability_markdown(
      result
    )
  )

  assert (
    "# Applicable theorem / lemma candidates for $\\nu'$"
    in markdown
  )

  assert (
    "Proof-scope occurrences:"
    in markdown
  )

  assert (
    "Applicability candidates:"
    in markdown
  )

  assert (
    "## Candidates"
    in markdown
  )

  assert (
    "`phase103.renderer.candidate`"
    in markdown
  )

  assert (
    "Rule: phase103 renderer candidate rule"
    in markdown
  )

  assert (
    "Premise index: 0"
    in markdown
  )

  assert (
    "Fixed-point safe: yes"
    in markdown
  )

  assert (
    "Root:"
    in markdown
  )

  assert (
    "Depth:"
    in markdown
  )

  assert (
    "Source statement type:"
    in markdown
  )

  assert (
    "Bindings:"
    in markdown
  )


def test_phase103_5_renderer_zero_candidate_result_has_counts_only():
  result = (
    explore_standard_repository_generator_applicability_input(
      "eta_999",
      build_renderer_catalog(),
    )
  )

  markdown = (
    render_repository_generator_applicability_markdown(
      result
    )
  )

  assert (
    "Proof-scope occurrences: 0"
    in markdown
  )

  assert (
    "Applicability candidates: 0"
    in markdown
  )

  assert (
    "## Candidates"
    not in markdown
  )


def test_phase103_5_renderer_rejects_wrong_type():
  with pytest.raises(
    TypeError,
    match=(
      "result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    render_repository_generator_applicability_markdown(
      object()
    )
