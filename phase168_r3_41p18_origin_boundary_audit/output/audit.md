# Phase 168 R3-41P18 — Origin Observation 信頼境界監査

監査のみ。アプリ本体、既存テスト、固定基準は変更しない。

## 正規の3群

| 群 | INFERENCE | GIVEN | Handoff と公開 Web の全文 | Citation |
|---|---:|---:|---|---|
| pi3_2 | 13 | 5 | True | True |
| pi4_3 | 19 | 6 | True | True |
| pi5_4 | 7 | 3 | True | True |

## Python API の境界と留保

- `forged_step_unseen_before_notes`: `True`
- `forged_step_rejected_before_notes`: `True`
- `self_attested_forged_inference_accepted`: `True`
- `inconsistent_result_target_accepted`: `True`
- `replacement_bridge_wrapper_accepted`: `True`
- `observation_aggregates_multiple_searches`: `True`
- `cross_search_bridge_rejected`: `True`
- `nested_cannot_reuse_outer_observation`: `True`
- `nested_does_not_inherit_outer_steps`: `True`
- `outer_observation_restored`: `True`
- `manual_observation_rejected`: `True`

## 判断

- Factory の生成記録と探索側 proved 通知の同一性は、通常経路の観測根拠として有効。
- ただし note_factory_inference / note_accepted_search_step は外部 Python から呼べるため、由来記録を認証として使えない。
- ContextVar の scope は search invocation と一対一とは限らず、複数探索の記録を混在できる。
- Handoff は Result の target・citing assertion と探索 context の一意な紐付けまで保証していない。
- 異なる Bridge のラッパーが同一リンクを持つ場合、元の Bridge オブジェクトの同一性を検証しない。
- これは in-process Python API の制約であり、外部 Web 攻撃の成立を意味しない。
- R3-41P17 の origin handoff を標準 Web に昇格させたり、R3-41P13 matcher replay を除去したりしない。
- partial と既存 API を維持し、Renderer の数学的ガード2件を残す。
- 次の工程では真正な探索呼出に由来する情報を信頼境界内で束ねる最小設計を行う。

**AUDIT_STATUS**: `ORIGIN_BOUNDARY_GAPS_CONFIRMED`

**FULL_PYTEST_NOT_RUN**
