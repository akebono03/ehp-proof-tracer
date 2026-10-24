# Phase 168 R3-40E — 旧延期描画ループの撤去

## 現状と変更対象

R3-40D の実行結果により、R3-40C の共通 Topological Sort が保持され、限定 pytest 15件 PASS、4群の論理依存逆転0件、既存3群の固定基準説明項目12/12となった。R3-40C の Projection は `NarrativeOrderEntry(step_index)` のみ返し、`after_indices` は常に空となっている。

今回変更するリポジトリファイルは **`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` だけ**。旧 `entry.after_indices` を繰り返して延期文章を描画する死んだ経路を削除する。変更関数全文は `full_functions/render_model_backed_narrative_markdown_FULL.py`、実行後のファイル全文は `full_files/phase168_r3_5_model_renderer.py` に保存する。import は変更しない。

`NarrativeOrderEntry.after_indices` は既存 API 互換性のため残す。Proof Search、Proof Tree、引用・命題台帳、文献順、特殊化、他の関数やクラスは変更しない。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_40e_remove_deferred_render.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_40e_remove_deferred_render\run.ps1"
```

## 追加テスト・完了条件

`tests/test_phase168_r3_40e_remove_deferred_render.py` の全文と import を同梱。

- 旧レンダリング・ループだけの削除と適用の冪等性。
- 4群の Projection が延期エントリーなしに各 ProofStep をちょうど1回返すこと。
- 変更前後の4群の Narrative を **バイト単位で一致**させる。
- 既存の限定 pytest、4群の依存逆転0件、固定基準説明項目12/12。
- 失敗時は Renderer をバックアップからロールバック。

全体 pytest は Phase 168 の最後にだけ実行する。次の工程での API 廃止やさらに広範な Renderer 整理は先取りしない。
