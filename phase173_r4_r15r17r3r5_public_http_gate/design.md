# Phase 173 R15R17-R3R5 設計

## 監査の位置付け

R15R17-R3R4 では歴史的なテスト契約10ファイルを修正し、限定 pytest 92 PASS をユーザー環境で確認した。R3R3 の型付き未解決 Goal の表示集約と R3R4 の契約修正を、公開 Flask の HTML まで追跡して監査する。本工程は本体の変更を伴わない。

## 対象コードと基準

2026-11-04 時点の GitHub develop HEAD は `a3baa7f2d5fa94983bbe1b795bd1883d57680b5b`。Web 入口は `web_app.create_app()` の通常の Group query POST、証明経路は `build_group_proof_progress_view()`、`build_standard_web_group_proof_view()`、共通 Model と Renderer、`templates/index.html` である。実際の証明探索はスタブ化しない。別機能の Group query データ照会のみ、既存の Web 回帰テストと同様に `NOT_FOUND` に差し替える。

## 監査内容

1. `(n,k)=(4,8)`：抽象群証明書あり、記名生成元は未完成、Reference 1か所、未解決 Goal は内部3件・画面1行集約、抽象群の同型 `\\cong` が検証済みステップにある。
2. `(4,9)`：抽象群証明書あり、記名生成元は未完成、未解決 Goal は内部2件・画面1行集約。
3. `(5,3)`：抽象群証明書なし。推論ステップや引用文献を捏造せず、内部3件・画面1行集約。
4. `(4,4)`：記名生成元の完成証明。未解決 Goal と別 Section を追加しない。

Web 実出力に対して `<div id="group-proof-rendered-lines">` 以下を HTMLParser で抽出し、見出し、文章、`data-latex` に対して検査する。別に小さな HTMLParser の契約テスト4件を置く。

## 安全性と Phase 境界

- `git fetch origin develop` はリモート参照取得のためだけに実行する。
- ローカルとリモートの HEAD は基準コミットの子孫であることを確認する。GitHub の追加コミットがあっても、関連本体ソースに差分がなければ監査を許可する。
- 本体対象ファイルのリモート差分・ステージ済み差分・未ステージ差分があれば中止する。
- `git reset`、`git clean`、`git add`、`git commit` は実行しない。Git index の前後同一性を確認する。
- `pytest -p no:cacheprovider` を用い、既存の `.pytest_cache` を変更しない。全体 pytest は Phase 173 終了時だけとする。
- HTML テストの合格はブラウザのレイアウト・MathJax 描画の実確認を意味しない。`MANUAL_BROWSER_CHECK.md` の手動確認を別途必要とする。
- 旧 legacy API の変更、数学的探索規則の追加、ProofStep の再解釈、未解決 Goal の内部削除は行わない。
