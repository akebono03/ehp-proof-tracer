from phase165_r52_partial_proof import (
    ProofSearchStatus,
    render_partial_proof_markdown,
)
from phase165_r52_r5_auto_search import (
    search_group_structure_automatically,
)

import argparse

from collections.abc import Sequence

import sys




from repository_operation_query_facade import (

  query_standard_repository_operation_input,

)

from repository_operation_query_presentation import (

  build_repository_operation_query_presentation,

)

from repository_operation_query_renderer import (

  render_repository_operation_query_markdown,

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




from toda_calculation_result import (

  TodaCalculationStatus,

)

from toda_group_query import TodaGroupQuery

from toda_group_query_semantics import (

  TodaGroupQueryDomainKind,

  classify_toda_group_query_domain,

  render_toda_group_query_domain_cli_message,

)

from toda_group_result_proof_replay import (

  build_complete_toda_group_result_proof_replay,

  build_toda_group_result_proof_replay,

)

from toda_group_proof_narrative_renderer import (

  render_toda_group_proof_narrative_markdown,

)

from toda_group_proof_outline_renderer import (

  render_toda_group_proof_outline_markdown,

)

from toda_group_proof_presentation import (

  build_toda_group_proof_presentation,

)

from toda_group_result_proof_replay_renderer import (

  render_toda_group_result_proof_replay_markdown,

)





def _configure_cli_utf8_streams(

) -> None:

  for stream in (

    sys.stdout,

    sys.stderr,

  ):

    reconfigure = getattr(

      stream,

      "reconfigure",

      None,

    )



    if reconfigure is None:

      continue



    reconfigure(

      encoding="utf-8",

    )





def _parse_positive_int(

  value: str,

) -> int:

  parsed = int(

    value

  )



  if parsed <= 0:

    raise argparse.ArgumentTypeError(

      "must be positive"

    )



  return parsed





def _parse_nonnegative_int(

  value: str,

) -> int:

  parsed = int(

    value

  )



  if parsed < 0:

    raise argparse.ArgumentTypeError(

      "must be nonnegative"

    )



  return parsed





def build_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py",

    description=(

      "Build a Toda homotopy-group proof report "

      "from the standard production repository."

    ),

    formatter_class=(

      argparse.RawDescriptionHelpFormatter

    ),

    epilog=(

      "Other commands:\n"

      "  explore             find repository occurrences "

      "of one generator\n"

      "  explore-proof       explore recursive proof ancestry "

      "for one generator\n"

      "  explore-applicable  find applicable theorem / lemma "

      "candidates\n"

      "  show-proof          replay the known-group proof "

      "for one generator\n"

      "  group-proof         replay the proof for one group "

      "query result\n"

      "  execute             execute one qualified theorem / "

      "lemma target\n"

      "  query               look up an existing operation "

      "fact\n"

      "  query-proof         replay one selected operation "

      "fact proof\n"

      "\n"

      "Use 'python main.py <command> --help' "

      "for command-specific help."

    ),

  )



  parser.add_argument(

    "n",

    type=_parse_positive_int,

    help=(

      "sphere dimension n for the project quantity "

      "pi_{n+k}^n"

    ),

  )



  parser.add_argument(

    "k",

    type=int,

    help=(

      "stem k for the project quantity pi_{n+k}^n "

      "(free part plus 2-primary component)"

    ),

  )



  return parser





def build_explore_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py explore",

    description=(

      "Explore occurrences of one generator "

      "in the standard production repository."

    ),

  )



  parser.add_argument(

    "generator",

    help=(

      "generator input such as "

      "nu_prime, nu_5, or eta_2"

    ),

  )



  return parser





def build_explore_proof_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py explore-proof",

    description=(

      "Explore one generator across the recursive "

      "proof ancestry of the standard production "

      "repository."

    ),

  )



  parser.add_argument(

    "generator",

    help=(

      "generator input such as "

      "nu_prime, nu_5, or eta_2"

    ),

  )



  return parser





def build_explore_applicable_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py explore-applicable",

    description=(

      "Find theorem / lemma applicability "

      "candidates for one generator across the "

      "recursive proof ancestry of the standard "

      "production repository."

    ),

  )



  parser.add_argument(

    "generator",

    help=(

      "generator input such as "

      "nu_prime, nu_5, or eta_2"

    ),

  )



  parser.add_argument(

    "--detailed",

    action="store_true",

    help=(

      "show full catalog-entry, premise-index, "

      "binding, and fixed-point provenance"

    ),

  )



  return parser





def build_show_proof_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py show-proof",

    description=(

      "Show the known-group proof provenance "

      "for one generator in the standard "

      "production repository."

    ),

  )



  parser.add_argument(

    "generator",

    help=(

      "generator input such as "

      "nu_prime, sigma_11, or nu_5"

    ),

  )



  parser.add_argument(

    "--depth",

    type=_parse_nonnegative_int,

    help=(

      "maximum proof replay depth; "

      "omit to use the default depth 1"

    ),

  )



  return parser





def build_group_proof_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py group-proof",

    description=(

      "Show trace, outline, or deterministic narrative "

      "for one repository-backed Toda group result."

    ),

  )



  parser.add_argument(

    "n",

    type=_parse_positive_int,

    help=(

      "sphere dimension n for the project quantity "

      "pi_{n+k}^n"

    ),

  )



  parser.add_argument(

    "k",

    type=int,

    help=(

      "stem k for the project quantity pi_{n+k}^n "

      "(free part plus 2-primary component)"

    ),

  )



  parser.add_argument(

    "--depth",

    type=_parse_nonnegative_int,

    default=2,

    help=(

      "maximum proof replay depth; "

      "default: 2"

    ),

  )



  parser.add_argument(

    "--mode",

    choices=(

      "trace",

      "outline",

      "narrative",

    ),

    default="narrative",

    help=(

      "proof presentation mode; "

      "default: narrative"

    ),

  )



  return parser





def build_execute_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py execute",

    description=(

      "Execute one qualified theorem / lemma target "

      "for a generator in the standard production "

      "repository."

    ),

  )



  parser.add_argument(

    "generator",

    help=(

      "generator input such as "

      "nu_prime, nu_5, or eta_2"

    ),

  )



  parser.add_argument(

    "--candidate",

    type=_parse_positive_int,

    help=(

      "1-based executable candidate number; "

      "omit to list candidates when ambiguous"

    ),

  )



  return parser





def build_query_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py query",

    description=(

      "Look up an existing mathematical operation "

      "fact in the standard production repository."

    ),

  )



  parser.add_argument(

    "query",

    help=(

      "operation query such as H(nu_prime), "

      "Delta(iota_9), E(eta_2 o nu_prime), "

      "eta_2 o nu_prime, or "

      "eta_2 o nu_prime o eta_6"

    ),

  )



  return parser





def build_query_proof_argument_parser(

) -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(

    prog="main.py query-proof",

    description=(

      "Replay the proof of one known operation-query "

      "fact from its primary repository provenance."

    ),

  )



  parser.add_argument(

    "query",

    help=(

      "operation query such as H(nu_prime), "

      "Delta(iota_9), E(eta_2 o nu_prime), "

      "eta_2 o nu_prime, or "

      "eta_2 o nu_prime o eta_6"

    ),

  )



  parser.add_argument(

    "--fact",

    type=_parse_positive_int,

    help=(

      "1-based fact number; required when the "

      "query has multiple known facts"

    ),

  )



  parser.add_argument(

    "--depth",

    type=_parse_nonnegative_int,

    help=(

      "maximum proof replay depth; "

      "omit to use the default depth 1"

    ),

  )



  return parser





def _run_explore_command(generator_input: str) -> int:
  from phase165_r27_r34_typed_lookup import (
    TypedLookupStatus,
    search_typed_generator_statements,
  )
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_explore_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1





def _run_explore_proof_command(generator_input: str) -> int:
  from phase165_r27_r34_typed_lookup import TypedLookupStatus, search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_explore_proof_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1




def _run_explore_applicable_command(

  generator_input: str,

  detailed: bool = False,

) -> int:

  print(
    "This legacy generator command is disabled; "
    "use the unified proof search when available."
  )
  return 1




def _run_show_proof_command(generator_input: str, max_depth: int | None = None) -> int:
  from phase165_r27_r34_typed_lookup import TypedLookupStatus, search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  if max_depth is not None and (isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0):
    raise ValueError("max_depth must be nonnegative")
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_show_proof_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1




def _run_group_query_command(
  n: int,
  k: int,
) -> int:
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    print(render_toda_group_query_domain_cli_message(domain))
    return 0

  result = search_group_structure_automatically(n=n, k=k)
  print(render_partial_proof_markdown(result), end="")
  return 0 if result.status is ProofSearchStatus.COMPLETE else 1


def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = 2,
  mode: str = "narrative",
) -> int:
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")
  if max_depth is not None and (
    isinstance(max_depth, bool)
    or not isinstance(max_depth, int)
    or max_depth < 0
  ):
    raise ValueError("max_depth must be nonnegative")

  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    print(render_toda_group_query_domain_cli_message(domain))
    return 1

  result = search_group_structure_automatically(n=n, k=k)
  print(render_partial_proof_markdown(result), end="")
  return 0 if result.status is ProofSearchStatus.COMPLETE else 1









def _run_execute_command(

  generator_input: str,

  candidate_number: int | None = None,

) -> int:

  print(
    "This legacy generator command is disabled; "
    "use the unified proof search when available."
  )
  return 1




def _run_query_command(

  query_input: str,

) -> int:

  try:

    result = (

      query_standard_repository_operation_input(

        query_input

      )

    )

  except (

    TypeError,

    ValueError,

  ) as error:

    parser = (

      build_query_argument_parser()

    )

    parser.error(

      str(

        error

      )

    )



  if not result.found:

    print(

      "No known repository fact found for "

      f"{query_input}."

    )

    return 1



  presentation = (

    build_repository_operation_query_presentation(

      result

    )

  )



  if not presentation.items:

    print(

      "No directly renderable repository fact found for "

      f"{query_input}."

    )

    return 1



  markdown = (

    render_repository_operation_query_markdown(

      presentation

    )

  )



  print(

    markdown,

    end="",

  )



  return 0





def _run_query_proof_command(

  query_input: str,

  fact_number: int | None = None,

  max_depth: int | None = None,

) -> int:

  try:

    result = (

      query_standard_repository_operation_input(

        query_input

      )

    )

  except (

    TypeError,

    ValueError,

  ) as error:

    parser = (

      build_query_proof_argument_parser()

    )

    parser.error(

      str(

        error

      )

    )



  if not result.found:

    print(

      "No known repository fact found for "

      f"{query_input}."

    )

    return 1



  query_presentation = (

    build_repository_operation_query_presentation(

      result

    )

  )



  if not query_presentation.items:

    print(

      "No directly renderable repository fact found for "

      f"{query_input}."

    )

    return 1



  if (

    fact_number is None

    and len(

      query_presentation.items

    ) > 1

  ):

    print(

      render_repository_operation_query_markdown(

        query_presentation

      ),

      end="",

    )

    print(

      "\nSpecify --fact N to replay one fact."

    )

    return 1



  try:

    if max_depth is None:

      replay = (

        build_repository_operation_query_proof_replay(

          query_presentation,

          fact_number=fact_number,

        )

      )

    else:

      replay = (

        build_repository_operation_query_proof_replay(

          query_presentation,

          fact_number=fact_number,

          max_depth=max_depth,

        )

      )

  except (

    TypeError,

    ValueError,

  ) as error:

    parser = (

      build_query_proof_argument_parser()

    )

    parser.error(

      str(

        error

      )

    )



  replay_presentation = (

    build_repository_operation_query_proof_replay_presentation(

      replay

    )

  )



  markdown = (

    render_repository_operation_query_proof_replay_markdown(

      replay_presentation

    )

  )



  print(

    markdown,

    end="",

  )



  return 0





def main(

  argv: Sequence[str] | None = None,

) -> int:

  raw_argv = (

    list(

      argv

    )

    if argv is not None

    else sys.argv[

      1:

    ]

  )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "explore"

  ):

    parser = (

      build_explore_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_explore_command(

      args.generator

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "explore-proof"

  ):

    parser = (

      build_explore_proof_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_explore_proof_command(

      args.generator

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "explore-applicable"

  ):

    parser = (

      build_explore_applicable_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_explore_applicable_command(

      args.generator,

      detailed=args.detailed,

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "show-proof"

  ):

    parser = (

      build_show_proof_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_show_proof_command(

      args.generator,

      max_depth=args.depth,

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "group-proof"

  ):

    parser = (

      build_group_proof_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_group_proof_command(

      args.n,

      args.k,

      max_depth=args.depth,

      mode=args.mode,

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "execute"

  ):

    parser = (

      build_execute_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_execute_command(

      args.generator,

      candidate_number=args.candidate,

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "query"

  ):

    parser = (

      build_query_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_query_command(

      args.query

    )



  if (

    raw_argv

    and raw_argv[

      0

    ] == "query-proof"

  ):

    parser = (

      build_query_proof_argument_parser()

    )



    args = parser.parse_args(

      raw_argv[

        1:

      ]

    )



    return _run_query_proof_command(

      args.query,

      fact_number=args.fact,

      max_depth=args.depth,

    )



  parser = build_argument_parser()
  args = parser.parse_args(raw_argv)
  return _run_group_query_command(
      args.n,
      args.k,
  )









if __name__ == "__main__":

  _configure_cli_utf8_streams()



  raise SystemExit(

    main()

  )

