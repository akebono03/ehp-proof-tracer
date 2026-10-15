# Phase 165 R5-R7 公開到達経路監査

状態: **REVIEW_REQUIRED**

## 静的検査

- PASS: `no_syntax_errors`
- PASS: `web_group_proof_reaches_canonical_module`
- PASS: `no_public_import_path_to_legacy_targets`
- PASS: `no_public_import_path_to_phase162_web`

## 公開入口から正規 Renderer への import 経路

- `web_group_proof.py`: `web_group_proof.py` → `phase165_r52_r3_web_adapter.py` → `phase165_r52_partial_proof.py` → `toda_group_proof_narrative_renderer.py`
- `phase165_r52_r3_web_adapter.py`: `phase165_r52_r3_web_adapter.py` → `phase165_r52_partial_proof.py` → `toda_group_proof_narrative_renderer.py`
- `phase165_r52_partial_proof.py`: `phase165_r52_partial_proof.py` → `toda_group_proof_narrative_renderer.py`

## 公開入口から旧 Phase 162 Web への import 経路

- `web_group_proof.py`: 検出なし
- `phase165_r52_r3_web_adapter.py`: 検出なし
- `phase165_r52_partial_proof.py`: 検出なし

## `phase162_r3_narrative_connection.py`
対象関数: `render_phase162_r3_narrative`

### 直接呼び出し

- `phase162_web_narrative_integration.py:297` → `render_phase162_r3_narrative`

### 公開入口からの import 経路

- `web_group_proof.py`: 検出なし
- `phase165_r52_r3_web_adapter.py`: 検出なし
- `phase165_r52_partial_proof.py`: 検出なし

旧 Phase 162 Web から: `phase162_web_narrative_integration.py` → `phase162_r3_narrative_connection.py`

## `toda_group_proof_narrative_proof_chain_renderer.py`
対象関数: `render_toda_group_proof_narrative_from_proof_chains_markdown`

### 直接呼び出し

- 検出なし

### 公開入口からの import 経路

- `web_group_proof.py`: 検出なし
- `phase165_r52_r3_web_adapter.py`: 検出なし
- `phase165_r52_partial_proof.py`: 検出なし

旧 Phase 162 Web から: 検出なし

## `toda_group_proof_narrative_concrete_transport.py`
対象関数: `render_concrete_transport_proof_from_steps`

### 直接呼び出し

- 検出なし

### 公開入口からの import 経路

- `web_group_proof.py`: 検出なし
- `phase165_r52_r3_web_adapter.py`: 検出なし
- `phase165_r52_partial_proof.py`: 検出なし

旧 Phase 162 Web から: 検出なし

## 限界

- This is a conservative module-import graph, not a function-level runtime call graph.
- An import path is possible reachability, not evidence that a function executes.
- Absence of a path does not rule out dynamic imports, monkeypatches, route registration, or reflection.
- Static roots are restricted to the named Group Proof modules; CLI and other surfaces require separate review.
- No source code is modified. Historical Phase162 fixture failures remain unresolved.
