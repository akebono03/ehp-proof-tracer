# Phase 169 R6A — π₈⁶ の2回懸垂輸送接続

## 現状の監査結果（R6）

- π₈⁶ は partial、ProofStep 2、未解決 Goal 7。
- Toda (4.5) は利用可能で、n=4、k=2 なら安定範囲 n≥k+2 を満たす。
- π₆⁴ の登録済み群構造は文献順で先行する。
- π₇⁵ の群構造は文献順で先行しないため、GIVEN として引用してはならない。
- 直接の E² 輸送では、DB に登録された η₆² と IteratedSuspension(η₄², 2) は型として一致しない。

## 変更対象

- 変更する既存ファイル: `phase165_r52_r9_shared_math.py`
- 変更する既存関数: `shared_expansion_provider`（関数全体の置換ファイルを出力）
- 追加するファイル: `phase169_r6a_pi86_two_step_transport/rule.py`
- 新規関数: `_two_step_eta_square_images`、`two_step_eta_square_transport_rule`、`expand_prior_two_step_eta_square_transport`
- 追加位置: R5B の Provider 接続の直後で、既存 EHP Provider 呼び出しの前。
- 新規テスト: `tests/test_r6a_two_step_transport.py`（6件）、`tests/test_r6a_patch_guard.py`（3件）。
- 変更しない既存ファイル: 探索器・Toda 規則・命題台帳・Renderer・既存テスト・五つのルート文書。

## 根目標の推論

以下の4前提をすべて実際に解決できたときだけ、既存の群構造を2回懸垂によって運ぶ。

1. 先行する π₆⁴=Z/2{η₄²} の型付き群構造。
2. Toda (4.5) に基づく E²:π₆⁴→π₈⁶ の型付き同型。
3. η 系列の定義から導いた E(η₄²)=η₅² の GeneratorImage。
4. η 系列の定義から導いた E(η₅²)=η₆² の GeneratorImage。

η₅² は中間の生成元表現であり、π₇⁵ の群構造を証明済みの GIVEN として扱うものではない。各 GeneratorImage は既存の `_composition_eta_suspensions` により両因子が検証できる場合のみ候補とする。安定範囲 n≥k+2 を緩めない。

## 限定テスト

- 新規 pytest 9件と、R6 4件、R5B 6件、R3O 7件、R4C 6件を実行する（合計32件）。
- `R6A_PI86_STATUS=complete`、`R6A_PI86_OPEN_GOALS=0`、`R6A_PROOF_TREE_VERIFIED=True`、`R6A_WEB_KEY=generic-complete-proof` を目標とする。これらは実行前の未確認条件。
- `output/audit.json` と `output/web_narrative.md` に Reference および証明全文を保存し、表示の最終確認は次工程で行う。
- 全体 pytest は Phase 169 完了時に実施する。

## ロールバック

`run.ps1` は既存関数を変更する前に本番ファイルの全バイトをバックアップし、限定 pytest または監査で失敗した場合はバックアップから復元する。すでに本番ファイルが Git 版と異なる場合や、Git blob が変わっていた場合はパッチ前に停止する。

## 次工程との境界

R6A は π₈⁶ の Backward Search の接続のみを目的とする。今後の他の群、η 以外の生成元、反復懸垂一般 r 回への拡張、表示表現の全般的な整理は行わない。
