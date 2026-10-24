# Phase 168 R3-41P6 — 規則名依存の文章判定修正

## GitHub 現行コードの事前確認

2026年10月24日、`akebono03/ehp-proof-tracer` の `develop` にある以下を確認した。

- `phase168_r3_27_typed_statement_projection.py`：`typed_sentence()`、既存の型付き Statement、`has_exactness()` の再帰処理。
- `phase168_r3_5_model_renderer.py`：P5 改善後の Renderer。
- `phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py`
- `phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py`
- `phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py`
- `phase168_r3_39f_frozen_comparison/audit.py`
- `phase165_r12_r12_ehp_consequences.py`、`phase165_r14_r6_generic_iso.py`、`proof.py`

GitHub の最新ソースと Windows 作業ツリーは異なる可能性があるため、適用時に R3-41P4 の監査 SHA-256 を照合する。

## 変更対象（最初に明示）

**既存実装**

1. `phase168_r3_27_typed_statement_projection.py` の関数 `typed_sentence()` のみ。
2. モジュール import 節・既存クラス・その他の関数を変更しない。

**追加**

- `phase168_r3_41p6_typed_exactness_prose/patch.py`、`restore.py`、`run.ps1`
- 同じパッケージの2つのテストモジュール（そのうち一つは配布パッチ安全性用）
- `baselines/` の R3-41P5 3群全文

## 変更理由

旧条件の `"exact" in str(getattr(p.inference_rule, "name", "")).lower()` は、規則の説明上の名前だけで「完全性より」という文章を選択する。今回、これを削除して、前提が `TodaProp42ExactnessStatement` または `EHPImageEqualsKernelStatement` の場合のみにする。既存の再帰的 `has_exactness()` はそのまま維持する。

これは数学的な規則の再実行ではなく、証明木中の型付き前提に従う文章表現である。

## 出力契約

ZIP 内に完全な適用・復元・テストコードを収録する。適用時に `typed_sentence()` **全関数**と変更ファイル**全文**を書き出す。
省略記号によるコード省略はしない。

## 限定テスト

- 3群の公開 Web の証明本文および Reference の R3-41P5 保存全文との完全一致。
- ProofStep 数、出典数、Citation provenance、固定基準の論証維持。
- 規則名だけに `exact` が含まれても「完全性より」と表示しない。
- 直接または間接に型付き EHP 完全性が存在する場合は従来の説明を維持。
- 関連既存テスト。**全体 pytest は実行しない。**

## 境界

R3-41P6 は「完全性の説明に使われる規則名依存」の修正のみ。
残る `_stable_eta_renaming_shape()` と `prop42_exactness_indices()` の未使用／追加群での処理は次の個別監査で判断する。Phase 168 の終了確認・全体 pytest を先取りしない。
