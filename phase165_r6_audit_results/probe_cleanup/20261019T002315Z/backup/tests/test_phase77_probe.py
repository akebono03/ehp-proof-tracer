from proof import ProofRule
from probes.probe_phase77_capabilities import (
  build_phase77_representative_result,
  main,
)
from toda_rules import TodaLemma516BracketSumContainmentStatement


def test_phase77_probe_final_statement_is_derived():
  result = build_phase77_representative_result()

  assert isinstance(
    result["final_statement"],
    TodaLemma516BracketSumContainmentStatement,
  )

  assert result["final_step"].rule == ProofRule.INFERENCE
  assert result["final_derived"] is True
  assert result["final_is_given"] is False


def test_phase77_probe_typed_setup_remains_given():
  result = build_phase77_representative_result()

  assert result["typed_setup_is_given"] is True


def test_phase77_probe_phase75_provenance_is_reachable():
  result = build_phase77_representative_result()

  assert result["phase75_theorem36_bridge_reachable"] is True
  assert result["phase75_sigma8_reachable"] is True


def test_phase77_probe_both_theorem36_branches_are_reachable():
  result = build_phase77_representative_result()

  assert result["first_branch_reachable"] is True
  assert result["second_branch_reachable"] is True
  assert result["theorem36_sum_reachable"] is True


def test_phase77_probe_sigma_transport_branch_is_reachable():
  result = build_phase77_representative_result()

  assert result["sigma_bridge_reachable"] is True
  assert result["sigma_definition_reachable"] is True
  assert result["scaled_composition_reachable"] is True


def test_phase77_probe_reuses_same_odd_parameter():
  result = build_phase77_representative_result()

  assert result["same_odd_parameter"] is True


def test_phase77_probe_first_bracket_uses_e7_beta():
  result = build_phase77_representative_result()

  assert result["first_bracket_uses_e7_beta"] is True


def test_phase77_probe_has_no_phase76_specific_dependency():
  result = build_phase77_representative_result()

  assert result["phase76_specific_rule_reachable"] is False


def test_phase77_probe_graph_is_non_circular():
  result = build_phase77_representative_result()

  assert result["final_is_self_ancestor"] is False
  assert result["final_conclusion_in_ancestors"] is False
  assert result["proof_graph_acyclic"] is True


def test_phase77_probe_output_contains_final_result(capsys):
  main()

  output = capsys.readouterr().out

  assert "Toda Lemma 5.16 result" in output
  assert "E^4 beta composed with sigma_(t+8)" in output
  assert "E^7 beta" in output
  assert "2 nu_(t+11)" in output


def test_phase77_probe_output_contains_provenance(capsys):
  main()

  output = capsys.readouterr().out

  assert "Provenance / integration" in output
  assert "Phase 75 Theorem 3.6 bridge reachable = True" in output
  assert "Phase 75 sigma_8 statement reachable = True" in output
  assert "same odd x preserved = True" in output
  assert "final Lemma 5.16 is GIVEN = False" in output


def test_phase77_probe_output_contains_non_circularity(capsys):
  main()

  output = capsys.readouterr().out

  assert "Applicability / non-circularity" in output
  assert "Phase 76 Toda (5.16) rule reachable = False" in output
  assert "final is self-ancestor = False" in output
  assert "final conclusion appears in ancestors = False" in output
  assert "proof graph acyclic = True" in output


def test_phase77_probe_output_documents_source_index_correction(capsys):
  main()

  output = capsys.readouterr().out

  assert "printed lemma contains E^n beta" in output
  assert "proof text" in output
  assert "typing also forces exponent 7" in output
  assert "machine representation therefore uses E^7 beta" in output


def test_phase77_probe_output_contains_completion_boundary(capsys):
  main()

  output = capsys.readouterr().out

  assert "Phase 77 representative probe boundary" in output
  assert "new mathematical inference rules" in output
  assert "generic Toda-bracket sum algebra" in output
  assert "automatic proof narrative generation" in output
  assert "persistent Proof Repository" in output


def test_phase77_probe_output_identifies_next_boundary(capsys):
  main()

  output = capsys.readouterr().out

  assert "Next mathematical boundary" in output
  assert "(G_7;2)=Z/16{sigma}" in output
