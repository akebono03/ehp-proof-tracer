from phase155_shard_planner import (
  _contiguous_partition,
  _file_nodeid,
)


def test_file_nodeid_extracts_test_file():
  assert (
    _file_nodeid(
      "tests/test_a.py::test_one"
    )
    == "tests/test_a.py"
  )


def test_contiguous_partition_preserves_file_order():
  files = [
    "tests/test_1.py",
    "tests/test_2.py",
    "tests/test_3.py",
    "tests/test_4.py",
    "tests/test_5.py",
    "tests/test_6.py",
  ]
  weights = {
    file_nodeid: 1.0
    for file_nodeid in files
  }

  shards = _contiguous_partition(
    files,
    weights,
    3,
  )

  flattened = [
    file_nodeid
    for shard in shards
    for file_nodeid in shard
  ]

  assert flattened == files


def test_contiguous_partition_covers_each_file_once():
  files = [
    "tests/test_1.py",
    "tests/test_2.py",
    "tests/test_3.py",
    "tests/test_4.py",
  ]
  weights = {
    "tests/test_1.py": 1.0,
    "tests/test_2.py": 8.0,
    "tests/test_3.py": 1.0,
    "tests/test_4.py": 1.0,
  }

  shards = _contiguous_partition(
    files,
    weights,
    2,
  )

  flattened = [
    file_nodeid
    for shard in shards
    for file_nodeid in shard
  ]

  assert flattened == files
  assert len(
    set(
      flattened
    )
  ) == len(
    files
  )


def test_partition_never_emits_empty_middle_shard():
  files = [
    "a",
    "b",
    "c",
    "d",
  ]
  weights = {
    key: 1.0
    for key in files
  }

  shards = _contiguous_partition(
    files,
    weights,
    4,
  )

  assert all(
    shard
    for shard in shards
  )


def test_replaced_extreme_names_do_not_affect_partition_api():
  files = [
    "tests/test_phase95_top_level_calculation_orchestration.py",
    "tests/test_phase97_single_found_calculation_to_report_api.py",
  ]
  weights = {
    files[
      0
    ]: 1.0,
    files[
      1
    ]: 1.0,
  }

  assert (
    _contiguous_partition(
      files,
      weights,
      2,
    )
    == [
      [
        files[
          0
        ]
      ],
      [
        files[
          1
        ]
      ],
    ]
  )
