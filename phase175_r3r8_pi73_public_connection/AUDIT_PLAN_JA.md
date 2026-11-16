# Phase 175 R3R8 — 公開接続監査計画

## 前提となる実測

ユーザーの2026年11月16日実測で、R3R7の限定pytestはDryRun・本実行とも50件PASS。出典Guard、R3R6証拠、Git不変性はいずれもPASS。以下の6義務が独立に `INFERRED` となった。

1. `lemma54_double_relation`
2. `double_suspension_membership`
3. `lemma57_zero_generator_image`
4. `zero_suspension_image`
5. `hopf_injectivity`
6. `pi73_cyclic_lift`

しかし通常のWeb Group queryは `generic-partial-proof`、未解決Goal、参照0件のまま。R3R7の `audit.inspect_actual_search()` がローカルの追加Providerを使用している一方、通常検索の `search_shared_group_goal()` はそのProviderを呼ばないことが原因である。

## 実装前のGitHub調査

- リポジトリ: `akebono03/ehp-proof-tracer`、`develop`、監査時HEAD `40bd19c0a91d09e7aaf15b216eae985fda65e347`。
- `phase165_r52_r9_shared_math.py::search_shared_group_goal`、追跡Git blob `9fa11b383812570fae1a26868c98992a5934a327`。
- `phase165_r55_nk_only_goal.py::search_group_from_registered_goal`：通常Group queryの登録済みGoalとCitation IDへの接続。
- `phase175_r3r7_lemma54_membership/audit.py::inspect_actual_search`、`rule.py`：6義務の実際の推論鎖と提案順。
- `phase175_r3r6_lemma57_general/source.py`, `rule.py`、`phase173_r4_r1_lemma54_source_bridge/source.py`：出典付き一般規則と検証済みLemma 5.4。
- `phase173_r4_r1_public_connection/route.py`：既存の公開接続手法。
- `phase175_r1_k4_audit/audit.py::inspect_one_group`：実際の検索、trust boundary、共通Renderer、Webを一括検証する既存監査。
- 関連既存テスト: R3R7の `tests/test_rule.py`、R3R6の `tests/test_rule.py`、R3の `tests/test_rule.py`、R4R1公開接続の `tests/`。

## 変更対象

**既存コードの変更は1関数のみ。**

- `phase165_r52_r9_shared_math.py::search_shared_group_goal()`：`n=3,k=4`、かつ利用者指定Provider不在の場合に、既存の公開接続に並ぶ経路を追加する。関数の全文は同梱 `search_shared_group_goal_FULL.py.txt` に格納。トップレベルimport変更なし。

**新規コード**（各ファイルの全文を同梱し、`CODE_FULL_JA.md`でも確認できる）。

- `route.py::public_cited_ehp_extensions`, `route.py::prepare_pi73_public_connection`：出典確認と一般規則候補群の公開Provider化。変更する既存クラス・関数はなし。
- `install.py`：変更前の全ファイル・Git blob・ASTをガードし、関数内部に一箇所だけ挿入。EOL維持・バックアップ・失敗時復元。
- `audit.py`：R3R7実測証拠検証、限定pytest、実検索・Web監査、失敗時の復元。
- `tests/test_install.py`, `tests/test_route.py`：パッチ・公開Goal・GIVENを偽造しない境界。
- `run.ps1`：DryRunおよび通常実行。

## 禁止事項

目標群の直接GIVEN、未証明の特例ゼロ写像、証明木の再利用、専用Narrative、Renderer変更、全体pytest、追跡対象の他ファイル変更を禁止する。対象以外の群への拡張はこのR3R8では行わない。

## 成功条件

実際の通常 `(n,k)=(3,4)` 検索で`complete`、結論が `sphere.csv` の登録済み目標と一致、open goal 0、証明ステップあり、共通trust boundary通過、ProofNarrativeModelのroot確認、Webが `generic-complete-proof`、partial false、Reference2件以上、例外なし。失敗なら元ファイルを正確に戻してEXIT非ゼロ。

次のR3R9以降で、$\pi_9^5$ と $\pi_{10}^6$ の未完成義務を改めて監査する。Phase 175全体pytestは最後だけ。
