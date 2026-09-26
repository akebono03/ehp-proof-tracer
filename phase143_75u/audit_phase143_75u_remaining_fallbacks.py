from collections import Counter, defaultdict

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


def main():
  scanned_groups = 0
  scanned_nodes = 0
  fallback_count = 0
  statement_counts = Counter()
  rule_counts = Counter()
  statement_rules = defaultdict(Counter)
  statement_groups = defaultdict(set)
  errors = []

  for n in range(2, 16):
    for k in range(0, 8):
      try:
        report = build_standard_toda_report(n=n, k=k)
        group_result = report.candidates[0].source_candidate.group_result
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(replay)
      except Exception as exc:
        errors.append((n, k, type(exc).__name__, str(exc)))
        continue

      scanned_groups += 1
      scanned_nodes += len(presentation.nodes)

      for node in presentation.nodes:
        step = node.proof_step
        if step.inference_rule is None:
          continue

        try:
          fact = _render_group_proof_narrative_fact(step)
        except Exception as exc:
          errors.append((n, k, type(exc).__name__, str(exc)))
          continue

        rule_name = step.inference_rule.name
        if fact != rule_name:
          continue

        fallback_count += 1
        statement_name = type(step.conclusion).__name__
        statement_counts[statement_name] += 1
        rule_counts[rule_name] += 1
        statement_rules[statement_name][rule_name] += 1
        statement_groups[statement_name].add((n, k))

  print("=" * 78)
  print("Phase 143-75U remaining rule-name fallback audit")
  print("=" * 78)
  print("scanned groups:", scanned_groups)
  print("scanned presentation nodes:", scanned_nodes)
  print("rule-name fallback occurrences:", fallback_count)
  print("statement types:", len(statement_counts))
  print("distinct fallback rule names:", len(rule_counts))
  print("render errors:", len(errors))

  print()
  print("Remaining statement inventory")
  print("-" * 78)

  for index, (statement_name, count) in enumerate(
    statement_counts.most_common(),
    start=1,
  ):
    groups = sorted(statement_groups[statement_name])
    print(
      str(index)
      + ". "
      + statement_name
      + ": "
      + str(count)
      + " occurrences, "
      + str(len(groups))
      + " groups"
    )
    for rule_name, rule_count in statement_rules[statement_name].most_common():
      print("   " + str(rule_count) + " x " + rule_name)
    print(
      "   groups: "
      + ", ".join(
        "pi_(" + str(n + k) + ")^" + str(n)
        for n, k in groups
      )
    )

  print()
  print("Fallback rule-name inventory")
  print("-" * 78)
  for index, (rule_name, count) in enumerate(
    rule_counts.most_common(),
    start=1,
  ):
    print(str(index) + ". " + str(count) + " x " + rule_name)

  print()
  print("=" * 78)

  if (
    scanned_groups == 112
    and scanned_nodes == 11033
    and fallback_count == 365
    and len(statement_counts) == 31
    and not errors
  ):
    print(
      "PASS: Phase 143-75T baseline is confirmed: "
      "365 fallbacks remain across 31 statement types."
    )
  else:
    print(
      "MEASURED RESULT: baseline differs from the Phase 143-75T "
      "expectation; inspect before implementing the next renderer."
    )


if __name__ == "__main__":
  main()
