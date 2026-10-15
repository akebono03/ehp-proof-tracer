# Phase 165 R5-R7 監査内容

## 対象

既存ファイル、関数、テストは変更しない。追加するファイルは `audit.py`, `test_audit.py`, `run.ps1`, `README.md`, `AUDIT.md`, `CHANGED_CODE.md`。

調査対象は旧・専用 Narrative 経路3件：

- `phase162_r3_narrative_connection.py` / `render_phase162_r3_narrative`
- `toda_group_proof_narrative_proof_chain_renderer.py` / `render_toda_group_proof_narrative_from_proof_chains_markdown`
- `toda_group_proof_narrative_concrete_transport.py` / `render_concrete_transport_proof_from_steps`

起点は `web_group_proof.py`, `phase165_r52_r3_web_adapter.py`, `phase165_r52_partial_proof.py`。旧 Phase162 Web 呼出経路 `phase162_web_narrative_integration.py` も個別に調べる。

## GitHub 事前確認

2026-10-15 に `akebono03/ehp-proof-tracer` の上記ファイルと関連表示コードを読み取り確認。

- `web_group_proof.py` は Phase165 の検索と共通 Web Adapter を利用する。
- `phase165_r52_r3_web_adapter.py` は `render_partial_proof_markdown` を使用する。
- `phase162_web_narrative_integration.py` は `render_phase162_r3_narrative` を呼び出す。
- `toda_group_proof_narrative_proof_chain_renderer.py` は別の Proof Chain 文章生成関数を公開している。
- `toda_group_proof_narrative_concrete_transport.py` は具体的な移送の表示関数を提供する。

GitHub の基準ブランチとユーザーの Windows ローカル環境は必ずしも一致しないため、**最終判断は Windows 側の出力**に基づく。

## 完了条件と境界

6件の監査単体テスト成功、走査の構文エラー0件、JSON・Markdown 報告生成が今回の実行完了条件。`REVIEW_REQUIRED` は想定どおりであり、一本化の数学的・実行時認定ではない。旧 Phase162 fixture 不整合は次作業に残す。全体 pytest は Phase165 最後のみ。
