# Phase 170 R3-R4 — $n=2$ 連続群の証明一般化監査

## 問題

$\pi_5^2$ が DB で既知でも Web が `generic-partial-proof` しか表示しない。これは証明探索、型付き Goal、Citation、Narrative のどこかに未完成の経路があることを意味するが、DB の値が誤りであることや数学的証明不可能を意味しない。同様に $\pi_6^2,\pi_7^2,\ldots$ の処理を確認する。

## 評価する境界

1. `data/sphere.csv` と `data/HyoujiGen.csv`：群構造・生成元のデータ。証明としては利用しない。
2. `registered_group_goal_candidates()`：型付き Goal を作れるか。`database_zero_group_goal_candidates()` は零群専用。
3. `resolve_specialized_goal_citing_id()`：引用位置を決定できるか。
4. `search_group_from_registered_goal()`：実際に `COMPLETE` となるか。未解決 Goal を保存する。
5. 未完成では本番と同一の Model と Web Adapter、完成時には本番 Web 経路と Trust Boundary を通す。

## 対象

初期設定は $n=2,k=3,4,5,6,7,8,9,10$。`-MaxK` で $k\leq20$ まで範囲を拡張できる（有限標本監査）。$k$ が変わると群構造も必要な数学的導出も異なるので、汎用推論規則の存在だけでは一律に完成と判定できない。

## 安全条件

現行 GitHub `develop` のレビュー済み HEAD と対象ファイルの Git blob ID を検査する。以後のコミットは Phase 170 の独立監査パッケージの追加だけを許し、既存ファイルの変更は拒否する。DB の変更、tracked file の編集、index の変更も拒否する。子プロセスを群ごとに分離し、監査上の長時間実行を timeout として記録する。全体 pytest は実行しない。

## 完了条件

各群について DB 登録・Goal 選択・検索状態・Web 表示が区別された監査結果と、変更のない Git 状態を得る。`COMPLETE_AND_WEB_VERIFIED` 以外は完成を主張しない。未解決の具体的推論規則や数学的根拠の実装は次の段階に委ねる。
