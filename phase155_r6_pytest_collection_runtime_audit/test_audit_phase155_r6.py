from __future__ import annotations

import audit_phase155_r6 as audit


def test_source_file_strips_node_components():
  assert (
    audit._source_file(
      "tests/test_x.py::test_a"
    )
    == "tests/test_x.py"
  )


def test_source_function_nodeid_strips_parameter_case():
  assert (
    audit._source_function_nodeid(
      "tests/test_x.py::test_a[value]"
    )
    == "tests/test_x.py::test_a[value]"
  )


def test_group_by_file_preserves_nodeids():
  result = audit._group_by_file(
    [
      "tests/test_a.py::test_1",
      "tests/test_a.py::test_2",
      "tests/test_b.py::test_3",
    ]
  )

  assert result[
    "tests/test_a.py"
  ] == [
    "tests/test_a.py::test_1",
    "tests/test_a.py::test_2",
  ]


def test_batched_is_stable():
  assert (
    audit._batched(
      [
        "a",
        "b",
        "c",
        "d",
        "e",
      ],
      2,
    )
    == [
      [
        "a",
        "b",
      ],
      [
        "c",
        "d",
      ],
      [
        "e",
      ],
    ]
  )


def test_deterministic_samples_take_spread():
  samples = audit._deterministic_samples(
    [
      f"tests/test_x.py::test_{index}"
      for index in range(
        10
      )
    ],
    3,
  )

  assert len(samples) == 3
  assert samples[
    0
  ] == "tests/test_x.py::test_0"
  assert samples[
    -1
  ] == "tests/test_x.py::test_9"


def test_parse_collected_nodeids_ignores_summary():
  stdout = (
    "tests/test_x.py::test_a\n"
    "tests/test_x.py::test_b[param]\n"
    "\n"
    "2 tests collected in 0.10s\n"
  )

  assert (
    audit._parse_collected_nodeids(
      stdout
    )
    == [
      "tests/test_x.py::test_a",
      "tests/test_x.py::test_b[param]",
    ]
  )


def test_runtime_sample_sizes_keep_probe_bounded():
  assert sum(
    audit.RUNTIME_SAMPLE_SIZES.values()
  ) <= 12
