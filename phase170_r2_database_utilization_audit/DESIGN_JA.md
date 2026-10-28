# Phase 170 R2 — DB 活用状況監査（AUDIT_ONLY）

目的は、R1 の実証済み探索記録と現行データベース・Goal 変換器・命題台帳を比較して、未活用情報があり得る箇所を分類すること。ここで新しい数学的規則、DB prior の採用資格、文献命題の掲載順、Renderer の動作を変更しない。

調査対象は `data/sphere.csv`（群構造）、`data/sphere_relation2.csv`（関係式）、`data/HyoujiGen.csv`（生成元表）、`data/TBtable.csv`、ならびに typed Goal 変換と Toda 命題台帳である。

確認する経路は `CSV → 構造化/簡易/零群候補 → 本番 Goal 選択器 → 証明探索（R1 既存記録）→ Proof Tree/Reference 実使用`。DB 行の存在、型付き候補への変換、出典条件を満たした GIVEN としての採用、推論による導出を区別する。

`SEARCH_FAILED` は証明不能と解釈しない。候補ゼロの場合は `NO_TYPED_GOAL_CANDIDATE`、複数候補の場合は `AMBIGUOUS_TYPED_GOAL`、候補があり未完成の場合は原則として `GOAL_EXISTS_SEARCH_OR_PREMISE_UNRESOLVED` とし、R3 で未解決 Goal と前提を詳査する。これらは診断ラベルであり、数学的な不足を確定するものではない。

監査は新規パッケージのコードと限定テストだけで構成する。既存 Git tracked ファイル・index・既存テスト・監査記録の削除や上書きを行わない。全体 pytest は Phase 170 の終了時まで実行しない。
