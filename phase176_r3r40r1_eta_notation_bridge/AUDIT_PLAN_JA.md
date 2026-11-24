# R3R40R1 — η-family の型付き表記接続

## 変更対象

既存ファイルは変更しない。新規ディレクトリ `phase176_r3r40r1_eta_notation_bridge` に `source.py` の `eta_notation_backward_plan()`（内部 `add()`、`build()`）、`connection_backward_plan()`、`audit.py` の `source_guard()`、`probe()`（内部 `provider()`、`visit()`）、`main()`、限定テスト、実行スクリプトを追加する。

## 数学的根拠

Toda の η-family 定義に基づく既存の型付き懸垂等式を二つの異なる表記に適用する。$E\eta_{n-1}=a$ と $E\eta_{n-1}=b$ を独立に推論し、対称律と推移律で $a=b$ を得る。合成因子の型と構造を再帰的に確認し、左右合成の等式保存で合成全体を接続する。結合律や文字列置換による同一視は行わない。

R3R39 の中間 Hopf 等式と Toda (5.5) の順方向等式は既存の共有探索の独立義務として残す。監査用 Provider は対象となる等式だけに既存規則を優先提示し、証明済みステップや GIVEN は挿入しない。

## 完了条件

出典選別、実際の DFS による既存規則の証明木再生、η-family 懸垂の独立推論、R3R39 の6段階、Toda (5.5) の出典付き推論、最終 Hopf 等式を確認する。限定 pytest と Git 差分検査も通過すること。公開 Provider への接続と根の群構造証明は次工程。全体 pytest は実施しない。
