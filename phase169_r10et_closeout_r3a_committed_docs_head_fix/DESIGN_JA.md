# R10ET Closeout R3A — Git コミット後の監査条件調整

## 事実

R3 作成時の `develop` は `a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5`。その後、R2A で作成した主要文書5件と更新パッケージが `6e5d6bbed186dd4da706b54c308f94041a32e6d7` にコミットされた。R3 の限定 pytest は8件 PASS したが、旧 HEAD 検査により実監査を開始できなかった。GitHub の比較では証明実装・関連テストの追加変更はない。

## 変更対象

- `phase169_r10et_closeout_r3_final_readonly_audit/audit.py` の `REVIEWED_HEAD` と追加定数 `R2A_MANIFEST_HEAD`。
- 同ファイルの `certify_documents()`：R2A manifest を作成当時の HEAD で検証。
- 同ファイルの `execute()`：コミット済み文書を前提に tracked 未変更を要求。
- 新規 R3A パッケージのパッチ・テスト・実行コード。

import 変更なし。監査対象の数学的規則、Proof Tree、Narrative Model、Renderer、DB、主要文書5件は変更しない。旧 R3 のコード、変更後コード、変更関数全文は `reviewed_sources/` に収録する。

## 安全性

R3 の `source blob` 8件、文書全文のバックアップ・SHA-256・ZIP 照合、R6D の19ケース、GitHub remote HEAD、Git index 不変の検査を維持する。元の R3 audit.py に一文字でも想定外の変更があればパッチを拒否する。元ファイルは `%LOCALAPPDATA%\EHPProofTracerRecovery` に保存する。失敗時には旧 audit.py に復元する。R3A は Phase 169 全体の完了を認定せず、全体 pytest を実行しない。
