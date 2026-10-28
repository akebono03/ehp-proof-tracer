# Phase 169 R10ET-R6 — Definition の残存依存監査

## 目的

R10ET-R5D で本番化した共通 Definition の優先順位について、完成証明の Proof Tree（証明木）から依存関係を検証する。特定の名前・family に依存した判断ではなく、型付き `GeneratorImage` の結論と実際の推論規則に基づいて判定する。

## 対象

既存の検証済み16ケースを必須対象とし、$\pi_{10}^{8}$、$\pi_{22}^{13}$、$\pi_{24}^{15}$ の3ケースを追加調査とする。必須対象は R2 の Shadow Proof Tree と比較する。新しい3ケースは既存の検証済み出力を持つ調査例であり、無条件の一般化を意味しない。

## 監査方法

1. GitHub で確認済みの `10et4` commit の5ファイルを R5D の `transform()` に通して期待する R5 バイト列を作り、現在の作業ファイルと照合する。R4 の2ファイルも Git blob を照合する。
2. 追加済みの R1 の `inspect_case()` を再利用し、本番の探索経路で Proof Tree・Reference・Narrative を生成する。`shared_expansion_provider()` の monkeypatch は一切しない。
3. 完成証明に対する Trust Boundary を実行する。`GeneratorImage` のうち `is_defined_stable_image()` に適合するものは `canonical_definition_inference()` により再生可能な正規推論であることを確認する。
4. 使用中の引用が root の祖先である GIVEN に結び付き、Reference に表示されることを確かめる。一般の安定群輸送の10ケースでは最初の2つの前提がそれぞれ DB prior と Toda (4.5) に支持されることも検証する。
5. R2 の引用順・Definition 採用数・2つの前提の支持引用が変わっていないことを確認する。追加3ケースは別枠とする。
6. 監査前後の `git diff --raw -z` と `git diff --cached --raw -z` を照合する。既存の未コミット変更やステージ済み資料を変更しない。

## 判断の境界

- 個別 Definition が命題台帳に登録されていることだけでは、完成証明がそれに依存しているとは言えない。
- 現行 Proof Tree が適用可能な共通 Definition で構成されていることは確認するが、すべての $n,k$ について証明探索が完成するとは主張しない。
- 共通 Definition が適用できない低次元・不安定域の命題を一律に置換しない。
- DB prior と Toda (4.5) を表示上の都合で削除しない。
- R6 は AUDIT_ONLY とし、本体・既存テスト・ドキュメントを改変しない。全体 pytest は Phase の終了時に実行する。

## 変更対象

新規フォルダ内のみ：`audit.py`、`run.ps1`、`tests/test_r6_helpers.py`、`README.md`、`DESIGN_JA.md`、`__init__.py`。既存 API・既存ファイルの変更はない。

## 完了条件

必須16ケースと追加3ケースが `complete`、Trust PASS、共通 Definition 適用可能な像に個別引用依存がないこと、R2 基準の Reference が維持されること、Git の追跡差分・ステージ領域が変更されないこと。限定 pytest が PASS。R6 は監査として完了し、後続 Phase に機能を先取りしない。
