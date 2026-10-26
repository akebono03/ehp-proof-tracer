# Phase 169 R3G2 — 引用対象選択の監査修正

## 事前確認

2026-10-26 の GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `a95940646b5554181a5ef3f70f4a8b2123badaa2` を調査した。
関連実装 `phase165_r55_nk_only_goal.py` は `registered_group_goal_candidates()` で DB 由来の Goal を選んだ後、`resolve_specialized_goal_citing_id(bridge, candidate)` で文献命題を決定する。`phase166_r3t_goal_source_binding/goal_source.py` は生成元表記の正規化を含む比較を行う。
既存 EHP 機能の `phase165_r14_r5_ehp_connection.py`、`phase165_r52_r9_shared_math.py` と関連テストを確認した。

## 原因

R3G1 の `audit()` は `_references_for_exact_content(bridge, target)` の件数が1でなければ失敗したが、DB 由来の `target` と文献命題は生成元表記が異なり得る。この件数は実際の探索が採用する citing ID の根拠ではない。

## 変更一覧（今回の Phase で必要な最小限）

- 既存本番コード、既存 API、既存 pytest、プロジェクト5文書：変更なし。
- `phase169_r3g2_actual_citing_resolution/audit.py`：`resolve_specialized_goal_citing_id` を import して `audit()` 内の citing ID 決定を置換。`audit()` はファイル全文を同梱。台帳 Relation の完全一致件数を診断として JSON と標準出力へ追加。文献名は Proposition 5.3 と照合。
- `phase169_r3g2_actual_citing_resolution/tests/test_phase169_r3g_hopf_source_and_composite_audit.py`：既存3件を保持し、実際の Goal 選択を使う監査テスト1件を末尾に追加。必要な import と4件のテスト関数全文を収録。
- `phase169_r3g2_actual_citing_resolution/run.ps1`：R3G2 の名前、監査モジュール実行先を更新。監査・テストの意味を変更しない。

## 検証

対象限定 pytest：新規4件、既存 EHP adapter 6件、EHP Backward Goal 4件。全体 pytest は実行しない。

```powershell
python -B -m pytest -q -p no:cacheprovider `
  ".\phase169_r3g2_actual_citing_resolution\tests\test_phase169_r3g_hopf_source_and_composite_audit.py" `
  ".\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py" `
  ".\tests\test_phase161_r3_backward_goal_schema.py"
```

実行後、`R3G2_FOCUSED_PYTEST_EXIT_CODE=0`、`R3G2_AUDIT_EXIT_CODE=0`、`R3G2_COMPLETE` と `output/source_and_composite.json` を確認する。

## 完了条件と次 Phase の境界

R3G2 は (5.3) の原文・台帳の型・文献順と、Proposition 5.1 の GIVEN と INFERENCE の違い、`H(ν′)=η₅` に到達する推論の実在を記録するだけである。Goal や Reference の存在だけで証明を認定しない。R3H の修正対象は R3G2 の実探索報告に基づいて決定する。
