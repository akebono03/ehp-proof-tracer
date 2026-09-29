from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  Toda56Nu4Prop44SpecializationStatement,
)


def _field_signature(value):
  if not is_dataclass(value):
    return ()

  return tuple(
    field.name
    for field in fields(value)
  )


def _safe_expression_latex(value):
  try:
    return render_toda_expression_latex(
      value
    )
  except Exception:
    return (
      "<unrendered:"
      + type(value).__name__
      + ">"
    )


def _safe_scalar_latex(value):
  try:
    return _render_scalar_latex(
      value
    )
  except Exception:
    return (
      "<unrendered:"
      + type(value).__name__
      + ">"
    )


def main():
  scanned_groups = 0
  scanned_nodes = 0
  target_occurrences = 0
  target_fallbacks = 0
  semantic_renderings = 0
  errors = []

  statement_signatures = Counter()
  field_types = defaultdict(Counter)
  rule_counts = Counter()
  rule_groups = defaultdict(set)
  n_values = Counter()
  alpha_values = Counter()
  membership_types = Counter()
  membership_element_values = Counter()
  membership_group_types = Counter()
  membership_group_values = Counter()
  hopf_relation_types = Counter()
  hopf_lhs_values = Counter()
  hopf_rhs_values = Counter()
  hopf_relation_kind_values = Counter()
  lemma54_types = Counter()
  lemma54_signatures = Counter()
  statement_renderer_results = Counter()
  sample_by_rule = {}

  target_fields = (
    "lemma54_statement",
    "n",
    "alpha",
    "membership",
    "hopf_relation",
  )

  for n in range(2, 16):
    for k in range(0, 8):
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
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=7,
          )
        )
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
      except Exception as exc:
        errors.append(
          (
            n,
            k,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      scanned_groups += 1
      scanned_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        step = node.proof_step
        statement = step.conclusion

        if not isinstance(
          statement,
          Toda56Nu4Prop44SpecializationStatement,
        ):
          continue

        target_occurrences += 1

        statement_signatures[
          _field_signature(
            statement
          )
        ] += 1

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else "<no inference rule>"
        )
        rule_counts[
          rule_name
        ] += 1
        rule_groups[
          rule_name
        ].add(
          (
            n,
            k,
          )
        )

        for field_name in target_fields:
          value = getattr(
            statement,
            field_name,
          )
          field_types[
            field_name
          ][
            type(value).__name__
          ] += 1

        n_values[
          _safe_scalar_latex(
            statement.n
          )
        ] += 1
        alpha_values[
          _safe_expression_latex(
            statement.alpha
          )
        ] += 1

        membership = (
          statement.membership
        )
        membership_types[
          type(membership).__name__
        ] += 1

        if hasattr(
          membership,
          "element",
        ):
          membership_element_values[
            _safe_expression_latex(
              membership.element
            )
          ] += 1

        if hasattr(
          membership,
          "group",
        ):
          group = membership.group
          membership_group_types[
            type(group).__name__
          ] += 1
          group_dimension = getattr(
            group,
            "group_dimension",
            None,
          )
          sphere_dimension = getattr(
            group,
            "sphere_dimension",
            None,
          )
          membership_group_values[
            (
              _safe_scalar_latex(
                group_dimension
              ),
              _safe_scalar_latex(
                sphere_dimension
              ),
            )
          ] += 1

        hopf_relation = (
          statement.hopf_relation
        )
        hopf_relation_types[
          type(hopf_relation).__name__
        ] += 1

        if hasattr(
          hopf_relation,
          "lhs",
        ):
          hopf_lhs_values[
            _safe_expression_latex(
              hopf_relation.lhs
            )
          ] += 1

        if hasattr(
          hopf_relation,
          "rhs",
        ):
          hopf_rhs_values[
            _safe_expression_latex(
              hopf_relation.rhs
            )
          ] += 1

        if hasattr(
          hopf_relation,
          "relation_type",
        ):
          hopf_relation_kind_values[
            str(
              hopf_relation.relation_type
            )
          ] += 1

        lemma54 = (
          statement.lemma54_statement
        )
        lemma54_types[
          type(lemma54).__name__
        ] += 1
        lemma54_signatures[
          _field_signature(
            lemma54
          )
        ] += 1

        try:
          semantic = (
            render_toda_proof_statement_latex(
              statement
            )
          )
          statement_renderer_results[
            (
              "<None>"
              if semantic is None
              else semantic
            )
          ] += 1
          if semantic is not None:
            semantic_renderings += 1

          fact = (
            _render_group_proof_narrative_fact(
              step
            )
          )
          if (
            step.inference_rule is not None
            and fact
            == step.inference_rule.name
          ):
            target_fallbacks += 1
        except Exception as exc:
          errors.append(
            (
              n,
              k,
              type(exc).__name__,
              str(exc),
            )
          )

        if rule_name not in sample_by_rule:
          sample_by_rule[
            rule_name
          ] = statement

  print("=" * 78)
  print(
    "Phase 143-75Z "
    "Toda56Nu4Prop44SpecializationStatement "
    "semantic structure audit"
  )
  print("=" * 78)
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "scanned presentation nodes:",
    scanned_nodes,
  )
  print(
    "target occurrences:",
    target_occurrences,
  )
  print(
    "target rule-name fallbacks:",
    target_fallbacks,
  )
  print(
    "existing statement semantic renderings:",
    semantic_renderings,
  )
  print(
    "errors:",
    len(errors),
  )

  print()
  print("Statement field signatures")
  print("-" * 78)
  for signature, count in (
    statement_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Field type inventory")
  print("-" * 78)
  for field_name in target_fields:
    print(
      field_name
      + ": "
      + repr(
        dict(
          field_types[
            field_name
          ]
        )
      )
    )

  print()
  print("First-class specialization values")
  print("-" * 78)
  print(
    "n:",
    dict(n_values),
  )
  print(
    "alpha:",
    dict(alpha_values),
  )
  print(
    "membership types:",
    dict(membership_types),
  )
  print(
    "membership elements:",
    dict(
      membership_element_values
    ),
  )
  print(
    "membership group types:",
    dict(
      membership_group_types
    ),
  )
  print(
    "membership group dimensions:",
    dict(
      membership_group_values
    ),
  )
  print(
    "hopf relation types:",
    dict(
      hopf_relation_types
    ),
  )
  print(
    "hopf lhs:",
    dict(hopf_lhs_values),
  )
  print(
    "hopf rhs:",
    dict(hopf_rhs_values),
  )
  print(
    "hopf relation kinds:",
    dict(
      hopf_relation_kind_values
    ),
  )

  print()
  print("Embedded Lemma 5.4 structure")
  print("-" * 78)
  print(
    "types:",
    dict(lemma54_types),
  )
  for signature, count in (
    lemma54_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Per-rule occurrence structure")
  print("-" * 78)
  for rule_name, count in (
    rule_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + rule_name
    )
    print(
      "  groups: "
      + str(
        len(
          rule_groups[
            rule_name
          ]
        )
      )
    )
    sample = sample_by_rule[
      rule_name
    ]
    print(
      "  n: "
      + _safe_scalar_latex(
        sample.n
      )
    )
    print(
      "  alpha: "
      + _safe_expression_latex(
        sample.alpha
      )
    )
    print(
      "  membership type: "
      + type(
        sample.membership
      ).__name__
    )
    print(
      "  hopf relation type: "
      + type(
        sample.hopf_relation
      ).__name__
    )
    print(
      "  lemma54 type: "
      + type(
        sample.lemma54_statement
      ).__name__
    )

  print()
  print("Current statement-renderer results")
  print("-" * 78)
  for value, count in (
    statement_renderer_results.most_common()
  ):
    print(
      str(count)
      + " x "
      + value
    )

  print()
  print("=" * 78)

  expected_signature = (
    "lemma54_statement",
    "n",
    "alpha",
    "membership",
    "hopf_relation",
  )

  if (
    scanned_groups == 112
    and target_occurrences == 26
    and target_fallbacks == 26
    and semantic_renderings == 0
    and statement_signatures[
      expected_signature
    ] == 26
    and len(
      statement_signatures
    ) == 1
    and len(
      rule_counts
    ) == 1
    and not errors
  ):
    print(
      "PASS: all 26 target statements "
      "share one five-field Prop. 4.4 "
      "specialization structure."
    )
  else:
    print(
      "MEASURED RESULT: inspect the "
      "specialization structure before "
      "implementation."
    )


if __name__ == "__main__":
  main()
