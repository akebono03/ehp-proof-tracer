# Phase 173 R4-R15R15R2 設計

## 原因と変更理由

従来の R15R15 Installer は `9729d3ee` を固定し、R15R14 の2ファイルが未コミットであることを前提としていた。R15R14 が `5563a670` で GitHub `develop` にコミットされた後、コードが正当な状態でも Source Guard が停止した。

## 変更対象

本番コード: `web_group_proof_common.py` の `WebGroupProofView` 全体、`phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view()` 全体、`templates/index.html` の群問い合わせ結果表示分岐。

新規追加: `phase173_r4_r15r15r2_head_guard_fix/`（`patches.py`、`install.py`、`run.ps1`、`tests/`、文書）。既存の import は不変更。既存テストの上書きもなし。

## 証明と表示の境界

検証済みの `PartialProofResult.abstract_structure` の有無だけを表示フラグに変換し、Web 上段の結果案内で参照する。証明探索、推論規則、ProofStep、引用文献、結論、未解決 Goal は変更しない。完成／抽象群のみ証明済み／証明書なしを1つの Web 表示経路で区別する。

## Source Guard

Reviewed baseline は `5563a67008d097d08745481ee299dbb94e12c2b9`。`develop` の HEAD はその子孫であり、ローカル HEAD と `origin/develop` が等しく、関連4ファイルの Git blob が監査値から変わらない場合のみ実行する。追跡ファイルの想定外の変更は拒否する。`DryRun` では既存コードを書き換えない。

## 限定テストと完了条件

`tests/test_contract.py`、`tests/test_integration.py` と R15R14/R15R13/R15R12/R15R11、Phase117 の関連テストに限定する。全体 pytest は Phase 173 の終了時のみ実施。HTML 上段の抽象群証明の案内、完成表示の維持、証明書なしの案内、未解決 Goal と Citation の不変を確認する。

次工程の Reference 表示改善や記名生成元の証明探索は先取りしない。
