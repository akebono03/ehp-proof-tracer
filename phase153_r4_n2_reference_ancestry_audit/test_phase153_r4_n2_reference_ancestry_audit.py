from audit_phase153_r4_n2_reference_ancestry import (
  TARGETS,
  audit_group,
  render_summary_markdown,
)


def test_phase153_r4_audits_exactly_six_n2_groups():
  assert TARGETS == (
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
  )


def test_phase153_r4_each_target_builds_reference_ancestry_audit():
  audits = tuple(
    audit_group(
      n=n,
      k=k,
    )
    for n, k in TARGETS
  )

  assert len(
    audits
  ) == 6

  for audit, target in zip(
    audits,
    TARGETS,
  ):
    assert (
      audit.n,
      audit.k,
    ) == target
    assert audit.presentation.root_step is not None
    assert isinstance(
      audit.references,
      tuple,
    )


def test_phase153_r4_summary_contains_all_six_target_groups():
  audits = tuple(
    audit_group(
      n=n,
      k=k,
    )
    for n, k in TARGETS
  )

  rendered = render_summary_markdown(
    audits
  )

  for group_dimension in range(
    4,
    10,
  ):
    assert (
      f"$\\pi_{{{group_dimension}}}^{{2}}$"
      in rendered
    )

  assert "root-selected" in rendered
  assert "distance→root" in rendered
