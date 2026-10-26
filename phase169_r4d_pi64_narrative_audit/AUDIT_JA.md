# Phase 169 R4D — π₆⁴ 証明本文・Reference 読み取り専用監査

## 対象

- GitHub の `develop` 現行コード上で実行する。
- `π₆⁴ = Z/2{η₄²}` の18ステップ完成証明、未解決0件、Proof Tree の出典境界を再検証する。
- Web の標準入口 `build_standard_web_group_proof_view(4, 2, mode="narrative", citation_source="model")` を実行する。
- 共通 Narrative Model と Renderer から Reference と本文の全行を保存する。
- 命題番号の対応、本文で使用されない Reference、未登録の引用タグ、数式区切り、証明末尾を監査する。

## 改変範囲

アプリケーションコード・既存テスト・既存文書は変更しない。新規監査パッケージだけを追加し、結果はこのパッケージの `output` に出力する。既存の R4C `output` は変更しない。既存の追跡ファイルの変更が生じた場合は、該当ファイルを表示して停止し、黙って上書きしない。

## 限定 pytest

新規4件、R4Cの6件、R3Zの3件の計13件を指定する。全体 pytest は Phase 169 の最後まで実行しない。

## 完了条件と次工程

証明の complete、Web 側の complete、出典の真正性を確認したうえで、表示上の検討事項を機械的に列挙する。表示に修正が必要なら、後続 R4E で現在の Renderer と表示テストを改めて確認し、必要最小限の範囲のみ修正する。R4D は表示を変更しない。
