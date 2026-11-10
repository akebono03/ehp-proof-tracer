# Phase 174 R3-R7-R54 監査計画

## 監査基準

GitHub `akebono03/ehp-proof-tracer` `develop` の監査済み HEAD: R52 マージ後 `1151d6a3044fd7fae2ff1fb864a83afdaefc285d`、R53 マージ後 `e2598a3b4c865afea15b06b097c809333fabcc85`。現在の実リモート HEAD は後者を確認済み。ユーザー環境の R53 は Source Guard・公開 Proof Search・Web Model の検証が PASS している。GitHub の対象コードと既存 Flask テストの現在版を確認済み。

## 対象と変更ファイル

新規追加は `phase174_r3_r7_r54_public_http_narrative_audit/` のみ。既存本番ファイル、README.md、design.md、development_log.md、roadmap.md、proof_records.md は変更しない。

- `source_guard.py`: `verify_checkout()`。R53 未コミット・R53 マージ済みの既知 HEAD のみを受け入れ、実装済み関数を内容比較し、HTTP 経路・HTML テンプレート・Renderer・Proof Trust Boundary の Git blob を厳密照合。
- `audit.py`: `ProofHTMLParser` クラス、`observe_response()`、`inspect_public_http_proof()`、`report_path()`、`main()`。公開 `POST /` を実際に呼び出す。
- `tests/test_html_parser.py`、`tests/test_static.py`、`tests/test_guard.py`、`tests/test_http.py`: HTML 契約、改変防止、Source Guard、公開 HTTP を検証。
- `run.ps1`: DryRun と本監査、限定 pytest、R53 の既存公開回帰テスト。

## 完了条件

Group query と Group proof form の両方で HTTP 200、`\pi_{12}^{7}=0`、`generic-complete-proof`、使用文献、`□` を確認する。証明木からの ProofStep を直接注入しない。導入文の重複件数は測定値として JSON に記録し、合否判定の対象にしない。

## 次の工程との境界

R54 は HTTP レスポンスの契約監査のみ。ライブサーバ・ブラウザ・KaTeX の視覚検証と、共通 Renderer での重複文の一般的改善は別工程。全体 pytest は Phase 174 の最終段階まで実施しない。
