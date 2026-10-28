# Phase 169 R10ER-R1 — 安定元の Definition と直和群の表示

## R10EQ-R1 の結果

ユーザー実行で限定 pytest 72 PASS、π₄₁³⁰・π₄₄³⁰ における完全証明と Trust PASS を確認した。π₄₆³⁰ についても Web の完成証明表示が提示された。現行 Renderer は引用由来の像ごとに GIVEN 祖先を必須とするため、R10EQ で導入された Definition 由来の推論には表示圧縮を適用できない。

## 今回の変更対象

`phase169_r10ec_direct_sum_narrative_projection/projection.py` の `project_verified_direct_sum_transport()` のみを全文置換する。既存 import、既存クラス、探索、推論規則、共通 Definition、Reference 台帳、Trust Boundary は変更しない。

引用由来の `GeneratorImage` は、R10EN の `require_each=True` で各像の GIVEN 祖先を必ず照合する。無引用の像を認めるのは、既存 `expand_defined_stable_element_image()` で生成できるものに限り、原則としてゼロ前提の定義的な INFERENCE であること、推論規則の名称・記述・前提パターン・結論・matcher の成立を確認する。名前や表示だけから数学的な等式を新たに証明しない。

R10EL の利用先確認・排他的消去の要件は変更しない。Proof Tree は不変で、文章のみを圧縮する。引用の存在しない Definition の像に架空の [R] を付けない。

表示目標：

$$
E^{14}(\sigma_{16}^{2})=\sigma_{30}^{2},\qquad E^{14}(\kappa_{16})=\kappa_{30}.
$$

$$
E^{12}(\omega_{18})=\omega_{30},\qquad
E^{12}(\sigma_{18}\mu_{25})=\sigma_{30}\mu_{37}.
$$

## テスト・完了条件

限定 pytest、π₄₄³⁰・π₄₆³⁰・既存の 9-stem の Web 完成証明、すべての Trust Boundary の PASS、反復懸垂表示の各2式のみ・1段階等式0件、引用検証維持、対象外の追跡ファイル無変更。

Windows 側で実行するまで統合動作は未確認。失敗時は変更対象の1ファイルだけを復元する。全体 pytest は Phase 169 終了時のみ。

次段階では、巡回群・直和群の表示をさらに共通化する余地はあるが、本 R1 では行わない。
