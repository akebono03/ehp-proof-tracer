# Phase 169 R10EI — 巡回群の懸垂等式残差監査

## 現在の観測と対象

R10EH-R1（2026-10-28）の限定監査では、$\pi_{28}^{22}$ は complete / Trust PASS / 54 ProofStep、1段の懸垂等式17本、重複0件、R10A 適用可能と報告された。一方、$\pi_{32}^{22}$ は complete / Trust PASS / 68 ProofStep、懸垂等式20本、重複10件、R10A 適用不可だった。

いずれも数学的導出は検証済みであり、今回の作業は **Narrative Projection（証明文章への射影）** だけの調査とする。11-stem の $\pi_{33}^{22}$ と14-stem の $\pi_{36}^{22}$ は partial のままにし、ここでは扱わない。

## 監査方法

1. 登録済み Goal と Backward Search により対象2群を再探索する。
2. complete を確認し、実際の screened Bridge（文献選別済み接続）を使って Trust Boundary を再実行する。
3. Proof Narrative Model のステップ列が採用済み Proof Tree と一致するか確認する。
4. R10A / R10EC の既存 Projection を変更せず、適用可能性・非表示対象のインデックスを取得する。
5. 出力された `$E(\alpha)=\beta$` 形の等式と重複を記録する。
6. 対応し得る `GeneratorImage` / `GeneratorSuspension` の **実際の型付き結論**を調べ、親 ProofStep、consumer、個別 Citation、GIVEN 祖先を記録する。表示文字列の一致は診断にとどめる。

## 追加ファイル

- `diagnostics.py`：`AuditCase`、`image_formula_occurrences()`、`extra_duplicate_occurrences()`、`validate_coverage()`、`assess_case()`。
- `audit.py`：`_source_citations()`、`_typed_formula()`、`_typed_step_index()`、`inspect_case()`、`_markdown_report()`、`main()`。
- `tests/test_r10ei_diagnostics.py`：文字列集計と監査ケース範囲を確認する限定テスト。
- `run.ps1`：Git の祖先・対象 blob・未変更状態を点検して限定テストと本体監査を実行する。

既存 import、既存関数、既存クラス、既存テスト、本番ファイル、DB、Toda 原典への変更はない。

## 完了条件と次 Phase の境界

- $\pi_{28}^{22}$ と $\pi_{32}^{22}$ が complete / Trust PASS。
- 既存 Reference と Proof Tree を保持。
- 懸垂等式の実際の発生源と、非表示可能性を判断するための consumer と引用の対応を記録。
- Git 管理下の既存ファイルに変更なし。
- 全体 pytest は **Phase 169 の最後だけ**実行する。

次の実装では、真に単独消費される証明ステップの文章だけを省略し、既存の推論・出典を変更しない。監査結果の数式一致だけでは省略を正当化しない。
