# Phase 169 R2A — 実装と監査の境界

## 変更対象（最初に確認）

- 本体変更ファイル：`phase168_r3_37c_reference_projection.py` のみ。
- 変更関数：`project_reference_bodies(registry, assertion_ids)` のみ。
- import：トップレベルの変更なし。関数内で `Toda52UniversalStatement` の import を追加。関数内の import 部分は `full_functions/project_reference_bodies.py` に全文を掲載。
- 新規限定テスト：`tests/test_phase169_r2a_toda52_reference_body.py`（本 ZIP 内のテストであり、リポジトリ既存テストを変更しない）。新規テスト関数は同ファイルに全文収録。
- 新規監査補助：`audit.py`、`apply.py`、`run.ps1`。

`full_files/phase168_r3_37c_reference_projection.py` は修正後の本体ファイル全文。変更前の全文は `baseline/` に収録。

## 根拠

R1 の実測により、$\pi_4^2$ は3 ProofStep（GIVEN 2件、INFERENCE 1件）で完成し、(5.2) は `Toda52UniversalStatement` の型付き GIVEN として導出木に存在する。`build_proof_narrative_model()` は登録された `assertion_id` に関連する本文を `project_reference_bodies()` で生成するが、その関数は (5.2) の型を文章化していない。

このため、原典の内容を追加で探索せず、**型の各フィールドが採用済みの値に一致する場合に限って**次を表示する。

$$
\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2 \qquad (i\ge3).
$$

## テストと完了条件

- 実際の $\pi_4^2$ 完全探索を再実行し、登録済み (5.2) の `assertion_ids` と GIVEN の一致を監査。
- 追加された本文が Reference と Web 向け Markdown に反映されること。
- 未登録の異なる命題、未使用命題を引用本文へ混入しないこと。
- `phase168_r3_39a_reference_accuracy`、`test_phase168_r3_4_link_bridge`、`phase168_r3_41l_reasoned_prose` の限定 pytest を実行。
- 既存の $\pi_4^2$ の証明ステップ数が3であること。
- 全体 pytest は Phase 169 の終了時まで保留。

## 後続 Phase との境界

$\pi_5^3$ の探索 `search_failed`（未解決 Goal 3件）は未修正。EHP の同型性、生成元の輸送、既証明の再利用はこの R2A で実装しない。Renderer の証明文章（(5.2) の $i=4$ への特殊化説明）も変更しない。
