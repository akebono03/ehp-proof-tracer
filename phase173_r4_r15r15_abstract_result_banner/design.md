# Phase 173 R4-R15R15 — 抽象群証明の結果案内を統一

## 問題

従来の `templates/index.html` は、群問い合わせの `WebGroupQueryView.status=not_found` と、Web 証明の `partial_result` のみを参照する。このため、`\pi_{12}^{4}` などで「No proof-backed result found」と表示される一方、同じ画面に検証済みの抽象群構造が表示される。

この `not_found` は**記名生成元を含む完成証明**がないことを意味し、抽象群構造の証明がないことは意味しない。`WebGroupQueryView` の API と検索結果は変更しない。

## 共通経路

`Proof Search → PartialProofResult.abstract_structure → WebGroupProofView.abstract_structure_certified → templates/index.html`。

`CertifiedAbstractStructure` は既存の `PartialProofResult.__post_init__` により型付き ProofStep に裏付けられる。Web Adapter はその非 None 判定のみを渡す。Template は証明文の見出し文字列や出典本文を照合しない。

表示は共通の `WebGroupProofView` によって、次の三状態を分ける。

1. `partial_result=False`：記名生成元まで完成。
2. `partial_result=True` かつ `abstract_structure_certified=True`：抽象群構造のみ証明済み。
3. `partial_result=True` かつ `abstract_structure_certified=False`：完成証明も抽象群の検証済み証明書もない。

フィールドは既定値 False とするため、既存の他の Web 呼び出しを破壊しない。型チェックを追加し、完成状態と抽象群のみ証明済みの矛盾を拒否する。

## 変更境界

変更する本番ファイルは `web_group_proof_common.py`、`phase165_r52_r3_web_adapter.py`、`templates/index.html` の3つのみ。探索規則・DB・Reference・数学的同型・Markdown 本文・R15R14 の改修内容は変更しない。実装後は限定 pytest のみ実行し、全体 pytest は Phase 173 終了時まで保留する。

## 実行前条件

GitHub `develop` HEAD は `9729d3ee51e93f26cf6b31a3880cb1a92a552f2c`。ローカルの R15R14 未コミット変更2ファイルは、登録済み R15R14 の完全な変換結果と一致することが必須。その他の未レビューの tracked 変更や staged 変更があれば停止する。

## 完了条件

`n=4,k=8` は抽象群のみ証明済みの案内、`n=4,k=4` は完成案内、抽象群証明書のない未完成では従来の案内とする。元の証明状態・数式・引用・未解決 Goal を変えない。ブラウザ実表示はユーザー側で確認する。
