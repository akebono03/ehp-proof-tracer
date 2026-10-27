# Phase 169 R10EH — 6/10/11/14-stem の証明・文章境界監査

## 目的

R10EG で1-stemの回帰を解消した後、Web で確認された4群について、探索が完了しているのに証明文章が冗長である問題と、出典・推論が足りず未完成の問題を区別する。

- $\pi_{28}^{22}=\mathbb Z/2\{\nu_{22}^2\}$：一般安定輸送が完成したときの巡回群生成元表示と $E^{14}$ の連鎖。
- $\pi_{32}^{22}=\mathbb Z/2\{\eta_{22}\mu_{23}\}$：合成生成元による巡回群の表示と重複した $\eta$ 懸垂。
- $\pi_{33}^{22}=\mathbb Z/8\{\zeta_{22}\}$：未解決 `GeneratorImage` の有無を確認する。
- $\pi_{36}^{22}=\mathbb Z/2\{\sigma_{22}^2\}\oplus\mathbb Z/2\{\kappa_{22}\}$：未解決画像と引用可能な系列定義の有無を確認する。

## 本番ファイルへの変更

なし。新規パッケージ `phase169_r10eh_stem6_10_11_14_audit/` のみ。

`policy.py` は監査ケース・分類のみを保持し、数学的な仮定を作らない。`audit.py` は実際の `search_group_from_registered_goal()` を実行し、`complete` の場合だけ `verify_proof_tree_for_narrative()` で検証する。検証済みの Model に対してだけ R10A / R10EC の圧縮条件を評価する。`partial` の Proof Tree を `complete` に変更しない。

`HyoujiGen.csv` の family ID は表示・型のメタデータであり、そのまま引用可能な命題にはならない。Toda の既存の固定 Reference に位置付けられた系列定義の登録と混同しない。本監査で検査する `SOURCE_RECORDS` は当該汎用 family source connector の範囲に限る。

## テスト

8件の独立した分類テストと、実リポジトリに対する4群の限定監査を行う。全体 pytest は Phase 169 の末尾だけ実施する。既存の追跡済み出力（R10EF の監査ファイルを含む）は一切書き換えない。出力は一意な `output/run_*` の下に保存し、Git の追跡済み変更状態を前後比較する。

## 次の Phase との境界

完成している巡回群に対する Projection の拡張と、未完成の $\zeta$ / $\kappa$ 系列の原典照合は異なる作業である。R10EH はどちらも実装せず、事実を採取する。
