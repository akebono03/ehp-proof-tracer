from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
MAIN_PATH = ROOT / "main.py"
BACKUP_PATH = ROOT / "main.py.phase132_7_backup"


def replace_exact(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  if not MAIN_PATH.exists():
    raise RuntimeError(
      "main.py was not found in the repository root"
    )

  original = MAIN_PATH.read_text(
    encoding="utf-8",
  )

  if not BACKUP_PATH.exists():
    shutil.copy2(
      MAIN_PATH,
      BACKUP_PATH,
    )

  updated = original

  old_imports = '''from toda_group_result_proof_replay_renderer import (
  render_toda_group_result_proof_replay_markdown,
)
'''

  new_imports = '''from toda_group_proof_narrative_renderer import (
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
'''

  updated = replace_exact(
    updated,
    old_imports,
    new_imports,
    "group-proof imports",
  )

  old_parser = '''def build_group_proof_argument_parser(
) -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="main.py group-proof",
    description=(
      "Replay the proof provenance for one "
      "repository-backed Toda group result."
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
    help=(
      "maximum proof replay depth; "
      "omit to use the default depth 1"
    ),
  )

  return parser
'''

  new_parser = '''def build_group_proof_argument_parser(
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
    help=(
      "maximum proof replay depth; "
      "omit to use the default depth 1"
    ),
  )

  parser.add_argument(
    "--mode",
    choices=(
      "trace",
      "outline",
      "narrative",
    ),
    default="trace",
    help=(
      "proof presentation mode; "
      "default: trace"
    ),
  )

  return parser
'''

  updated = replace_exact(
    updated,
    old_parser,
    new_parser,
    "build_group_proof_argument_parser",
  )

  old_runner = '''def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = None,
) -> int:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = (
    classify_toda_group_query_domain(
      query
    )
  )

  if (
    domain.kind
    is not (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  ):
    print(
      "No repository-backed group proof is available for "
      f"pi_{{{n + k}}}^{{{n}}}."
    )
    return 1

  report = (
    build_standard_toda_report(
      n=n,
      k=k,
    )
  )

  if (
    report.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    print(
      "No proof-backed group result found for "
      f"pi_{{{n + k}}}^{{{n}}}."
    )
    return 1

  if (
    report.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  ):
    print(
      "Multiple proof-backed group results found for "
      f"pi_{{{n + k}}}^{{{n}}}; "
      "group-proof requires exactly one result."
    )
    return 1

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  if max_depth is None:
    replay = (
      build_toda_group_result_proof_replay(
        group_result
      )
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )

  markdown = (
    render_toda_group_result_proof_replay_markdown(
      replay
    )
  )

  print(
    markdown,
    end="",
  )

  return 0
'''

  new_runner = '''def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = None,
  mode: str = "trace",
) -> int:
  if mode not in (
    "trace",
    "outline",
    "narrative",
  ):
    raise ValueError(
      "mode must be trace, outline, or narrative"
    )

  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = (
    classify_toda_group_query_domain(
      query
    )
  )

  if (
    domain.kind
    is not (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  ):
    print(
      "No repository-backed group proof is available for "
      f"pi_{{{n + k}}}^{{{n}}}."
    )
    return 1

  report = (
    build_standard_toda_report(
      n=n,
      k=k,
    )
  )

  if (
    report.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    print(
      "No proof-backed group result found for "
      f"pi_{{{n + k}}}^{{{n}}}."
    )
    return 1

  if (
    report.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  ):
    print(
      "Multiple proof-backed group results found for "
      f"pi_{{{n + k}}}^{{{n}}}; "
      "group-proof requires exactly one result."
    )
    return 1

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  if max_depth is None:
    replay = (
      build_toda_group_result_proof_replay(
        group_result
      )
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )

  if mode == "trace":
    markdown = (
      render_toda_group_result_proof_replay_markdown(
        replay
      )
    )
  else:
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

  print(
    markdown,
    end="",
  )

  return 0
'''

  updated = replace_exact(
    updated,
    old_runner,
    new_runner,
    "_run_group_proof_command",
  )

  old_dispatch = '''    return _run_group_proof_command(
      args.n,
      args.k,
      max_depth=args.depth,
    )
'''

  new_dispatch = '''    return _run_group_proof_command(
      args.n,
      args.k,
      max_depth=args.depth,
      mode=args.mode,
    )
'''

  updated = replace_exact(
    updated,
    old_dispatch,
    new_dispatch,
    "group-proof dispatch",
  )

  MAIN_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Phase 132-7 applied successfully."
  )
  print(
    f"Backup: {BACKUP_PATH.name}"
  )


if __name__ == "__main__":
  main()
