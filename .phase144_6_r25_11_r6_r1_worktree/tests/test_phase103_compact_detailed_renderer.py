from repository_generator_applicability_renderer import (
  render_repository_generator_applicability_compact_markdown,
  render_repository_generator_applicability_detailed_markdown,
  render_repository_generator_applicability_markdown,
)
from test_phase103_rule_family_grouped_renderer import (
  _build_same_name_multi_catalog_result,
)


def test_phase103_6c5_compact_renderer_keeps_summary_and_rule_families():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_compact_markdown(
      result
    )
  )

  assert (
    "Applicability candidates: 5"
    in markdown
  )

  assert (
    "Source statements with candidates: 2"
    in markdown
  )

  assert (
    "Rule groups: 4"
    in markdown
  )

  assert (
    "Rule families: 3"
    in markdown
  )

  assert (
    "Rule: first grouped rule"
    in markdown
  )

  assert (
    "Catalog entries: 2"
    in markdown
  )


def test_phase103_6c5_compact_renderer_hides_catalog_provenance_details():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_compact_markdown(
      result
    )
  )

  assert "  - Catalog: `" not in markdown
  assert "Fixed-point safe:" not in markdown
  assert "Premise index:" not in markdown
  assert "Bindings:" not in markdown


def test_phase103_6c5_detailed_renderer_keeps_full_provenance():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_detailed_markdown(
      result
    )
  )

  assert (
    "phase103.grouped.first.second-catalog"
    in markdown
  )

  assert (
    "Fixed-point safe: yes"
    in markdown
  )

  assert (
    "Premise index: 0; Bindings: 0"
    in markdown
  )


def test_phase103_6c5_legacy_renderer_remains_detailed_for_api_compatibility():
  result = (
    _build_same_name_multi_catalog_result()
  )

  assert (
    render_repository_generator_applicability_markdown(
      result
    )
    == (
      render_repository_generator_applicability_detailed_markdown(
        result
      )
    )
  )
