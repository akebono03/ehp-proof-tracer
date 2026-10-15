# Phase 165-R57-R6 安定輸送分岐の削除前監査

## 変更対象

- 新規 `phase165_r57_r6_stable_transport_gate/audit.py`：`audit_stable_transport_boundary()`、`main()`。
- 新規 `phase165_r57_r6_stable_transport_gate/test_phase165_r57_r6_stable_transport_gate.py`：対象テスト4件。
- 新規 `run.ps1`、`README.md`、`AUDIT.md`。
- 既存ファイル・クラス・関数・import は変更しない。

## 確認した既存コード

GitHub `akebono03/ehp-proof-tracer` の `toda_stable_group_transport.py` は Toda (4.5) の有限巡回群・零群輸送の推論規則を持つ。`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` の規則一覧にはこれらの関数が直接登場しない。`toda_stable_transport.py` の `build_canonical_toda_45_isomorphism_step()` は旧 GIVEN ファクトリーを利用するため、共有探索へそのまま流用することは認めない。

`phase165_r55_nk_only_goal.py` での群構造候補選択と、`toda_group_proof_narrative_renderer.py` の安定輸送専用表示分岐も調査する。

## 判定

- 本監査は数学的証明ではない。
- `pi_5^4` の探索成功を主張しない。
- 現行の安定輸送の専用表示分岐はこの R57-R6 で削除しない。
- Source Fact・推論規則・生成元の輸送が新方式で導出された後に、実出力の比較を行って削除する。

## テスト

`python -m pytest -q phase165_r57_r6_stable_transport_gate/test_phase165_r57_r6_stable_transport_gate.py`

全体 pytest は Phase 165 の最後のみ。
