from pathlib import Path


MAIN_PATH = Path("main.py")


def _replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"expected exactly one {label} marker, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  if not MAIN_PATH.exists():
    raise RuntimeError(
      "main.py was not found; run this script from the repository root"
    )

  text = MAIN_PATH.read_text(
    encoding="utf-8",
  )

  if "def build_group_proof_argument_parser(" in text:
    raise RuntimeError(
      "Phase 131-4 appears to be already applied"
    )

  old_import = '''from toda_group_query_semantics import (\n  TodaGroupQueryDomainKind,\n  classify_toda_group_query_domain,\n  render_toda_group_query_domain_cli_message,\n)\n'''
  new_import = '''from toda_group_query_semantics import (\n  TodaGroupQueryDomainKind,\n  classify_toda_group_query_domain,\n  render_toda_group_query_domain_cli_message,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_group_result_proof_replay_renderer import (\n  render_toda_group_result_proof_replay_markdown,\n)\n'''
  text = _replace_once(
    text,
    old_import,
    new_import,
    "import",
  )

  old_help = '''      "  show-proof          replay the known-group proof "\n      "for one generator\\n"\n'''
  new_help = '''      "  show-proof          replay the known-group proof "\n      "for one generator\\n"\n      "  group-proof         replay the proof for one group "\n      "query result\\n"\n'''
  text = _replace_once(
    text,
    old_help,
    new_help,
    "help",
  )

  parser_marker = '''def build_execute_argument_parser(\n) -> argparse.ArgumentParser:\n'''
  parser_function = '''def build_group_proof_argument_parser(\n) -> argparse.ArgumentParser:\n  parser = argparse.ArgumentParser(\n    prog="main.py group-proof",\n    description=(\n      "Replay the proof provenance for one "\n      "repository-backed Toda group result."\n    ),\n  )\n\n  parser.add_argument(\n    "n",\n    type=_parse_positive_int,\n    help=(\n      "sphere dimension n for the project quantity "\n      "pi_{n+k}^n"\n    ),\n  )\n\n  parser.add_argument(\n    "k",\n    type=int,\n    help=(\n      "stem k for the project quantity pi_{n+k}^n "\n      "(free part plus 2-primary component)"\n    ),\n  )\n\n  parser.add_argument(\n    "--depth",\n    type=_parse_nonnegative_int,\n    help=(\n      "maximum proof replay depth; "\n      "omit to use the default depth 1"\n    ),\n  )\n\n  return parser\n\n\n'''
  text = _replace_once(
    text,
    parser_marker,
    parser_function + parser_marker,
    "parser insertion",
  )

  run_marker = '''def _run_execute_command(\n  generator_input: str,\n  candidate_number: int | None = None,\n) -> int:\n'''
  run_function = '''def _run_group_proof_command(\n  n: int,\n  k: int,\n  max_depth: int | None = None,\n) -> int:\n  query = TodaGroupQuery(\n    n=n,\n    k=k,\n  )\n\n  domain = (\n    classify_toda_group_query_domain(\n      query\n    )\n  )\n\n  if (\n    domain.kind\n    is not (\n      TodaGroupQueryDomainKind\n      .POSITIVE_DIMENSION\n    )\n  ):\n    print(\n      "No repository-backed group proof is available for "\n      f"pi_{{{n + k}}}^{{{n}}}."\n    )\n    return 1\n\n  report = (\n    build_standard_toda_report(\n      n=n,\n      k=k,\n    )\n  )\n\n  if (\n    report.status\n    is TodaCalculationStatus.NOT_FOUND\n  ):\n    print(\n      "No proof-backed group result found for "\n      f"pi_{{{n + k}}}^{{{n}}}."\n    )\n    return 1\n\n  if (\n    report.status\n    is TodaCalculationStatus.MULTIPLE_RESULTS\n  ):\n    print(\n      "Multiple proof-backed group results found for "\n      f"pi_{{{n + k}}}^{{{n}}}; "\n      "group-proof requires exactly one result."\n    )\n    return 1\n\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n\n  if max_depth is None:\n    replay = (\n      build_toda_group_result_proof_replay(\n        group_result\n      )\n    )\n  else:\n    replay = (\n      build_toda_group_result_proof_replay(\n        group_result,\n        max_depth=max_depth,\n      )\n    )\n\n  markdown = (\n    render_toda_group_result_proof_replay_markdown(\n      replay\n    )\n  )\n\n  print(\n    markdown,\n    end="",\n  )\n\n  return 0\n\n\n'''
  text = _replace_once(
    text,
    run_marker,
    run_function + run_marker,
    "run-function insertion",
  )

  main_marker = '''  if (\n    raw_argv\n    and raw_argv[\n      0\n    ] == "execute"\n  ):\n'''
  main_branch = '''  if (\n    raw_argv\n    and raw_argv[\n      0\n    ] == "group-proof"\n  ):\n    parser = (\n      build_group_proof_argument_parser()\n    )\n\n    args = parser.parse_args(\n      raw_argv[\n        1:\n      ]\n    )\n\n    return _run_group_proof_command(\n      args.n,\n      args.k,\n      max_depth=args.depth,\n    )\n\n'''
  text = _replace_once(
    text,
    main_marker,
    main_branch + main_marker,
    "main branch insertion",
  )

  MAIN_PATH.write_text(
    text,
    encoding="utf-8",
  )

  print("Phase 131-4 main.py patch applied.")


if __name__ == "__main__":
  main()
