import argparse
from contextlib import (
  redirect_stderr,
  redirect_stdout,
)
import sys
from typing import (
  Sequence,
  TextIO,
)

from generator_input import (
  resolve_generator_input,
)
from proof_repository import ProofRepository
from repository_element_facade import (
  explore_repository_generator,
)
from toda_calculation_facade import (
  build_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


def build_cli_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="ehp-proof-tracer",
  )

  subparsers = parser.add_subparsers(
    dest="command",
    required=True,
  )

  group_parser = subparsers.add_parser(
    "group",
    help=(
      "build a theorem-backed report "
      "for pi_(n+k)^n"
    ),
  )
  group_parser.add_argument(
    "n",
    type=int,
  )
  group_parser.add_argument(
    "k",
    type=int,
  )

  element_parser = subparsers.add_parser(
    "element",
    help=(
      "explore repository occurrences "
      "of one generator"
    ),
  )
  element_parser.add_argument(
    "generator",
  )

  return parser


def _write_markdown(
  stream: TextIO,
  markdown: str,
) -> None:
  stream.write(
    markdown
  )

  if not markdown.endswith(
    "\n"
  ):
    stream.write(
      "\n"
    )


def _run_group_command(
  repository: ProofRepository,
  n: int,
  k: int,
  stdout: TextIO,
  stderr: TextIO,
) -> int:
  try:
    result = build_toda_report(
      repository,
      n=n,
      k=k,
    )
  except (
    TypeError,
    ValueError,
  ) as error:
    print(
      f"error: {error}",
      file=stderr,
    )
    return 2

  if (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    print(
      (
        "No theorem-backed result found for "
        f"pi_{n + k}^{n}."
      ),
      file=stdout,
    )
    return 0

  reports = (
    result.reports
  )

  for index, report in enumerate(
    reports
  ):
    if index:
      stdout.write(
        "\n---\n\n"
      )

    _write_markdown(
      stdout,
      report,
    )

  return 0


def _run_element_command(
  repository: ProofRepository,
  generator_input: str,
  stdout: TextIO,
  stderr: TextIO,
) -> int:
  try:
    generator = (
      resolve_generator_input(
        generator_input
      )
    )
  except (
    TypeError,
    ValueError,
  ) as error:
    print(
      f"error: {error}",
      file=stderr,
    )
    return 2

  report = (
    explore_repository_generator(
      repository,
      generator,
    )
  )

  _write_markdown(
    stdout,
    report.markdown,
  )

  return 0


def run_cli(
  repository: ProofRepository,
  argv: Sequence[str] | None = None,
  *,
  stdout: TextIO | None = None,
  stderr: TextIO | None = None,
) -> int:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if stdout is None:
    stdout = sys.stdout

  if stderr is None:
    stderr = sys.stderr

  parser = build_cli_parser()

  try:
    with (
      redirect_stdout(
        stdout
      ),
      redirect_stderr(
        stderr
      ),
    ):
      arguments = parser.parse_args(
        argv
      )
  except SystemExit as error:
    return int(
      error.code
    )

  if arguments.command == "group":
    return _run_group_command(
      repository,
      arguments.n,
      arguments.k,
      stdout,
      stderr,
    )

  if arguments.command == "element":
    return _run_element_command(
      repository,
      arguments.generator,
      stdout,
      stderr,
    )

  raise RuntimeError(
    "unsupported parsed command"
  )
