# Phase 169 R4E — 引用本文対応の修正

## 変更対象

- `phase168_r3_37c_reference_projection.py` の `project_reference_bodies` 関数全体
  - 関数内 import の変更後全文を含む完全な関数は実行後の `output/project_reference_bodies_FULL.py` に生成する。
  - Proposition 4.4 の型付き命題を登録済みの条件付き主張として Reference に表示する。
- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown` 関数全体
  - 関数内 import の変更後全文を含む完全な関数は実行後の `output/render_model_backed_narrative_markdown_FULL.py` に生成する。
  - `MapInjective`（単射性）の証明木の実際の `TodaProp44UniversalStatement` 祖先の引用番号を付ける。
  - 単独で表示された EHP 完全列に、実際の `TodaProp42GeneralExactnessStatement` 祖先の引用番号を付ける。
- 新規 `phase169_r4e_citation_binding/patch.py`, `audit.py`, `run.ps1` とテストファイル。

## 安全条件

検証対象の Git blob SHA は下記の2つのみ。HEAD が別のコミットでも2ファイルの内容が不変なら実行可能。対象ファイルに別の修正があれば適用を拒否する。

- Reference projection: `ee39f50c00117ac120ab74e391491d79fbd65c25`
- Model Renderer: `324900b180b60e14ce7d310912e4833b1ff89c31`

数学的証明規則、引用台帳、Proof Tree、Proof Narrative Model、Web API は変更しない。pytest または監査が失敗した場合、両方の元ファイルをバイト単位で復元する。

## 予定する限定 pytest

`python -m pytest -q phase169_r4e_citation_binding/tests/test_r4e_patch_safety.py phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py`

全体 pytest は Phase 169 の最後まで実施しない。

## 完了条件

- π₆⁴ の18ステップ・完全証明・未解決0件を維持。
- Reference 5件に対する本文タグが5件すべて存在する。
- Proposition 4.4 に出典どおりの仮定を含む命題内容が表示される。
- Proposition 4.4 に基づく「単射」と Proposition 4.2 (4.4) に基づく「完全列」にそれぞれ祖先に由来するタグが付く。
- 既存の π₅³ 28ステップ・Reference 6件を壊さない。
- 全体 pytest の実行なし。

次工程では本文の長さ・文章表現を別途監査する。文面の固定文章化や π₇⁵ の探索は本工程には含めない。
