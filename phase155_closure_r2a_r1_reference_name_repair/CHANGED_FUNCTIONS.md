# Phase 155 Closure-R2A-R1 changed functions

Import changes: none.

Production changes: none.

## `tests/test_phase132_8_group_proof_narrative_dedup.py`

### `test_phase132_8_cli_narrative_uses_deduplicated_renderer`

```python
def test_phase132_8_cli_narrative_uses_deduplicated_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "[R1]" in captured.out
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out
```

## `tests/test_phase133_10_sigma_label_wording.py`

### `test_phase133_10_sigma9_depth_two_uses_final_japanese_wording`

```python
def test_phase133_10_sigma9_depth_two_uses_final_japanese_wording(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "[R1]" in captured.out
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out

  assert (
    "Theorem 3.6 から Lemma 5.14 への σ″ bridge"
    not in captured.out
  )
  assert (
    "Toda Lemma 5.14 の σ′ branch"
    not in captured.out
  )
```

## `tests/test_phase133_6_group_proof_narrative_labels.py`

### `test_phase133_6_sigma9_depth_two_reuses_new_labels`

```python
def test_phase133_6_sigma9_depth_two_reuses_new_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "[R1]" in captured.out
  assert r"\pi_{12}^{5}" in captured.out
  assert r"\mathbb{Z}/2" in captured.out
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out
```

## `tests/test_phase133_9_group_proof_narrative_labels.py`

### `test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels`

```python
def test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "[R1]" in captured.out
  assert r"\pi_{16}^{9}" in captured.out
  assert r"\mathbb{Z}/16" in captured.out

  internal_names = (
    "Toda Theorem 3.6 Lemma 5.14 sigma double-prime bridge",
    "Toda Lemma 5.14 sigma-prime branch",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out
```

### `test_phase133_9_previous_labels_remain_available`

```python
def test_phase133_9_previous_labels_remain_available(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "[R1]" in captured.out
  assert r"\pi_{12}^{5}" in captured.out
  assert r"\mathbb{Z}/2" in captured.out
```
