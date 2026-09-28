from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
import main as cli_main
from repository_generator_known_group_proof_replay import (
  build_standard_repository_generator_known_group_proof_replay_input,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
  TodaSuspensionInjectiveStatement,
)


def _nu_prime_replay_statements():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "nu_prime"
    )
  )

  return tuple(
    replay_step.proof_step.conclusion
    for replay_step in result.steps
  )


def _single_statement(
  statements,
  statement_type,
):
  matches = tuple(
    statement
    for statement in statements
    if isinstance(
      statement,
      statement_type,
    )
  )

  assert len(
    matches
  ) == 1

  return matches[
    0
  ]


def test_phase109_31_renders_nu_prime_membership_as_latex():
  statement = _single_statement(
    _nu_prime_replay_statements(),
    HomotopyGroupMembershipStatement,
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == r"\nu' \in \pi_{6}^{3}"
  )


def test_phase109_31_renders_suspension_injective_as_latex():
  statement = _single_statement(
    _nu_prime_replay_statements(),
    TodaSuspensionInjectiveStatement,
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"E: \pi_{5}^{2} \to \pi_{6}^{3}"
      r" \text{ is injective}"
    )
  )


def test_phase109_31_renders_hopf_surjective_as_latex():
  statement = _single_statement(
    _nu_prime_replay_statements(),
    TodaHopfInvariantSurjectiveStatement,
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"H: \pi_{6}^{3} \to \pi_{6}^{5}"
      r" \text{ is surjective}"
    )
  )


def test_phase109_31_show_proof_nu_prime_has_no_audited_raw_repr(
  capsys,
):
  exit_code = cli_main.main(
    [
      "show-proof",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    r"$\nu' \in \pi_{6}^{3}$"
    in captured.out
  )

  assert (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3} \text{ is injective}$"
    in captured.out
  )

  assert (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5} \text{ is surjective}$"
    in captured.out
  )

  assert (
    "HomotopyGroupMembershipStatement("
    not in captured.out
  )

  assert (
    "TodaSuspensionInjectiveStatement("
    not in captured.out
  )

  assert (
    "TodaHopfInvariantSurjectiveStatement("
    not in captured.out
  )


def test_phase109_31_show_proof_sigma11_regression_remains_clean(
  capsys,
):
  exit_code = cli_main.main(
    [
      "show-proof",
      "sigma_11",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    r"$\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}$"
    in captured.out
  )

  assert (
    r"$\pi_{n + 7}^{n} = \mathbb{Z}/16\{\sigma_{n}\}$"
    in captured.out
  )
