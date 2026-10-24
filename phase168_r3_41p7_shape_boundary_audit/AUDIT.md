# Phase 168 R3-41P7 — 数学的再判定の残存経路監査

## GitHub develop での事前確認

対象ファイルと関連テストを GitHub `akebono03/ehp-proof-tracer` の `develop` で確認した。GitHub の状態と Windows 作業ディレクトリが一致しない場合もあるため、実行環境のファイルを改めて読み、SHA-256 と動的呼び出しを記録する。

- `phase168_r3_27_typed_statement_projection.py` — `project_stable_eta_notation_transition()`、`typed_sentence()`。
- `phase166_r3ac_stable_notation.py` — `_stable_eta_renaming_shape()`、`stable_eta_notation_rule()`。
- `phase165_r12_r11_prop42_unified.py` — `prop42_exactness_indices()`、`prop42_specialization_inference_rule()`。
- `phase165_r12_r12_ehp_consequences.py` — `EHPImageEqualsKernelStatement`、`ehp_image_equals_kernel_inference_rule()`。
- `phase168_r3_5_model_renderer.py`、`phase168_r3_3_proof_narrative_model.py`。
- 関連テスト：`phase166_r3ac_stable_notation/tests/test_r3ac.py`、R3-41P6、R3-41O、R3-41N1、R3-29、R3-39A。

## 事前監査の結論

1. `_stable_eta_renaming_shape()` は推論側で写像・次数・$\eta$ の型情報を検証する。Typed Projection 側の再呼び出しは責務重複候補。
2. `prop42_exactness_indices()` は Proposition 4.2 の特殊化と EHP の像＝核の推論を検証する。Typed Projection にも再判定がある。
3. 3群の R3-41P4 監査では、いずれも表示側での呼び出しは0回。ただし、それは将来の群に不要な証明にはならない。
4. 型付き ProofStep の妥当性が証明探索で保証されていても、手動構築した Model の不正な値を表示側で拒否する挙動は現状存在する。削除する際には、この境界を意識する必要がある。

## この ZIP の変更対象

アプリケーション・既存テストの変更は **0ファイル**。

新規監査パッケージのみ：`audit.py`、`run.ps1`、`tests/test_audit_helpers.py`、3群の既存全文 fixture、`README.md`、`AUDIT.md`。

## 完了条件

限定 pytest が通過し、3群の全文・Reference・Citation provenance が維持され、正常例と不正入力例の扱いが検査できること。

## 次工程との境界

この監査だけで既存 Renderer のチェックは削除しない。結果をもとに、Model の信頼境界を明確にしたうえで、必要な最小実装のみを次工程で行う。全体 pytest は Phase 168 最終時のみ。
