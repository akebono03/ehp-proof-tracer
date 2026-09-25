from toda_group_proof_narrative_arguments import (
  _argument_dependency_closure_indices,
)


def test_phase143_7_fix1_dependency_cycle_excludes_conclusion():
  direct_dependencies = (
    (1,),
    (0,),
  )

  closure = (
    _argument_dependency_closure_indices(
      direct_dependencies,
      0,
    )
  )

  assert closure == (
    1,
  )
