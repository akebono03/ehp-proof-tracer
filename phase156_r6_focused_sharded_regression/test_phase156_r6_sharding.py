from phase156_r6_focused_sharded_regression.phase156_r6_sharded_reference_regression import (
  SHARD_COUNT,
  _all_groups,
  groups_for_shard,
)


def test_phase156_r6_four_shards_partition_112_groups_exactly():
  shards = tuple(
    groups_for_shard(
      shard_index
    )
    for shard_index in range(
      SHARD_COUNT
    )
  )
  flattened = tuple(
    group
    for shard in shards
    for group in shard
  )

  assert len(
    shards
  ) == 4
  assert all(
    len(
      shard
    )
    == 28
    for shard in shards
  )
  assert len(
    flattened
  ) == 112
  assert len(
    set(
      flattened
    )
  ) == 112
  assert set(
    flattened
  ) == set(
    _all_groups()
  )


def test_phase156_r6_each_shard_spans_all_n_values():
  for shard_index in range(
    SHARD_COUNT
  ):
    shard = groups_for_shard(
      shard_index
    )

    assert {
      n
      for n, _k in shard
    } == set(
      range(
        2,
        16,
      )
    )


def test_phase156_r6_each_shard_has_two_k_values_per_n():
  for shard_index in range(
    SHARD_COUNT
  ):
    shard = groups_for_shard(
      shard_index
    )

    for n in range(
      2,
      16,
    ):
      assert len(
        tuple(
          k
          for group_n, k in shard
          if group_n == n
        )
      ) == 2
