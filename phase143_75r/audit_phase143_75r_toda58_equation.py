from collections import Counter, defaultdict
from dataclasses import fields

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


TARGET_NAME = "Toda58EquationStatement"
EXPECTED_OCCURRENCES = 45
EXPECTED_GROUPS = 41


def _try_render(value):
  try:
    latex = render_repository_conclusion_latex(
      value
    )
  except (TypeError, ValueError):
    latex = None

  if latex is not None:
    return (
      "repository",
      latex,
    )

  try:
    latex = render_toda_proof_statement_latex(
      value
    )
  except (TypeError, ValueError):
    latex = None

  if latex is not None:
    return (
      "toda",
      latex,
    )

  return (
    "none",
    None,
  )


def main():
  occurrences = 0
  groups = set()
  statement_field_signatures = Counter()
  component_type_counts = defaultdict(Counter)
  component_render_counts = defaultdict(Counter)
  component_render_samples = defaultdict(dict)
  literature_type_signatures = Counter()
  rule_counts = Counter()
  rule_to_statement_shape = defaultdict(Counter)
  semantic_failures = []
  build_errors = []
  representative_statements = {}

  scanned_groups = 0
  presentation_nodes = 0

  for n in range(2, 16):
    for k in range(0, 8):
      group_label = (
        "pi_"
        + str(n + k)
        + "^"
        + str(n)
      )

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(
          replay
        )
      except Exception as exc:
        build_errors.append(
          (
            group_label,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      scanned_groups += 1
      presentation_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        step = node.proof_step
        statement = step.conclusion

        if type(statement).__name__ != TARGET_NAME:
          continue

        occurrences += 1
        groups.add(group_label)

        statement_fields = tuple(
          field.name
          for field in fields(statement)
        )
        statement_field_signatures[
          statement_fields
        ] += 1

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else "<no rule>"
        )
        rule_counts[rule_name] += 1

        if rule_name not in representative_statements:
          representative_statements[
            rule_name
          ] = repr(statement)

        component_shape = []

        for field_name in (
          "delta_nu_relation",
          "whitehead_nu_relation",
          "delta_whitehead_relation",
        ):
          value = getattr(
            statement,
            field_name,
            None,
          )
          value_type = type(value).__name__
          component_type_counts[
            field_name
          ][
            value_type
          ] += 1

          render_source, latex = _try_render(
            value
          )
          component_render_counts[
            field_name
          ][
            render_source
          ] += 1

          if (
            latex is not None
            and render_source
            not in component_render_samples[
              field_name
            ]
          ):
            component_render_samples[
              field_name
            ][
              render_source
            ] = latex

          component_shape.append(
            (
              field_name,
              value_type,
              render_source,
            )
          )

          if value is None:
            semantic_failures.append(
              (
                group_label,
                field_name,
                "missing component",
              )
            )

        literature = getattr(
          statement,
          "literature_statements",
          None,
        )

        if isinstance(literature, tuple):
          literature_signature = tuple(
            type(item).__name__
            for item in literature
          )
        else:
          literature_signature = (
            "<not tuple>",
          )

        literature_type_signatures[
          literature_signature
        ] += 1

        rule_to_statement_shape[
          rule_name
        ][
          (
            statement_fields,
            tuple(component_shape),
            literature_signature,
          )
        ] += 1

  print("=" * 78)
  print(
    "Phase 143-75R Toda58EquationStatement "
    "semantic structure audit"
  )
  print("=" * 78)
  print("scanned groups:", scanned_groups)
  print(
    "scanned presentation nodes:",
    presentation_nodes,
  )
  print("target occurrences:", occurrences)
  print(
    "groups containing target:",
    len(groups),
  )
  print("build errors:", len(build_errors))
  print(
    "semantic failures:",
    len(semantic_failures),
  )

  print()
  print("Statement field signatures")
  print("-" * 78)
  for signature, count in (
    statement_field_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Component types and renderability")
  print("-" * 78)
  for field_name in (
    "delta_nu_relation",
    "whitehead_nu_relation",
    "delta_whitehead_relation",
  ):
    print(field_name)
    print(
      "  types: "
      + repr(
        dict(
          component_type_counts[
            field_name
          ]
        )
      )
    )
    print(
      "  renderers: "
      + repr(
        dict(
          component_render_counts[
            field_name
          ]
        )
      )
    )
    for source, latex in (
      component_render_samples[
        field_name
      ].items()
    ):
      print(
        "  sample "
        + source
        + ": "
        + latex
      )

  print()
  print("Literature metadata signatures")
  print("-" * 78)
  for signature, count in (
    literature_type_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Inference rules")
  print("-" * 78)
  for name, count in rule_counts.most_common():
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Rule -> aggregate semantic shape")
  print("-" * 78)
  for rule_name in sorted(
    rule_to_statement_shape
  ):
    shapes = rule_to_statement_shape[
      rule_name
    ]
    print(rule_name)
    print(
      "  distinct semantic shapes:",
      len(shapes),
    )
    for shape, count in shapes.most_common():
      print(
        "  "
        + str(count)
        + " x "
        + repr(shape)
      )

  print()
  print("Representative aggregate statements")
  print("-" * 78)
  for rule_name in sorted(
    representative_statements
  ):
    print(rule_name)
    print(
      "  "
      + representative_statements[
        rule_name
      ]
    )

  if semantic_failures:
    print()
    print("Semantic failures")
    print("-" * 78)
    for failure in semantic_failures:
      print(
        "  - "
        + repr(failure)
      )

  if build_errors:
    print()
    print("Build errors")
    print("-" * 78)
    for error in build_errors:
      print(
        "  - "
        + repr(error)
      )

  print()
  print("=" * 78)

  expected_fields = (
    "delta_nu_relation",
    "whitehead_nu_relation",
    "delta_whitehead_relation",
    "literature_statements",
  )

  component_names = (
    "delta_nu_relation",
    "whitehead_nu_relation",
    "delta_whitehead_relation",
  )

  all_components_present = all(
    sum(
      component_type_counts[
        name
      ].values()
    )
    == EXPECTED_OCCURRENCES
    for name in component_names
  )

  if (
    occurrences == EXPECTED_OCCURRENCES
    and len(groups) == EXPECTED_GROUPS
    and not build_errors
    and not semantic_failures
    and statement_field_signatures
    == Counter(
      {
        expected_fields:
          EXPECTED_OCCURRENCES,
      }
    )
    and all_components_present
    and len(rule_counts) == 1
    and all(
      len(
        component_type_counts[
          name
        ]
      ) == 1
      for name in component_names
    )
  ):
    print(
      "PASS: all 45 aggregates have one "
      "uniform semantic component structure. "
      "Use the renderability inventory above "
      "to design Phase 143-75S."
    )
  else:
    print(
      "MEASURED RESULT: inspect the structure "
      "inventory before designing Phase 143-75S."
    )


if __name__ == "__main__":
  main()
