# Phase 168 R3-41P2 — 実行パス・古いテスト期待値の限定修正

2026年10月24日

## ユーザー環境の証拠

`review_bundle(20261024-084647).zip` の監査情報で確認：

- Git `develop`, HEAD `02c2a6a1e13eb69f297dc50a363db958aa18f72c`
- 静的監査7箇所は正常に出力された。
- `phase165_r57_r20_general_specialization.py` は `source_trace` で検出され SHA-256 も記録されている。
- Python `audit.py` の直接起動によりプロジェクトルートが `sys.path` に入らず、同モジュールの import が失敗した。
- 限定 pytest は 26 passed, 1 failed。失敗は R3-29 の `"零写像である"` という旧固定表現の検査で、R3-41O 後は `\operatorname{Im}\Delta=\ker E=0` の等式が表示される。
- R3-41N1 の既存テストはこの等式と中間ステップの接続を既に検査しており、直近の限定テストでも PASS。

## 変更ファイル・関数

1. `phase168_r3_41p_boundary_audit/run.ps1` — スクリプト全文を更新。既存 `Invoke-LoggedPython()` は維持し、監査を `python -B -m phase168_r3_41p_boundary_audit.audit` で起動。新規テスト更新の事前実行を追加。実行結果のログ・ZIP を引き続き保存。
2. 新規 `phase168_r3_41p_boundary_audit/apply_test_fix.py` — `apply_legacy_test_fix()` / `main()` の全文を追加。テスト1関数内の旧表記を厳密一致で更新し、元ファイルのバイト列をバックアップ。その他は変更しない。
3. 新規 `phase168_r3_41p_boundary_audit/restore_test.py` — `restore_legacy_test()` / `main()` の全文を追加。ハッシュが一致する場合のみ復元する。
4. 既存 `phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py` — `test_pi32_all_steps_preserved_without_suppression()` 全文を置換。**import は変更しない**。関数以外の変更はない。
5. 新規 `phase168_r3_41p_boundary_audit/tests/test_launcher_and_stale_test_patch.py` — テストと import 全文を追加。
6. `phase168_r3_41p_boundary_audit/README.md` — 実行・復元手順を更新（全文収録）。

## 既存テスト関数の置き換え後全文

```python
def test_pi32_all_steps_preserved_without_suppression():
    result, model = _case(2, 1)
    entries = project_narrative_order(model)
    indices = [i for item in entries for i in (item.step_index, *item.after_indices)]
    assert sorted(indices) == list(range(len(model.steps)))
    rendered = render_model_backed_narrative_markdown(result, model)
    assert r"\operatorname{Im}\Delta=\ker E=0" in rendered
    assert rendered.count("次の完全列を考える") == 1
```

このテストは元の「ProofStep の表示順投影は全ノードを保持する」という検査を維持し、古い文章の完全一致部分だけを数学的に同値な現在の等式へ変更する。`Proof Tree` と公開 Narrative の内容は変更しない。

## 動作・復元

- 監査結果は `output/audit.md`, `audit.json`, `pi*_current.md`, `pi*_proof.diff`, `pi*_reference.diff` に保存。
- テストバックアップは `output/backups/r3_29_test_original.bin`、ハッシュ状態は `output/backups/r3_29_test_state.json`。
- 復元はプロジェクトルートで `python -B -m phase168_r3_41p_boundary_audit.restore_test`。
- ZIP は全ファイル全文を格納。実コードへ無関係な import や新しい Adapter は追加しない。

## 限定 pytest

```powershell
python -B -m pytest -q -p no:cacheprovider `
  .\phase168_r3_41p_boundary_audit\tests\test_launcher_and_stale_test_patch.py `
  .\phase168_r3_41p_boundary_audit\tests\test_audit_error_reporting.py `
  .\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py `
  .\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py `
  .\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py `
  .\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py `
  .\phase168_r3_8_citation_origin\tests\test_phase168_r3_8_citation_origin.py
```

## 完了条件

- 監査側の import エラー解消。
- 動的監査で3群の全文、Citation provenance、数学的判定関数の呼び出しを収集。
- 限定 pytest を通過（ユーザー Windows 上で再検証）。
- プロジェクト実装のコードと Proof Tree は無変更。
- 全体 pytest は Phase 168 終了時のみ実行。

## 次 Phase との境界

この修正は監査ランナーと旧テスト期待値だけ。Renderer の証明再検証除去は R3-41P の監査結果を受け、別工程で行う。
