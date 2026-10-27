# Phase 169 R10E8-R2 — 改行形式対応

## 原因

ユーザー環境の `phase165_r52_r9_shared_math.py` は CRLF 改行であったが、R10E8 の `patch.py` は `b"\r\n"` を検出すると `expected LF working source` で停止していた。Git の blob SHA 照合は通過しており、内容の相違ではなく Windows 作業ツリーの改行表現が原因である。

## 変更対象

今回新設する `phase169_r10e8r2_crlf_safe_patch/newline_support.py` の `decode_working_source()`、`encode_working_source()`、`patch.py` の `apply_guarded_crlf_patch()` と `main()`、`run.ps1`、限定テストのみ。既存の R10E8 `patch.py` や本番規則を変更しない。

R10E8 の未適用パッチが正常に通過した場合に置き換わる本番の2ファイルは従来と同じ。

- `phase169_r10d2_general_family_definition/family_citation.py`
- `phase165_r52_r9_shared_math.py`

## 安全境界

R10E8 の `transformed_sources()` をそのまま呼ぶ。したがって文字列アンカーの出現回数、重複適用拒否、AST 構文検査は従来どおり。LF・CRLF はファイルごとに統一されている必要がある。混在形式、bare CR、BOM、不正な UTF-8 を拒否する。書き込み後の失敗時は事前のバイト列を復元する。HEAD は検証した祖先からの派生であり、そこからの変更が R10E8-R1/R2 フォルダに限定されている場合のみ受け入れる。さらに関連ファイルの blob SHA を照合する。

`HyoujiGen.csv` は型情報、引用済み Chapter VI の定義は出典、共通 `expand_cited_stable_family()` は推論規則、各 `GeneratorImage` は証明課題、という責務分離を維持する。CSV だけから懸垂像を `GIVEN` としない。

## テスト・完了条件・次段階

ローカル実施済みの補助テストは9件 PASS。Windows の本体 pytest は ZIP の `run.ps1` で R10E8・R10D2・R10E5・R10E4 とともに限定実行する。証明探索監査により $\pi_{23}^{15}$ と $\pi_{24}^{15}$ を再評価する。未解決 `GeneratorImage`・`Relation` が残る限り `partial` を維持する。全体 pytest は Phase 169 の最後のみ。次段階は完成 Proof Tree の検証と文章化であり、本修正はその実装を先取りしない。
