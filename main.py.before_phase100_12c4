import argparse
from collections.abc import Sequence

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


def build_argument_parser(
) -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description=(
      "Build a Toda homotopy-group proof report "
      "from the standard production repository."
    ),
  )

  parser.add_argument(
    "n",
    type=int,
    help="sphere dimension n",
  )

  parser.add_argument(
    "k",
    type=int,
    help="stem k for pi_{n+k}(S^n)",
  )

  return parser


def main(
  argv: Sequence[str] | None = None,
) -> int:
  parser = build_argument_parser()

  args = parser.parse_args(
    argv
  )

  result = (
    build_standard_toda_report(
      n=args.n,
      k=args.k,
    )
  )

  if (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    print(
      "No proof report found for "
      f"pi_{{{args.n + args.k}}}^{{{args.n}}}."
    )
    return 1

  print(
    "\n\n---\n\n".join(
      result.reports
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
