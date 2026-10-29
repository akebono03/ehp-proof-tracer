# Phase 170 R3-R7（改訂）— Toda (5.2) と先行 DB 結果の共通接続

## 対象と数学的根拠

Toda (5.2) の一般形 $\eta_2\circ-:\pi_i^3\xrightarrow{\cong}\pi_i^2\ (i\ge3)$ を使用する。$n=2$ で $m=n+k$ とおくと、輸送元 $(k',n')=(m-3,3)$ は証明対象 $(k,n)=(m-2,2)$ より辞書式順序で前にある。

群構造が零群、有限巡回群、自由巡回群、有限個の巡回群の直和である場合を同一の (5.2) 経路で扱う。生成元が必要な場合には $\eta_2\circ-$ による像を型付き構造で照合する。直和の加法と整数倍は写像の準同型性により成分ごとに照合する。生成元表示が合わない DB 行を無理に証明済みにはしない。

## 既存の信頼境界

先行 DB 行の取得は `exact_prior_database_result()` を使用する。この関数は `sphere.csv` の明示的な行のみを使用する。先行順序は `precedes_db_goal()` に従う。下位 Goal から `GIVEN` を作成するのは既存 Backward Search であり、`admitted_db_step()` が DB の内容と辞書式順序を検証する。公開時には `verified_db_step()` により同じ DB を再読込して検査する。

Toda (5.2) 自体は、文献の出典審査を通過した `Toda52UniversalStatement` を要する。DB 前提を文献命題と偽って表示しない。

## 変更ファイル・関数

変更は `phase168_r2_toda52_transport.py` のみで、既存関数 `expand_toda52_finite_cyclic_goal()` を共通入口として維持する。旧実装は新しい `_expand_toda52_screened_cyclic_goal()` にそのまま移し、既存の証明経路を優先する。新規補助関数 `_eta2_inverse_image()`、`_toda52_group_presentation_matches()`、`_toda52_ordered_db_rule()` を、その旧経路の後に追加する。import 領域は変更しない。

## 限定検証と Phase 境界

既存の R3-R5、R3-R6、R10E4 のテストに加え、構造ごとの新規 pytest を実行する。証明探索と Web 表示は $\pi_5^2,\pi_6^2,\pi_7^2,\pi_8^2,\pi_9^2,\pi_{10}^2,\pi_{11}^2,\pi_{12}^2,\pi_{16}^2$ を対象にする。失敗時は修正対象1ファイルを自動復元する。全体 pytest は Phase 170 終了時のみ実施する。

$\pi_2^2$ は $i=2$ のため (5.2) の対象外。高次 DB で型付き生成元が一意に復元できない行の対応は別課題とする。個別 Proposition の大量登録や DB データの変更はしない。
