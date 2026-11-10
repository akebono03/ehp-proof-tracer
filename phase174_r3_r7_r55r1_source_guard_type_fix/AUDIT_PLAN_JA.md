# Phase 174 R3-R7 R55R1 修正設計・監査契約

## 基準

- GitHub `develop` HEAD: `40db3a00ca8be58e589e0949e6a70dcedd3b9cf5`（R54 取込み）。
- 現行 `phase168_r3_5_model_renderer.py` と R54 HTTP テストを確認済み。
- R55 `source_guard.py` の `verify_checkout()` に対する型の取り違えのみ修正する。
- 本体 Renderer の改善方法と Proof Search / 共通 Narrative / 数学規則は変更しない。

## 再現症状

`replace_lines_preserving_eol(norm(previous))` が `str` を返すにもかかわらず、`norm(desired)` が `decode()` を再実行するため `AttributeError` になる。

## 対応

`installed=(norm(actual)==norm(desired))` を `installed=(norm(actual)==desired)` に置き換える。
`source_guard.py` の全文を予期した内容 SHA-256 と照合し、差分を1箇所に限定。CRLF/LF 差は正規化して照合し、実際の改行は保持する。

## 検証

- R55R1 の5件の限定テストは修正後関数の未実装・実装済み両方を模擬実行。
- 修正前でも `R55R1 -DryRun` は Source Guard を変更しない。
- 本実行で R55 Source Guard のみ修正し、R55 の既存 DryRun→本実行→限定 pytest を再実行する。
- 全体 pytest は Phase 174 最後のみ。

## 完了条件

`R55R1 RUN=PASS` と `R55 RUN=PASS`、公開 HTTP 2経路で `generic-complete-proof` と共通導入文1回、28 ProofStep・未解決 Goal 0件を確認する。証明木・数学的根拠・Renderer 変更範囲は R55 と同一。

## 次 Phase との境界

R55 の表示重複修正とその回帰が完了した後、Phase closeout 用の文書更新・全体 pytest へ進む。R55R1 でその作業を前倒ししない。
