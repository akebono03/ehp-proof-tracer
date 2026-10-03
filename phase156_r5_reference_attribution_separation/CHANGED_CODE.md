# Phase156-R5 repair — changed code

## 変更対象

- `toda_rules.py`
  - `toda_53_nu_prime_bracket_specialization_inference_rule()`
- `tests/test_phase156_r5_reference_attribution_separation.py`
  - 新規追加

## `toda_rules.py`

既存関数全体は実行時に `changed_function_after.txt` へ出力する。
今回の production change は同関数内の `LiteratureReference` の attribution のみ。

変更前:

```python
literature_reference=LiteratureReference(
  label="Toda (5.3) / Lemma 5.2",
  author="H. Toda",
  title="Composition Methods in Homotopy Groups of Spheres",
  year=1962,
  locator="(5.3) / Lemma 5.2",
),
```

変更後:

```python
literature_reference=LiteratureReference(
  label="Toda (5.3)",
  author="H. Toda",
  title="Composition Methods in Homotopy Groups of Spheres",
  year=1962,
  locator="(5.3)",
),
```

import の変更はない。

## 新規テスト

`tests/test_phase156_r5_reference_attribution_separation.py` は
パッケージ内の同名ファイル全文をそのまま追加する。
