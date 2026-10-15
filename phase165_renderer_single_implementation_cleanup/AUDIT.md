# Phase 165 Renderer 実装一本化監査

- 現行 GitHub の `toda_group_proof_narrative_renderer.py` は完成証明の正規 Renderer である。
- 同ファイルは `toda_group_proof_generic_narrative_renderer.py` の `_render_generic_narrative_step` その他の共通関数・定数を import しており、後者の即時削除は ImportError を生じる。
- 旧 Generic Renderer には完成表示用 `render_toda_group_proof_generic_narrative_markdown` と部分証明用 `render_toda_partial_proof_narrative_markdown` の2関数が存在する。前者は現行の公開完成表示では使用しない。
- 本修正は両関数を除いた実体を `toda_group_proof_narrative_shared_components.py` に移し、部分証明関数を正規 Renderer に設置する。残存 import には互換パッケージの遅延委譲を用いる。
- `phase165_r52_partial_proof.py` の `render_partial_proof_markdown` 内 import を正規 Renderer へ変更する。
- 互換パッケージは Renderer を実装しない。完全な旧名前空間削除は追加の依存関係移行が必要であり、今回は API 保全のため先送りする。
- 完成証明 π₃² と未完成証明 π₄³ の Markdown 出力を変更前後で厳密に照合する。変更差があれば自動復元。
- 全体 pytest は Phase 165 末尾まで実施しない。

## 変更対象

1. `toda_group_proof_narrative_renderer.py`：既存 `render_toda_group_proof_narrative_markdown` は変更せず、部分証明関数を末尾に追加。
2. `phase165_r52_partial_proof.py`：`render_partial_proof_markdown` 関数内 import を共通 Renderer へ変更。
3. `toda_group_proof_narrative_shared_components.py`：共通低水準関数・定数を移動して新設。
4. `toda_group_proof_generic_narrative_renderer.py`：削除。互換 import は新規 `toda_group_proof_generic_narrative_renderer/__init__.py` で保持。
5. 新規 `install.py`、`restore.py`、`snapshot.py`、`run.ps1`、`test_cleanup.py`。

次 Phase 境界：残る互換 namespace の完全廃止（全 import 利用箇所の更新）および R27 の π₄³ 専用 Adapter 監査は本修正の対象外。
