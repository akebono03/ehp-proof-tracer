from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements,
)


def test_phase159_r1_7c_r4_late_shorter_prefix_is_suppressed():
  longer = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$."
  )
  shorter = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$."
  )
  markdown = (
    longer
    + "\n\n"
    + r"$\pi_{2}^{1}=0$."
    + "\n\n"
    + shorter
  )

  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      markdown
    )
  )

  assert longer in rendered
  assert shorter not in rendered


def test_phase159_r1_7c_r4_earlier_shorter_exactness_is_preserved():
  shorter = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  longer = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )
  markdown = (
    shorter
    + "\n\n"
    + longer
  )

  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      markdown
    )
  )

  assert shorter in rendered
  assert longer in rendered
