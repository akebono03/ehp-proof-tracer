from pathlib import Path
import importlib.util


AUDIT_PATH = Path(
  "phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit"
) / "audit_phase148_rc2_4_repair_r4_1.py"


def _load_audit_module():
  spec = (
    importlib.util.spec_from_file_location(
      "phase148_r4_1_audit",
      AUDIT_PATH,
    )
  )
  assert spec is not None
  assert spec.loader is not None

  module = (
    importlib.util.module_from_spec(
      spec
    )
  )
  spec.loader.exec_module(
    module
  )
  return module


def test_phase148_rc2_4_repair_r4_1_r1_argument_locations_use_current_argument_api():
  module = (
    _load_audit_module()
  )
  group_result = (
    module._group_result()
  )
  contexts = (
    module._contexts(
      group_result
    )
  )
  complete = contexts[
    "complete"
  ]
  matches = (
    module._matching_steps(
      complete[
        "closure"
      ],
      module.EQUATIONS[
        0
      ][
        1
      ],
    )
  )

  assert len(
    matches
  ) == 1

  proof_step = matches[
    0
  ][
    0
  ].proof_step

  locations = (
    module._argument_locations(
      complete[
        "closure"
      ],
      complete[
        "sidecar"
      ],
      complete[
        "arguments"
      ],
      complete[
        "blocks"
      ],
      proof_step,
    )
  )

  assert isinstance(
    locations,
    tuple,
  )

  for (
    argument_index,
    role,
    location,
  ) in locations:
    assert isinstance(
      argument_index,
      int,
    )
    assert isinstance(
      role,
      str,
    )
    assert set(
      location
    ) == {
      "supporting",
      "conclusion",
      "local_body",
    }
